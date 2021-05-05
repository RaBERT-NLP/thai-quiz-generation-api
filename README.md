# thai-quiz-generation-api

This repository is for NLP course at Chulalongkorn University. This repository is backend using Django for question and choices generation task. 
We use fine-tuned mT5 model with three dataset (NSC 2018, XQuAD, and Iapp-wiki-qa-dataset) for doing question generation task. 
We use WangchanBERTa to doing fill mask task to generate choices in choices generation task.

## Installation

First, install all required libraries.
```
pip install -r requirements.txt
```

Second, set up the Django.
```
python manage.py makemigrations
python manage.py migrate
```

## Run the project

To run the project with our thai-quiz-generation-web, please use port 8000
```
python manage.py runserver <port_num>
```

## APIs
We have to APIs which are:
1. <POST> /questions_text/
```
input (JSON):  { 
                 "text": <str> text for generate the question and choices,
                 "limit": <int> the number of questions
               }
               
output (JSON): {
                  "data": <list>[
                                    {
                                        "question"  : <str> Question text,
                                        "choices"   : <list> Contain  four choices,
                                        "answer"    : <str> Answer text,
                                        "answer_idx": <int> index of answer in choices list
                                    }
                                ]
               }
 ```

2. <POST> /questions_url/
```
input (JSON): { 
                "url": <str> url of content to generate the question and choices,
                "limit": <int> the number of questions
              }
           
output (JSON): {
                  "data": <list>[
                                    {
                                        "question"  : <str> Question text,
                                        "choices"   : <list> Contain  four choices,
                                        "answer"    : <str> Answer text,
                                        "answer_idx": <int> index of answer in choices list
                                    }
                                ]
               }
```
            
                  
                
       
