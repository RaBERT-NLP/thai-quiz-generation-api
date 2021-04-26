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

class QAModel():
    def __init__(self):
        self.mt5_tokenizer = MT5Tokenizer.from_pretrained("Pollawat/mt5-small-thai-qa-qg")
        self.mt5_model = MT5ForConditionalGeneration.from_pretrained("Pollawat/mt5-small-thai-qa-qg")

        self.wangchanberta_tokenizer = AutoTokenizer.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
        self.wangchanberta_model = AutoModelForMaskedLM.from_pretrained("airesearch/wangchanberta-base-att-spm-uncased")
        self.wangchanberta_pipeline = fill_mask = pipeline(task='fill-mask', tokenizer=self.wangchanberta_tokenizer, model=self.wangchanberta_model)

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

    def masking_sentence(self, text, target):
        return text.replace(target, '<mask>', 1)

    def generate_choices(self, text, answer, n_choices=3):
        masked_text = self.masking_sentence(text, answer)
        out = self.wangchanberta_pipeline(masked_text)
        choices = {answer}
        for i in range(n_choices):
            choices.add(out[i]['token_str'])
        return choices

    def generate_from_wiki(self, url, WINDOW_SIZE = 400, ROLLING = 300, NUM = 10):
        r = requests.get(url)
        encoding = chardet.detect(r.content)
        r.encoding = encoding
        content = trafilatura.extract(r.text)
        response = {}

        ith = 1
        for line in content.split('\n'):
            if len(line) > 150 and ith <= NUM:
                for i in range(0, max(1, len(line) - WINDOW_SIZE), ROLLING):
                    tmp_text = line[i:i+WINDOW_SIZE]
                    # print(tmp_text)
                    q, a = self.generate_quiz(tmp_text)
                    if q and a:
                        try:
                            x = generate_choices(line, a)
                            response[ith] = {
                                "question": q,
                                "choices": x,
                                "answer": a
                            }
                            print(f'{ith:<2}', q)
                            print('   ', f'{str(x):<100}', f'{a:>50}')
                            ith += 1
                        except:
                            pass
                    if ith > NUM:
                        break

        return response
        


qa = QAModel()

text = "กรุงเทพมหานคร เป็นเมืองหลวงและนครที่มีประชากรมากที่สุดของประเทศไทย"
url_wiki = "https://th.wikipedia.org/wiki/%E0%B8%9B%E0%B8%A3%E0%B8%B5%E0%B8%94%E0%B8%B5_%E0%B8%9E%E0%B8%99%E0%B8%A1%E0%B8%A2%E0%B8%87%E0%B8%84%E0%B9%8C"

# question,answer = qa.generate_quiz(text)
response = qa.generate_from_wiki(url=url_wiki)

# print(question,answer)
print(response['question'])

# choices = qa.generate_choices(text,answer)
# print(choices)
