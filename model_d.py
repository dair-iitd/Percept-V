import openai
from openai import OpenAI
import base64
import backoff
import torch
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
    def chat_generate(self, input_string, image_path, temperature = 0.0, two_images = False, few_shot = False , few_shot_response = None , few_shot_image_path = None):
        client = OpenAI(api_key=self.api_key)
        if not few_shot:
            if two_images == False:    
                base64_image = encode_image(image_path[0])
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
                                    }
                                ]
                    }
                            ],
                        #max_completion_tokens = self.max_new_tokens,
                        temperature = temperature,
                        top_p = 0.0
                )
            else:
                base64_image1 = encode_image(image_path[0])
                base64_image2 = encode_image(image_path[1])
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
                                    }
                                ]
                    }
                            ],
                        #max_completion_tokens = self.max_new_tokens,
                        temperature = temperature,
                        top_p = 0.0
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
                temperature = temperature,
                top_p = 0.0
            )
            # print(json.dumps(json.loads(response.model_dump_json()), indent=4))
            generated_text = response.choices[-1].message.content.strip()
            return generated_text

    def generate(self, input_string, image_path, temperature = 0.0,  two_images = False, few_shot = False , few_shot_response = None , few_shot_image_path = None):
        if self.model_name in ['gpt-4o', 'o4-mini']:
            return self.chat_generate(input_string, image_path, temperature, two_images, few_shot, few_shot_response, few_shot_image_path)
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
#         vl_gpt = vl_gpt.to(torch.bbfloat16).eval()

        

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
#             bnb_4bit_compute_dtype=torch.bfloat16
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
#         # model = LlavaNextForConditionalGeneration.from_pretrained("llava-hf/llava-v1.6-mistral-7b-hf", torch_dtype=torch.bfloat16, low_cpu_mem_usage=True)
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

# Suppress all warnings
warnings.filterwarnings("ignore")



class Gemini:
    """
    A simple OpenAI Style Client for Vertex AI
    """
    def __init__(self, gcp_project_id, region='global' , model = "gemini-2.5-flash"):
        self.model = model
        self.client = genai.Client(
            vertexai=True,
            project=gcp_project_id,
            location=region
        )
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

    def generate(self, input_string, image_path, temperature = 0.0, two_images = False):


        if(two_images == False):
            with open(image_path[0], "rb") as f:
                data = f.read()

        
            contents = [
                # types.Part.from_uri(file_uri=file_uri, mime_type="image/png"),
                Part.from_bytes(data = data , mime_type="image/png"),
                Part.from_text(text=input_string)
            ]

            # generate_content_config = types.GenerateContentConfig(
            #     temperature=temperature,
            #     max_output_tokens=1000,
            #     safetySettings=self.safety_settings,
            #     candidateCount=1,
            # )
            try:
                ret = self.client.models.generate_content(
                    contents = contents,
                    model = self.model,
                    # config=generate_content_config
                )
                response = ret.candidates[0].content.parts[0].text
                return response
        
            except Exception as e:
                print(f"Error during generation: {e}")
                sys.exit(1)
                return None
        else:
            #image1_path = image_path[0]
            #uploaded_file = self.client.files.upload(file=image1_path)
            with open(image_path[0], "rb") as file:
                data = file.read()
            with open(image_path[1], "rb") as f:
                data1 = f.read()

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
        
            contents = [
                # types.Part.from_uri(file_uri=file_uri, mime_type="image/png"),
                Part.from_bytes(data = data , mime_type="image/png"),
                Part.from_bytes(data = data1 , mime_type="image/png"),
                Part.from_text(text=input_string)
            ]

            # generate_content_config = types.GenerateContentConfig(
            #     temperature=temperature,
            #     max_output_tokens=1000,
            #     safetySettings=self.safety_settings,
            #     candidateCount=1,
            # )
            try:
                ret = self.client.models.generate_content(
                    contents = contents,
                    model = self.model,
                    # config=generate_content_config
                )
                response = ret.candidates[0].content.parts[0].text
                return response
        
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

    
    
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

# class QwenWrapper:
#     def __init__(self, model_name="Qwen/Qwen2.5-VL-7B-Instruct", offload_folder="/root/.cache/huggingface/offload"):
#         """
#         Initialize the Qwen model with VRAM-safe loading.
#         """
#         print("Loading processor...")
#         self.processor = AutoProcessor.from_pretrained(model_name)

#         print("Loading model (FP16, multi-GPU, offload enabled)...")
#         max_mem = {0: "28GiB", 1: "28GiB"}  # Adjust per GPU; leave some free
#         self.model = AutoModelForVision2Seq.from_pretrained(
#             model_name,
#             device_map="auto",           # Automatic multi-GPU placement
#             dtype=torch.bfloat16,         # FP16 for memory efficiency
#             offload_folder=offload_folder, # Swap tensors to CPU if GPU full
#             offload_state_dict=True      # Offload model weights if needed
#         )
#         self.model.eval()  # inference mode
#         print("Model loaded successfully!")

#     def generate(self, prompt, image_path=None, temperature=1.0, two_images=False):
#         """
#         Generate output from prompt and optional images.
#         """
#         inputs = self.processor(
#             text=prompt,
#             images=image_path,
#             return_tensors="pt"
#         )

#         # Move input tensors to correct device
#         device = self.model.device
#         inputs = {k: v.to(device) for k, v in inputs.items()}

#         with torch.no_grad():  # prevent gradient memory usage
#             outputs = self.model.generate(
#                 **inputs,
#                 temperature=temperature,
#                 do_sample=True
#             )
#         return self.processor.decode(outputs[0], skip_special_tokens=True)

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq

class QwenWrapper:
    def __init__(self, model_name="Qwen/Qwen2.5-VL-7B-Instruct", device_map="auto", offload_folder=None):
        """
        Initializes the QwenWrapper with FP16, multi-GPU, and offloading support.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load processor
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)

        # Load model with fp16 and offload options
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map=device_map,
            offload_folder=offload_folder,
        )
    def generate(self, prompt, image_path=None, temperature=1.0, two_images=False, **kwargs):
        """
        Generates output from the Qwen model with proper image handling.
        
        Args:
            prompt (str): The text prompt.
            image_path (str or list, optional): Path(s) to image(s).
            temperature (float): Sampling temperature for generation.
            two_images (bool): If True, expects `image_path` as list of 2 images.
            **kwargs: Other generation kwargs.
            
        Returns:
            str: Model output text.
        """
        # Validate temperature
        if temperature <= 0.0:
            # Use greedy decoding instead of sampling
            do_sample = False
            temperature = 1.0  # placeholder, won't be used
        else:
            do_sample = True

        # Prepare images
        if image_path is not None:
            if two_images:
                if not isinstance(image_path, list):
                    image_path = [image_path]
                if len(image_path) != 2:
                    raise ValueError("two_images=True requires a list of 2 images")
            else:
                if isinstance(image_path, list):
                    if len(image_path) != 1:
                        raise ValueError("two_images=False requires a single image")
                    image_path = image_path[0]

            # Process images with text
            inputs = self.processor(
                text=prompt,
                images=image_path,
                return_tensors="pt"
            )
        else:
            # Only text
            inputs = self.processor(
                text=prompt,
                return_tensors="pt"
            )

        # Move all tensors to model device
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        # Generate output
        outputs = self.model.generate(
            **inputs,
            do_sample=do_sample,
            temperature=temperature,
            **kwargs
        )

        # Decode output tokens
        decoded = self.tokenizer.batch_decode(outputs, skip_special_tokens=True)
        return decoded[0] if len(decoded) == 1 else decoded

    # def generate(self, prompt, image_path=None, temperature=0.0, two_images=False, max_new_tokens=256):
    #     """
    #     Generate text using the Qwen model.
    #     - prompt: text input
    #     - image_path: optional single or list of images
    #     - temperature: 0 for greedy, >0 for sampling
    #     - two_images: whether input contains 2 images
    #     """
    #     # Prepare inputs
    #     if two_images and isinstance(image_path, list) and len(image_path) != 2:
    #         raise ValueError("two_images=True requires image_path to be a list of 2 images")

    #     inputs = self.processor(
    #         text=prompt,
    #         images=image_path if two_images else image_path,
    #         return_tensors="pt"
    #     )

    #     # Move to device
    #     inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

    #     # Determine sampling strategy
    #     do_sample = temperature > 0
    #     temp_value = temperature if do_sample else None

    #     # Generate
    #     with torch.no_grad():
    #         outputs = self.model.generate(
    #             **inputs,
    #             do_sample=do_sample,
    #             temperature=temp_value,
    #             max_new_tokens=max_new_tokens
    #         )

    #     # Decode output
    #     return self.processor.decode(outputs[0], skip_special_tokens=True)

class QwenWrapper:
    def __init__(self, model_name="Qwen/Qwen2.5-VL-7B-Instruct", device_map="auto", offload_folder=None):
        """
        Initializes the QwenWrapper with FP16, multi-GPU, and offloading support.
        """
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        # Load processor once
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)

        # Load model once with FP16 and device mapping
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_name,
            torch_dtype=torch.bfloat16,
            device_map=device_map,
            offload_folder=offload_folder,
        )

    def generate(self, prompt, image_path=None, temperature=0.0, two_images=False, max_new_tokens=40, **kwargs):
        """
        Generates output using Qwen model with proper image handling and token alignment.
        """
        if image_path is None:
            raise ValueError("image_path cannot be None for vision-to-sequence tasks.")

        # Load images
        image_data0 = Image.open(image_path[0]).convert("RGB")
        images = [image_data0]

        if two_images:
            if len(image_path) != 2:
                raise ValueError("two_images=True requires a list of exactly 2 image paths.")
            image_data1 = Image.open(image_path[1]).convert("RGB")
            images.append(image_data1)

        # Build message
        content = [{"type": "image", "image": img} for img in images]
        content.append({"type": "text", "text": prompt})

        message = [{"role": "user", "content": content}]

        # Process inputs
        inputs = self.processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        # Decide sampling or greedy
        do_sample = temperature > 0.0

        # Generate output
        outputs = self.model.generate(
            **inputs,
            do_sample=do_sample,
            temperature=temperature if do_sample else 1.0,
            max_new_tokens=max_new_tokens,
            **kwargs
        )

        # Decode
        decoded = self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])
        return decoded

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import gc
import torch
from transformers import AutoProcessor, AutoModelForVision2Seq
from PIL import Image
import gc

class QwenWrapper:
    def __init__(self, model_name="Qwen/Qwen2.5-VL-7B-Instruct", device_map="auto", offload_folder="./offload", dtype=torch.bfloat16):
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForVision2Seq.from_pretrained(
            model_name,
            device_map=device_map,
            offload_folder=offload_folder,
            dtype=dtype
        )
        self.model.eval()
        self.model.tie_weights()
    
    @torch.no_grad()
    def generate(self, prompt, image_path=None, temperature=0.0, two_images=False, max_new_tokens=40, **kwargs):
        do_sample = temperature > 0.0

        # Prepare images
        if image_path is not None:
            if two_images:
                if not isinstance(image_path, list):
                    image_path = [image_path]
                if len(image_path) != 2:
                    raise ValueError("two_images=True requires a list of 2 images")
                images = [Image.open(p).convert("RGB") for p in image_path]
            else:
                if isinstance(image_path, list):
                    if len(image_path) != 1:
                        raise ValueError("two_images=False requires a single image")
                    image_path = image_path[0]
                images = [Image.open(image_path).convert("RGB")]
        else:
            images = []

        # Build message for apply_chat_template (required for correct image tokenization)
        content = []
        for img in images:
            content.append({"type": "image", "image": img})
        content.append({"type": "text", "text": prompt})

        message = [{"role": "user", "content": content}]

        # Prepare inputs
        inputs = self.processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        # Generate
        outputs = self.model.generate(
            **inputs,
            do_sample=do_sample,
            max_new_tokens=max_new_tokens,
            **kwargs
        )

        # Decode
        decoded = self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])

        # Cleanup
        del inputs, outputs, images
        torch.cuda.empty_cache()
        gc.collect()

        return decoded


class Qwen:
    def __init__(self, model = "Qwen/Qwen2.5-VL-7B-Instruct"):
        self.model = model
    
    def generate(self, input_string, image_path, temperature = 0.0, two_images = False):
        
        processor = AutoProcessor.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct")
        model = AutoModelForVision2Seq.from_pretrained("Qwen/Qwen2.5-VL-7B-Instruct",
         device_map="auto",
         torch_dtype=torch.bfloat16 
        )

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
    

import torch
from transformers import AutoProcessor, AutoModelForVision2Seq, LlavaForConditionalGeneration
from PIL import Image
import gc

class GllavaWrapper:
    def __init__(self, model_name="renjiepi/G-LLaVA-7B", device_map="auto", offload_folder="./offload", dtype=torch.bfloat16):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.processor = AutoProcessor.from_pretrained(model_name)
        self.model = LlavaForConditionalGeneration.from_pretrained(
            model_name,
            torch_dtype=dtype
        ).to(self.device)
        #self.model.eval()
        #self.model.tie_weights()
    
    @torch.no_grad()
    def generate(self, prompt, image_path=None, temperature=0.0, two_images=False, max_new_tokens=40, **kwargs):
        do_sample = temperature > 0.0

        # Prepare images
        if image_path is not None:
            if two_images:
                if not isinstance(image_path, list):
                    image_path = [image_path]
                if len(image_path) != 2:
                    raise ValueError("two_images=True requires a list of 2 images")
                images = [Image.open(p).convert("RGB") for p in image_path]
            else:
                if isinstance(image_path, list):
                    if len(image_path) != 1:
                        raise ValueError("two_images=False requires a single image")
                    image_path = image_path[0]
                images = [Image.open(image_path).convert("RGB")]
        else:
            images = []

        # Build message for apply_chat_template (required for correct image tokenization)
        """content = []
        for img in images:
            content.append({"type": "image", "image": img})
        content.append({"type": "text", "text": prompt})

        message = [{"role": "user", "content": content}]"""

        # Prepare inputs
        inputs = self.processor(text=prompt, images=images, return_tensors="pt").to(self.device, torch.float16)

        # Generate
        output = self.model.generate(**inputs)
        decoded = self.processor.decode(output[0], skip_special_tokens=True)

        # Decode
        #decoded = self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])

        # Cleanup
        del inputs, outputs, images
        torch.cuda.empty_cache()
        gc.collect()

        return decoded

    
from transformers import AutoModelForCausalLM, AutoTokenizer  
from PIL import Image

class DeepSeek:
    def __init__(self, model = "deepseek-ai/Janus-Pro-7B"):
        self.model = model
    
    def generate(self, input_string, image_path, temperature = 0.0, two_images = False):
        
        model = AutoModelForCausalLM.from_pretrained("deepseek-ai/Janus-Pro-7B")  
        tokenizer = AutoTokenizer.from_pretrained("deepseek-ai/Janus-Pro-7B" ,
         device_map="auto",
    torch_dtype="auto"
        ) 

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

    
import torch
from transformers import AutoProcessor, AutoModelForCausalLM
from PIL import Image
import gc

class DeepSeekWrapper:
    """
    VRAM-safe DeepSeek wrapper compatible with multi-GPU, offloading, and image handling.
    """
    def __init__(self, model_name="deepseek-ai/Janus-Pro-7B", device_map="auto", offload_folder="./offload", dtype=torch.bfloat16):
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map=device_map,
            offload_folder=offload_folder,
            torch_dtype=dtype
        )
        self.model.eval()
        self.model.tie_weights()
    
    @torch.no_grad()
    def generate(self, prompt, image_path=None, temperature=0.0, two_images=False, max_new_tokens=40, **kwargs):
        """
        Generate text from DeepSeek model with proper image handling.
        Args:
            prompt (str): Text prompt
            image_path (str or list): Path(s) to image(s)
            temperature (float): Sampling temperature
            two_images (bool): True if two images
            max_new_tokens (int): Max tokens to generate
        Returns:
            str: Generated text
        """
        do_sample = temperature > 0.0

        # Prepare images
        images = []
        if image_path is not None:
            if two_images:
                if not isinstance(image_path, list) or len(image_path) != 2:
                    raise ValueError("two_images=True requires a list of 2 images")
                images = [Image.open(p).convert("RGB") for p in image_path]
            else:
                if isinstance(image_path, list):
                    if len(image_path) != 1:
                        raise ValueError("two_images=False requires a single image")
                    image_path = image_path[0]
                images = [Image.open(image_path).convert("RGB")]

        # Build message
        content = [{"type": "image", "image": img} for img in images]
        content.append({"type": "text", "text": prompt})
        message = [{"role": "user", "content": content}]

        # Process inputs
        inputs = self.processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        # Generate output
        outputs = self.model.generate(
            **inputs,
            do_sample=do_sample,
            temperature=temperature if do_sample else 1.0,
            max_new_tokens=max_new_tokens,
            **kwargs
        )

        # Decode
        decoded = self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])

        # Cleanup
        del inputs, outputs, images
        torch.cuda.empty_cache()
        gc.collect()

        return decoded

from transformers import AutoProcessor
from transformers import AutoModel
from PIL import Image
import torch
import gc

class DeepSeekWrapper:
    def __init__(self, model_name="deepseek-ai/Janus-Pro-7B", device_map="auto", offload_folder="./offload", dtype=torch.bfloat16):
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)
        self.model = AutoModel.from_pretrained(
            model_name,
            device_map=device_map,
            offload_folder=offload_folder,
            torch_dtype=dtype,
        )
        self.model.eval()
    
    @torch.no_grad()
    def generate(self, prompt, image_path, two_images=False, max_new_tokens=40, temperature=0.0, **kwargs):
        # Load images
        images = [Image.open(image_path[0]).convert("RGB")]
        if two_images:
            images.append(Image.open(image_path[1]).convert("RGB"))

        # Build message for apply_chat_template
        content = [{"type": "image", "image": img} for img in images]
        content.append({"type": "text", "text": prompt})
        message = [{"role": "user", "content": content}]

        # Prepare inputs
        inputs = self.processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        # Sampling or greedy
        do_sample = temperature > 0.0

        # Generate output
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature if do_sample else 1.0,
            **kwargs
        )

        # Decode
        decoded = self.processor.decode(outputs[0][inputs["input_ids"].shape[-1]:])

        # Cleanup
        del inputs, outputs, images
        torch.cuda.empty_cache()
        gc.collect()

        return decoded


from transformers import AutoProcessor, AutoModel
from PIL import Image
import torch
import gc

class DeepSeekWrapper:
    def __init__(
        self,
        model_name="deepseek-ai/Janus-Pro-7B",
        device_map="auto",
        offload_folder="./offload",
        dtype=torch.bfloat16
    ):
        """
        Memory-optimized DeepSeek wrapper for multimodal generation.
        Supports single or double image + text prompts.
        """
        # Processor for tokenization & multimodal inputs
        self.processor = AutoProcessor.from_pretrained(model_name, use_fast=True)

        # Load model with device mapping & offloading
        self.model = AutoModel.from_pretrained(
            model_name,
            device_map=device_map,
            offload_folder=offload_folder,
            torch_dtype=dtype,
        )
        self.model.eval()

    @torch.no_grad()
    def generate(
        self,
        prompt=None,
        image_path=None,
        two_images=False,
        max_new_tokens=40,
        temperature=0.0,
        **kwargs
    ):
        """
        Generate text from prompt and optional image(s).
        """
        if image_path is None and prompt is None:
            raise ValueError("At least one of prompt or image_path must be provided.")

        # Load images
        images = []
        if image_path is not None:
            images.append(Image.open(image_path[0]).convert("RGB"))
            if two_images and len(image_path) > 1:
                images.append(Image.open(image_path[1]).convert("RGB"))

        # Build message for apply_chat_template
        content = [{"type": "image", "image": img} for img in images] if images else []
        if prompt:
            content.append({"type": "text", "text": prompt})

        message = [{"role": "user", "content": content}]

        # Prepare inputs with processor
        inputs = self.processor.apply_chat_template(
            message,
            add_generation_prompt=True,
            tokenize=True,
            return_dict=True,
            return_tensors="pt"
        ).to(self.model.device)

        # Determine sampling strategy
        do_sample = temperature > 0.0

        # Generate
        outputs = self.model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=do_sample,
            temperature=temperature if do_sample else 1.0,
            **kwargs
        )

        # Decode only the newly generated part
        start_idx = inputs["input_ids"].shape[-1]
        decoded = self.processor.decode(outputs[0][start_idx:])

        # Cleanup to reduce memory usage
        del inputs, outputs, images
        torch.cuda.empty_cache()
        gc.collect()

        return decoded



import torch
import gc
from PIL import Image

# Import from cloned DeepSeek repo instead of plain transformers
# (Adjust import paths if repo is inside a subfolder)


# from deepseek_vl2.models import DeepseekForConditionalGeneration
# from deepseek_vl2.processing import DeepseekProcessor
import torch
from deepseek_vl2.models import DeepseekVLV2Processor, DeepseekVLV2ForCausalLM
from deepseek_vl2.utils.io import load_pil_images
import gc

class DeepSeekWrapper:
    def __init__(self, model_name="deepseek-ai/deepseek-vl2-tiny", device="cuda", dtype=torch.bfloat16):
        """
        DeepSeek-VL2 wrapper for multimodal text+image generation.
        """
        self.device = device
        self.processor: DeepseekVLV2Processor = DeepseekVLV2Processor.from_pretrained(model_name)
        self.tokenizer = self.processor.tokenizer

        # Load model
        self.model: DeepseekVLV2ForCausalLM = DeepseekVLV2ForCausalLM.from_pretrained(model_name, trust_remote_code=True)
        self.model = self.model.to(dtype).to(device).eval()

    @torch.no_grad()
    def generate(self, conversation, max_new_tokens=512, temperature=0.0):
        """
        Generate responses from conversation + optional images.

        conversation: List of dicts like:
        [
            {"role": "<|User|>", "content": "your text", "images": ["img1.png", "img2.png"]},
            {"role": "<|Assistant|>", "content": ""}
        ]
        """

        # Load PIL images
        pil_images = load_pil_images(conversation)

        # Prepare inputs
        prepared_inputs = self.processor(
            conversations=conversation,
            images=pil_images,
            force_batchify=True,
            system_prompt=""
        ).to(self.device)

        # Get embeddings
        inputs_embeds = self.model.prepare_inputs_embeds(**prepared_inputs)

        # Generate outputs
        outputs = self.model.language.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=prepared_inputs.attention_mask,
            pad_token_id=self.tokenizer.eos_token_id,
            bos_token_id=self.tokenizer.bos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=max_new_tokens,
            do_sample=temperature>0.0,
            use_cache=True
        )

        # Decode
        answer = self.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=False)

        # Optional cleanup
        del prepared_inputs, inputs_embeds, outputs, pil_images
        torch.cuda.empty_cache()
        gc.collect()

        return answer

import torch
from deepseek_vl2.models import DeepseekVLV2Processor, DeepseekVLV2ForCausalLM
from deepseek_vl2.utils.io import load_pil_images
import gc

class DeepSeekWrapper:
    def __init__(self, model_name="deepseek-ai/deepseek-vl2-tiny", device="cuda", dtype=torch.bfloat16):
        self.device = device
        self.processor: DeepseekVLV2Processor = DeepseekVLV2Processor.from_pretrained(model_name)
        self.tokenizer = self.processor.tokenizer
        self.model: DeepseekVLV2ForCausalLM = DeepseekVLV2ForCausalLM.from_pretrained(
            model_name, trust_remote_code=True
        )
        self.model = self.model.to(dtype).to(device).eval()

    @torch.no_grad()
    def generate(self, prompt=None, image_path=None, temperature=0.0, two_images=False, max_new_tokens=512):
        if prompt is None and image_path is None:
            raise ValueError("At least one of prompt or image_path must be provided.")

        conversation = []
        user_entry = {"role": "<|User|>", "content": prompt or "", "images": []}

        # Add images
        if image_path is not None:
            if isinstance(image_path, str):
                user_entry["images"].append(image_path)
            else:
                user_entry["images"].append(image_path[0])
                if two_images and len(image_path) > 1:
                    user_entry["images"].append(image_path[1])

        conversation.append(user_entry)
        conversation.append({"role": "<|Assistant|>", "content": "", "images": []})

        # Load images
        pil_images = load_pil_images(conversation)

        # Prepare inputs
        prepared_inputs = self.processor(
            conversations=conversation,
            images=pil_images,
            force_batchify=True,
            system_prompt=""
        ).to(self.device)

        # Get embeddings
        inputs_embeds = self.model.prepare_inputs_embeds(**prepared_inputs)

        # Generate
        outputs = self.model.language.generate(
            inputs_embeds=inputs_embeds,
            attention_mask=prepared_inputs.attention_mask,
            pad_token_id=self.tokenizer.eos_token_id,
            bos_token_id=self.tokenizer.bos_token_id,
            eos_token_id=self.tokenizer.eos_token_id,
            max_new_tokens=max_new_tokens,
            do_sample=temperature > 0.0,
            use_cache=True
        )

        # Decode
        answer = self.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=False)

        # Cleanup
        del prepared_inputs, inputs_embeds, outputs, pil_images
        torch.cuda.empty_cache()
        gc.collect()

        return answer

# from deepseek_vl2.models import DeepseekVLV2Processor, DeepseekVLV2ForCausalLM
# from deepseek_vl2.utils.io import load_pil_images
# import torch
# import gc
# from PIL import Image

# class DeepSeekWrapper:
#     def __init__(
#         self,
#         model_name="deepseek-ai/deepseek-vl2-tiny",
#         dtype=torch.bfloat16,
#     ):
#         """
#         DeepSeek wrapper for multimodal perception tasks.
#         Fully prompt-driven; output format is not enforced in code.
#         """
#         self.processor = DeepseekVLV2Processor.from_pretrained(model_name)
#         self.model = DeepseekVLV2ForCausalLM.from_pretrained(model_name, trust_remote_code=True)
#         self.model = self.model.to(dtype).cuda().eval()
#         self.tokenizer = self.processor.tokenizer

#     @torch.no_grad()
#     def generate(
#         self,
#         prompt: str,
#         image_path: list = None,
#         max_new_tokens: int = 512,
#         temperature: float = 0.0,
#         two_images: bool = False,
#         **kwargs,
#     ):
#         """
#         Args:
#             prompt: Task description including desired output format.
#             image_path: List of image file paths.
#             max_new_tokens: Max tokens for generation.
#             temperature: Sampling temperature (0 = deterministic).
#             two_images: Whether to process two images.
#         Returns:
#             Raw model output (fully prompt-driven, unmodified).
#         """
#         # Load images
#         images = []
#         if image_path:
#             images.append(Image.open(image_path[0]).convert("RGB"))
#             if two_images and len(image_path) > 1:
#                 images.append(Image.open(image_path[1]).convert("RGB"))

#         # Prepare conversation message
#         message = [{"role": "<|User|>", "content": prompt}]
#         if images:
#             message[0]["content"] = "<|grounding|>\n" + message[0]["content"]
#             message[0]["images"] = images

#         # Prepare inputs
#         pil_images = load_pil_images(message) if images else None
#         inputs = self.processor(
#             conversations=message,
#             images=pil_images,
#             force_batchify=True,
#             system_prompt="",
#         ).to(self.model.device)

#         # Run image encoder if images exist
#         if pil_images:
#             inputs_embeds = self.model.prepare_inputs_embeds(**inputs)
#             outputs = self.model.language.generate(
#                 inputs_embeds=inputs_embeds,
#                 attention_mask=inputs.attention_mask,
#                 pad_token_id=self.tokenizer.eos_token_id,
#                 bos_token_id=self.tokenizer.bos_token_id,
#                 eos_token_id=self.tokenizer.eos_token_id,
#                 max_new_tokens=max_new_tokens,
#                 do_sample=temperature > 0.0,
#                 temperature=temperature if temperature > 0.0 else 1.0,
#                 use_cache=True,
#                 **kwargs,
#             )
#         else:
#             outputs = self.model.generate(
#                 **inputs,
#                 max_new_tokens=max_new_tokens,
#                 do_sample=temperature > 0.0,
#                 temperature=temperature if temperature > 0.0 else 1.0,
#                 **kwargs,
#             )

#         # Decode raw output
#         decoded = self.tokenizer.decode(outputs[0].cpu().tolist(), skip_special_tokens=True)

#         # Cleanup
#         del inputs, outputs, images
#         torch.cuda.empty_cache()
#         gc.collect()

#         return decoded

