#taken from Logic-LLM/models/utils.py
#python3 utils.py openai_key model_name temperature

import backoff  # for exponential backoff
import openai
#from openai import OpenAI
import base64
import os
import posixpath
import json
import sys
from typing import Any

@backoff.on_exception(backoff.expo, openai.error.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.ChatCompletion.create(**kwargs)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')


class OpenAIModel:
    def __init__(self, API_KEY, model_name, max_new_tokens) -> None:
        openai.api_key = API_KEY
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens

    # used for chat-gpt and gpt-4
    def chat_generate(self, input_string, image_path, temperature = 0.0):
        base64_image = encode_image(image_path)
        response = chat_completions_with_backoff(
                model = self.model_name,
                messages=[
                        {"role": "user", "content":[
                            {
                                "type": "text",
                                "text": input_string
                            },
                            {
                                "type": "image_url",
                                "image_url": {"url": f"data:image/png;base64, {base64_image}"}
                            }
                        ]
            }
                    ],
                max_tokens = self.max_new_tokens,
                temperature = temperature,
                top_p = 1.0
        )
        generated_text = response['choices'][0]['message']['content'].strip()
        return generated_text

    def generate(self, input_string, image_path, temperature = 0.0):
        if self.model_name in ['gpt-4o']:
            return self.chat_generate(input_string, image_path, temperature)
        else:
            raise Exception("Model name not recognized")
    
    """def batch_chat_generate(self, messages_list, temperature = 0.0):
        open_ai_messages_list = []
        for message in messages_list:
            open_ai_messages_list.append(
                [{"role": "user", "content": message}]
            )
        predictions = asyncio.run(
            dispatch_openai_chat_requests(
                    open_ai_messages_list, self.model_name, temperature, self.max_new_tokens, 1.0, self.stop_words
            )
        )
        return [x['choices'][0]['message']['content'].strip() for x in predictions]

    def batch_generate(self, messages_list, temperature = 0.0):
        if self.model_name in ['gpt-4', 'gpt-3.5-turbo']:
            return self.batch_chat_generate(messages_list, temperature)
        else:
            raise Exception("Model name not recognized")"""
    
if __name__ == "__main__":

    temperature = float(sys.argv[3])
    openaimodel = OpenAIModel(str(sys.argv[1]), str(sys.argv[2]), 1000)
    domains = ['counting-locations']
    for domain in domains:
        input_path = posixpath.join(os.getcwd(), str(domain), "input_format.txt")
        f = open(input_path, "r")
        input_string = str(f.read())
        f.close()

        json_path = posixpath.join(os.getcwd(), str(domain), 'data.json')
        f = open(json_path)
        data = json.load(f)
        answer = []
        for i in data:
            image_path = posixpath.join(os.getcwd(), str(domain), 'data', str(i['id']))
            gpt_response = openaimodel.generate(input_string, image_path, temperature)
            gold_output = {
            "id": i["id"],
            "num_objects_over_table": i["num_objects_over_table"],
            "num_objects_under_table": i["num_objects_under_table"],
            "gpt_response": gpt_response
            # "object_positions": positions
            }
            answer.append(gold_output)
        f.close()

        json_path_write = posixpath.join(os.getcwd(), str(domain), 'answer.json')
        with open(json_path_write, 'w') as json_file:
            json.dump(answer, json_file, indent=4)