import os
import re
import posixpath
import json
import sys
import argparse
import importlib
from typing import Any
from dotenv import load_dotenv
from model_d import OpenAIModel, Gemini, Claude, QwenWrapper, GllavaWrapper, DeepSeekWrapper

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")

def create_prompt(domain):
    # List of file names to read
    files_to_read = ["input_prompt.txt", "rules.txt", "output_prompt.txt"]
    # Initialize an empty prompt
    prompt = ""
    # Loop through each file, read its contents, and append to the prompt
    for filename in files_to_read:
        prompt_path = os.path.join(os.getcwd(), domain, "prompts", filename)
        with open(prompt_path, "r") as f:
            prompt += f.read()
            prompt += "\n"
    return prompt

def dynamic_import_output_from_text(domain):
    """
    Dynamically import the 'output_from_text' function from the domain-specific module.
    """
    try:
        # Construct the module path dynamically
        module_path = f"{domain}.utils"
        module = importlib.import_module(module_path)
        output_from_text_function = getattr(module, 'output_from_text')
        return output_from_text_function
    except ModuleNotFoundError:
        print(f"Module not found for domain: {domain}")
        sys.exit(1)
    except AttributeError:
        print(f"'output_from_text' function not found in the module: {module_path}")
        sys.exit(1)

# def batch_input(domains , skip , append  ,temperature):
#     model = VertexAIClient(project_id)
#     for domain in domains:
#         print(domain)
#         prompt = create_prompt(domain)
#         print(prompt)

#         model.batch_generate(prompt, domain , temperature, skip, append)
        

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Zero Shot prompting")
    parser.add_argument(
        '--temperature', '-t', 
        type=float, 
        default=0.0, 
        help='Temperature value for the OpenAI model (default: 0.0)'
    )
    parser.add_argument(
        '--model', '-m', 
        type=str, 
        default='gpt-4o', 
        help='OpenAI model name (default: gpt-4o)'
    )

    parser.add_argument(
        '--domains', '-d', 
        nargs='*', 
        default=['counting_locations'], 
        help='List of domains (default: ["counting_locations"])'
    )
    parser.add_argument(
        '--max_new_tokens', '-n',
        type=int,
        default=2000,
        help='Max new tokens for the OpenAI model (default: 1000)'
    )
    parser.add_argument(
        '--skip', '-s',
        type=int,
        default=0,
        help='Number of files to skip (default: 0)'
    )
    parser.add_argument(
        '--two_images', '-i',
        type=bool,
        default=False,
        help='True if each prompt has two images to compare'
    )
    args = parser.parse_args()
    temperature = args.temperature
    model_name = args.model
    domains = args.domains
    skip = args.skip
    append = (skip>0)
    if model_name == 'gpt-4o':
        model = OpenAIModel(openai_api_key, args.model, args.max_new_tokens)
    # elif model_name == 'janus':
    #     model = Janus()
    # elif model_name == 'llava':
    #     model = LLavaNext()
    # elif model_name == 'gemini':
    #     model = Gemini(gemini_api_key, args.model, args.max_new_tokens)
    elif model_name == 'o4-mini':
        model = OpenAIModel(openai_api_key, args.model, args.max_new_tokens)
    elif model_name == 'gemini':
        model = Gemini(project_id)
    elif model_name == "claude":
        model = Claude(project_id)
    elif model_name == "deepseek":
        # model = DeepSeek()
        model = DeepSeekWrapper()
    elif model_name == "qwen":
        # model = Qwen()
        model = QwenWrapper()
    elif model_name == "gllava":
        model = GllavaWrapper()
    else:
        print(f"Model {model_name} not supported")
        sys.exit(1)
    
    print(domains)
    for domain in domains:
        prompt = create_prompt(domain)+str("\n-Please provide a short and precise answer according to the given format.")+str("\n-Follow the output format strictly.")
        print(prompt)

        output_from_text = dynamic_import_output_from_text(domain)

        json_path = posixpath.join(os.getcwd(), str(domain), 'data.json')
        with open(json_path, 'r') as f:
            data = json.load(f)

        answer = []
        #count = 0
        for i in data:
            if skip > 0:
                skip -= 1
                continue
            #print(i['id'])
            image_path = []
            image_path.append(posixpath.join(os.getcwd(), str(domain), 'data', str(i['id'])))
            if args.two_images == True:
                image_path.append(posixpath.join(os.getcwd(), str(domain), 'data', str(i['id']).replace('second', 'first')))
            image_path.reverse()
            gpt_response = model.generate(prompt, image_path, temperature, args.two_images)
            gpt_response = re.sub(r'<.*>$', '', gpt_response)
            # print(gpt_response)
            # sys.exit(0)
            processed_output = output_from_text(gpt_response)
            i["gpt_response"] = gpt_response
            i["Output"] = processed_output["OUTPUT"]
            i["ERROR"] = processed_output["ERROR"]
            answer.append(i)

            """count += 1
            if count>=20:
                break"""

        json_path_write = posixpath.join(os.getcwd(), str(domain), f'answer_{model_name}.json')
        if append:
            with open(json_path_write, "r") as f:
                old_data = json.load(f)
                old_data.extend(answer)
            with open(json_path_write, "w") as f:
                json.dump(old_data, f, indent=2)
        else:
            with open(json_path_write, "w") as f:
                json.dump(answer, f, indent=2)
