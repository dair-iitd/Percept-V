import openai
from openai import OpenAI
import base64
import backoff

@backoff.on_exception(backoff.expo, openai.RateLimitError)
def chat_completions_with_backoff(**kwargs):
    return openai.chat.completions.create(**kwargs)

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')
    
class OpenAIModel:
    def __init__(self, API_KEY, model_name, max_new_tokens) -> None:
        #openai.api_key = API_KEY
        self.api_key = API_KEY
        self.model_name = model_name
        self.max_new_tokens = max_new_tokens

    # used for chat-gpt and gpt-4
    def chat_generate(self, input_string, gold_answer, image_path, example_image, temperature = 0.0, two_images = False, few_shot = False , few_shot_response = None , few_shot_image_path = None):
        client = OpenAI(api_key=self.api_key)
        if not few_shot:
            if two_images == False:    
                base64_image = encode_image(image_path[0])
                base64_example = encode_image(example_image[0])
                response = client.chat.completions.create(
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
                                    },
                                    {
                                        "type": "text",
                                        "text": "Here is an example-"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64, {base64_example}"}
                                    },
                                    {
                                        "type": "text",
                                        "text": str(gold_answer)
                                    }

                                ]
                    }
                            ],
                        #max_completion_tokens = self.max_new_tokens,
                        #temperature = temperature,
                        #top_p = 0.0
                )
            else:
                base64_image1 = encode_image(image_path[0])
                base64_image2 = encode_image(image_path[1])
                base64_example1 = encode_image(example_image[0])
                base64_example2 = encode_image(example_image[1])
                response = client.chat.completions.create(
                        model = self.model_name,
                        messages=[
                                {"role": "user", "content":[
                                    {
                                        "type": "text",
                                        "text": input_string
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64, {base64_image1}"}
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64, {base64_image2}"}
                                    },
                                    {
                                        "type": "text",
                                        "text": "Here is an example-"
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64, {base64_example1}"}
                                    },
                                    {
                                        "type": "image_url",
                                        "image_url": {"url": f"data:image/png;base64, {base64_example2}"}
                                    },
                                    {
                                        "type": "text",
                                        "text": str(gold_answer)
                                    }
                                ]
                    }
                            ],
                        #max_completion_tokens = self.max_new_tokens,
                        #temperature = temperature,
                        #top_p = 0.0
                )
            # print(json.dumps(json.loads(response.model_dump_json()), indent=4))
            generated_text = response.choices[0].message.content.strip()
            
            return generated_text
        else:
            few_shot_messages = []
            for i in range(len(few_shot_response)):
                base64_image = encode_image(few_shot_image_path[i])
                few_shot_messages.append(
                    {"role": "user", "content":[
                        {
                            "type": "text",
                            "text": input_string
                        },
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/png;base64, {base64_image}"}
                        }
                    ]}   
                )
                few_shot_messages.append(
                    {"role": "assistant", "content": few_shot_response[i]}
                )
            base64_image = encode_image(image_path)
            few_shot_messages.append(
                {"role": "user", "content":[
                    {
                        "type": "text",
                        "text": input_string
                    },
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/png;base64, {base64_image}"}
                    }
                ]}
            )

            response = client.chat.completions.create(
                model = self.model_name,
                messages = few_shot_messages,
                #max_tokens = self.max_new_tokens,
                #temperature = temperature,
                #top_p = 0.0
            )
            # print(json.dumps(json.loads(response.model_dump_json()), indent=4))
            generated_text = response.choices[-1].message.content.strip()
            return generated_text

    def generate(self, input_string, gold_answer, image_path, example_image, temperature = 0.0,  two_images = False, few_shot = False , few_shot_response = None , few_shot_image_path = None):
        if self.model_name in ['gpt-5-mini', 'gpt-4o', 'o4-mini']:
            return self.chat_generate(input_string, gold_answer, image_path, example_image, temperature, two_images, few_shot, few_shot_response, few_shot_image_path)
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
    
# from google import genai
# from google.genai import types

# import PIL.Image


# class Gemini: 
#     def __init__(self, API_KEY , model_name , max_new_tokens) -> None:
#         self.model_name = model_name
#         self.max_new_tokens = max_new_tokens
#         self.client = genai.Client(api_key=API_KEY)

#     def generate(self, input_string, image_path , temperature = 0.0 , few_shot = False , few_shot_response = None , few_shot_image_path = None):
#         image = PIL.Image.open(image_path)

#         response = self.client.models.generate_content(
#             model = "gemini-2.0-flash",
#             contents=[image , input_string]
#         )

#         return response.text

# # Load model directly
# # from transformers import AutoModel
# import torch
# from transformers import AutoModelForCausalLM  , AutoTokenizer
# from janus.models import MultiModalityCausalLM, VLChatProcessor
# from janus.utils.io import load_pil_images


# class Janus:
#     def __init__(self) -> None:
#         pass

#     def generate(self, input_string, image_path, temperature = 0.0 , few_shot = False , few_shot_response = None , few_shot_image_path = None):

#         # specify the path to the model
#         model_path = "deepseek-ai/Janus-Pro-1B"
#         vl_chat_processor: VLChatProcessor = VLChatProcessor.from_pretrained(model_path)
#         tokenizer = vl_chat_processor.tokenizer

#         vl_gpt: MultiModalityCausalLM = AutoModelForCausalLM.from_pretrained(
#             model_path, trust_remote_code=True
#         )
#         vl_gpt = vl_gpt.to(torch.bfloat16).eval()

        

#         # image = encode_image(image_path)

#         conversation = [
#             {
#                 "role": "<|User|>",
#                 "content": f"<image_placeholder>\n{input_string}",
#                 "images": [image_path],
#             },
#             {"role": "<|Assistant|>", "content": ""},
#         ]

#         # load images and prepare for inputs
#         pil_images = load_pil_images(conversation)
#         prepare_inputs = vl_chat_processor(
#             conversations=conversation, images=pil_images, force_batchify=True
#         ).to(vl_gpt.device)

#         # # run image encoder to get the image embeddings
#         inputs_embeds = vl_gpt.prepare_inputs_embeds(**prepare_inputs)

#         # # run the model to get the response
#         outputs = vl_gpt.language_model.generate(
#             inputs_embeds=inputs_embeds,
#             attention_mask=prepare_inputs.attention_mask,
#             pad_token_id=tokenizer.eos_token_id,
#             bos_token_id=tokenizer.bos_token_id,
#             eos_token_id=tokenizer.eos_token_id,
#             max_new_tokens=512,
#             do_sample=False,
#             use_cache=True,
#         )

#         answer = tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)
#         # print(f"{prepare_inputs['sft_format'][0]}", answer)
#         return answer


#         # model = AutoModelForCausalLM.from_pretrained("deepseek-ai/Janus-Pro-1B")
#         # tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/Janus-Pro-1B")


# from transformers import LlavaNextProcessor, LlavaNextForConditionalGeneration
# import torch
# from PIL import Image
# import sys
# from transformers import BitsAndBytesConfig
# from transformers import pipeline

# class LLavaNext:
#     def __init__(self) -> None:

#         pass
    
#     def generate(self, input_string, image_path, temperature = 0.0 , few_shot = False , few_shot_response = None , few_shot_image_path = None):
#         quantization_config = BitsAndBytesConfig(
#             load_in_4bit=True,
#             bnb_4bit_compute_dtype=torch.float16
#         )


#         model_id = "llava-hf/llava-1.5-7b-hf"

#         pipe = pipeline("image-to-text", model=model_id, model_kwargs={"quantization_config": quantization_config})
#         image = PIL.Image.open(image_path)

#         max_new_tokens = 200
#         prompt = "fUSER: <image>\{input_string}\nASSISTANT:"

#         outputs = pipe(image, prompt=prompt, generate_kwargs={"max_new_tokens": 200})

#         return print(outputs[0]["generated_text"])

#         # # Load the model in half-precision
#         # processor = LlavaNextProcessor.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf")
#         # model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf", torch_dtype=torch.float16, low_cpu_mem_usage=True)
#         # model.to("cuda:0")

#         # 

#         # conversation = [
#         #     {
#         #         "role": "user",
#         #         "content": [
#         #             {"type": "image"},
#         #             {"type": "text", "text": input_string},
#         #         ],
#         #     },
#         # ]
#         # prompt = processor.apply_chat_template(conversation, add_generation_prompt=True)
#         # inputs = processor(image, prompt, return_tensors="pt").to("cuda:0")

#         # # autoregressively complete prompt
#         # output = model.generate(**inputs, max_new_tokens=100)

#         # print(processor.decode(output[0], skip_special_tokens=True))
#         # sys.exit(0)


        
import os
import base64
from google import genai
from google.genai import types

import base64
from google.genai.types import Part , Content
import sys
import pathlib
import os
import posixpath
import json
import warnings
import PIL.Image


# Suppress all warnings
warnings.filterwarnings("ignore")



class Gemini:
    """
    A simple OpenAI Style Client for Vertex AI
    """
    def __init__(self, gcp_project_id, region='global' , model = "gemini-2.5-flash"):
        self.model = model
        self.client = genai.Client(api_key=gcp_project_id)
        self.safety_settings = [
            types.SafetySetting( 
                category="HARM_CATEGORY_HATE_SPEECH",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_DANGEROUS_CONTENT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
                threshold="OFF"
            ),
            types.SafetySetting(
                category="HARM_CATEGORY_HARASSMENT",
                threshold="OFF"
            )
        ]

    def prompt_model(self, messages, model, temperature=0.0, top_p=0.0, max_output_tokens=128):
        contents = [
            types.Content(role='user' if msg['role'] == 'user' else 'model', parts=[types.Part.from_text(text=msg['content'])])
            for msg in messages if msg['role'] != 'system'
        ]
        system_instructions = None
        for msg in messages:
            if msg['role'] == 'system':
                system_instructions = msg['content']
                break

        generate_content_config = types.GenerateContentConfig(
            temperature=temperature,
            top_p=top_p,
            max_output_tokens=max_output_tokens,
            systemInstruction=system_instructions,
            safetySettings=self.safety_settings,
            candidateCount=1,
        )

        ret = self.client.models.generate_content(
            model = model,
            contents = contents,
            config = generate_content_config,
        )
        response = ret.candidates[0].content.parts[0].text

        return response

    def generate(self, input_string, gold_answer, image_path, example_image, temperature = 0.0, two_images = False):


        if(two_images == False):
            """with open(image_path[0], "rb") as f:
                data = f.read()

        
            contents = [
                # types.Part.from_uri(file_uri=file_uri, mime_type="image/png"),
                Part.from_bytes(data = data , mime_type="image/png"),
                Part.from_text(text=input_string)
            ]"""

            img = PIL.Image.open(image_path[0])
            example_img = PIL.Image.open(example_image[0])
            

            # generate_content_config = types.GenerateContentConfig(
            #     temperature=temperature,
            #     max_output_tokens=1000,
            #     safetySettings=self.safety_settings,
            #     candidateCount=1,
            # )
            try:
                """ret = self.client.models.generate_content(
                    contents = contents,
                    model = self.model,
                    # config=generate_content_config
                )"""
                response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    img, # The SDK handles the inline data conversion
                    input_string,
                    "Here is an example- ",
                    example_img,
                    str(gold_answer)
                ])

                return response.candidates[0].content.parts[0].text
        
            except Exception as e:
                print(f"Error during generation: {e}")
                sys.exit(1)
                return None
        else:
            #image1_path = image_path[0]
            #uploaded_file = self.client.files.upload(file=image1_path)
            """with open(image_path[0], "rb") as file:
                data = file.read()
            with open(image_path[1], "rb") as f:
                data1 = f.read()"""

            """images = [Part(data=data, mime_type="image/jpeg"), Part(data=data1, mime_type="image/png"),]

            contents = [
                            {
                                "role": "user",
                                "parts": [
                                {"text": input_string},
                                *images,
                                ],
                            },
                        ]"""
        
            """contents = [
                # types.Part.from_uri(file_uri=file_uri, mime_type="image/png"),
                Part.from_bytes(data = data , mime_type="image/png"),
                Part.from_bytes(data = data1 , mime_type="image/png"),
                Part.from_text(text=input_string)
            ]"""
            
            img = PIL.Image.open(image_path[0])
            img1 = PIL.Image.open(image_path[1])
            example_img = PIL.Image.open(example_image[0])
            example_img1 = PIL.Image.open(example_image[1])

            
            # generate_content_config = types.GenerateContentConfig(
            #     temperature=temperature,
            #     max_output_tokens=1000,
            #     safetySettings=self.safety_settings,
            #     candidateCount=1,
            # )
            try:
                response = self.client.models.generate_content(
                model=self.model,
                contents=[
                    img, # The SDK handles the inline data 
                    img1,
                    input_string,
                    "Here is an example- ",
                    example_img,
                    example_img1,
                    str(gold_answer)
                ])

                return response.candidates[0].content.parts[0].text
        
            except Exception as e:
                print(f"Error during generation: {e}")
                sys.exit(1)
                return None

    def batch_generate(self, input_string, domain , temperature = 0.0 , skip = 0 , append = False):

        batched_input = []
        id = 1
        json_path = posixpath.join(os.getcwd(), str(domain), 'data.json')
        with open(json_path, 'r') as f:
            data = json.load(f)
        
        for i in data:
            if skip > 0:
                skip -= 1
                continue
            
            image_path = posixpath.join(os.getcwd(), str(domain), 'data', str(i['id']))
            with open(image_path, "rb") as f:
                image_data = f.read()
            
            contents = [{
                "parts" : { "image" : Part.from_bytes(data = image_data , mime_type="image/png"),
                            "text" :Part.from_text(text=input_string)
                },
                "role" : "user"
            }
            ]

            temp_input = {
                "id": id,
                "reqeust": {
                    "contents": contents
                }
            }
            batched_input.append(temp_input)
            id += 1
        json_path_write = posixpath.join(os.getcwd(), str(domain), f'answer_batch_job.json')
        if append:
            with open(json_path_write, "r") as f:
                old_data = json.load(f)
                old_data.extend(batched_input)
            with open(json_path_write, "w") as f:
                json.dump(old_data, f, indent=2)
        else:
            with open(json_path_write, "w") as f:
                json.dump(batched_input, f, indent=2)


from anthropic import AnthropicVertex

class Claude:
    def __init__(self, gcp_project_id, region='us-east5' , model = "claude-3-5-sonnet-v2@20241022"):
        self.model = model
        self.client = AnthropicVertex(
            project_id=gcp_project_id,
            region=region
        )
    
    def generate(self, input_string, image_path, temperature = 0.0, two_images = False):
        
        #get base64 data from image_path
        image_data = encode_image(image_path[0])
        if two_images:
            image_data1 = encode_image(image_path[1])


        if two_images == False:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-v2@20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "text",
                                "text": input_string,
                            }
                        ],
                    }
                ],
            )
        
        else:
            message = self.client.messages.create(
                model="claude-3-5-sonnet-v2@20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data,
                                },
                            },
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_data1,
                                },
                            },
                            {
                                "type": "text",
                                "text": input_string,
                            }
                        ],
                    }
                ],
            )

        return message.content[0].text.strip()

    
    
"""from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image

class Qwen:
    def __init__(self, model = "Qwen/Qwen2.5-VL-7B-Instruct"):
        self.model = model
    
    def generate(self, input_string, image_path, temperature = 0.0, two_images = False):
        
        processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")
        model = AutoModelForVision2Seq.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")

        #get base64 data from image_path
        image_data = Image.open(image_path[0]).convert("RGB")
        if two_images:
            image_data1 = Image.open(image_path[1]).convert("RGB")

        outputs = []
        if two_images == False:
            message = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_data},
                        {"type": "text", "text": input_string}
                    ]
                },
            ]

            inputs = processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",).to(model.device)

            outputs = model.generate(**inputs, max_new_tokens=40)
            
        else:
            message = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_data},
                        {"type": "image", "image": image_data1},
                        {"type": "text", "text": input_string}
                    ]
                },
            ]

            inputs = processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",).to(model.device)

            outputs = model.generate(**inputs, max_new_tokens=40)

        return processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])

    
from transformers import AutoModelForCausalLM, AutoTokenizer  
from PIL import Image

class DeepSeek:
    def __init__(self, model = "deepseek-ai/Janus-Pro-7B"):
        self.model = model
    
    def generate(self, input_string, image_path, temperature = 0.0, two_images = False):
        
        model = AutoModelForCausalLM.from_pretrained("deepseek-ai/Janus-Pro-7B")  
        tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/Janus-Pro-7B") 

        #get base64 data from image_path
        image_data = encode_image(image_path[0])
        if two_images:
            image_data1 = encode_image(image_path[1])

        outputs = []
        if two_images == False:
            message = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_data},
                        {"type": "text", "text": input_string}
                    ]
                },
            ]

            inputs = processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",).to(model.device)

            outputs = model.generate(**inputs, max_new_tokens=40)
            
        else:
            message = [
                {
                    "role": "user",
                    "content": [
                        {"type": "image", "image": image_data},
                        {"type": "image", "image": image_data1},
                        {"type": "text", "text": input_string}
                    ]
                },
            ]

            inputs = processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt",).to(model.device)

            outputs = model.generate(**inputs, max_new_tokens=40)

        return processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])

    
"""