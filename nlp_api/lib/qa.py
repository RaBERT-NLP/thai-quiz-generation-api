import re
import os
import json
import chardet
import requests
import trafilatura
import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
from transformers import (
    MT5Tokenizer, MT5ForConditionalGeneration, 
    AutoTokenizer, AutoModelForMaskedLM, pipeline
)
from pythainlp.corpus.common import thai_stopwords

class QAModel():
    def __init__(self):
        self.mt5_tokenizer = MT5Tokenizer.from_pretrained("Pollawat/mt5-small-thai-qa-qg")
        self.mt5_model = MT5ForConditionalGeneration.from_pretrained("Pollawat/mt5-small-thai-qa-qg")

        self.wangchanberta_tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
        self.wangchanberta_model = AutoModelForMaskedLM.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
        self.wangchanberta_pipeline = pipeline(task='fill-mask', tokenizer=self.wangchanberta_tokenizer, model=self.wangchanberta_model)
        self.stopwords = thai_stopwords()
    
    def generate_quiz(self, text, num_return_sequences=5):
        input_ids = self.mt5_tokenizer.encode(text, return_tensors='pt')

        beam_output = self.mt5_model.generate(
            input_ids, 
            max_length=80,
            num_beams=num_return_sequences,
            early_stopping=True,
            num_return_sequences=num_return_sequences,
            repetition_penalty=1, 
            length_penalty=1,
        )

        for i in range(num_return_sequences):
            text = self.mt5_tokenizer.decode(beam_output[i])
            if '<ANS>' in text:
                question, answer = text.split('<ANS>')
                question = re.sub('</?\w*>', '', question).strip()
                answer = re.sub('</?\w*>', '', answer).strip()

                if question.find('เป็น') == 0 or answer in question or len(answer) > len(question) or len(question) < 30:
                    continue

                return question, answer
        return None, None

    def generate_quiz_text(self, text, window_size=200, rolling=200):
        for i in range(0, max(1, len(text) - window_size), rolling):
            tmp_text = text[i:i+window_size]
            q, a = self.generate_quiz(tmp_text)
            if q and a:
                return q, a
        return None, None

    def masking_sentence(self, text, target):
        return text.replace(target, '<mask>', 1)

    def generate_choices(self, text, answer, n_choices=3):
        masked_text = self.masking_sentence(text, answer)
        out = self.wangchanberta_pipeline(masked_text)
        choices = {answer}
        i = 0
        while len(choices) < n_choices+1:
            try:
                temp_out = out[i]['token_str'].strip()
                if '▁' not in temp_out and temp_out.strip('▁') not in self.stopwords:
                    choices.add(temp_out)
                i += 1
            except:
                break
        return list(choices)
    
    def generate_quizzes_url(self, url, n_choices=3, window_size=400, rolling=300, n_questions=5):
        r = requests.get(url)
        encoding = chardet.detect(r.content)
        r.encoding = encoding
        content = trafilatura.extract(r.text)
        response = []

        lasted_q = ''
        ith = 1
        for line in content.split('\n'):
            if len(line) > 150 and ith <= n_questions:
                for i in range(0, max(1, len(line) - window_size), rolling):
                    tmp_text = line[i:i+window_size]
                    q, a = self.generate_quiz(tmp_text)
                    if q and a:
                        try:
                            if q == lasted_q:
                                continue
                            x = self.generate_choices(line, a, n_choices)
                            if len(x) != n_choices+1:
                                if len(x) == n_choices:
                                    x.append('ไม่มีข้อใดถูก')
                                else:
                                    continue
                            
                            if len(x) == n_choices+1:
                                response.append(dict({
                                    "question": q,
                                    "choices": x,
                                    "answer": a,
                                    "answer_idx": x.index(a)
                                }))
                                lasted_q = q
                                ith += 1
                            else:
                                continue
                        except:
                            pass
                    if ith > n_questions:
                        break
        return response
