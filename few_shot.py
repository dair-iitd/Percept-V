import os
import re
import posixpath
import json
import sys
import argparse
import importlib
from typing import Any
from dotenv import load_dotenv
from model_few import OpenAIModel  , Gemini , Claude

import warnings

# Suppress all warnings
warnings.filterwarnings("ignore")

# Load environment variables from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("GOOGLE_CLOUD_PROJECT")


fields = {'change_colour' : ['num_differences'], 'circle_boxes': ['answer'], 'circle_location': ['quadrant', 'count'], 
          'circle_right_triangle': ['right'], 'colours_present':  ['colours_present'], 'comparing_size': ['Gold_output'], 
          'count_coloured_circles': ['red_circle'], 'counting_circles': ['num_objects'], 
          'counting_locations': ['num_objects_over_table', 'num_objects_under_table'], 
          'counting_shapes': ['circles', 'squares', 'triangles'], 'cross_and_knots': ['gold_output'], 
          'graph_counting': ['num_nodes', 'num_edges'], 'grid_path': ['gold_output'], 'identifying_shapes': ['Gold_output'], 
          'inside_circles': ['inside_circles'], 'layered_colours': ['colors'], 'layered_shapes': ['order'], 
          'list_colours': ['list_colours'], 'list_shapes': ['list_shapes'], 'locate_circles_colour': ['gold_output'], 
          'locate_circles_shape': ['gold_output'], 'match_outline': ['Gold_output'], 'match_shadow': ['Gold_output'], 
          'maze_solving': ['path'], 'mirror_image': ['mirror_image'], 'numbered_shapes': ['circles'], 
          'sort_circles': ['Gold_output'], 'sort_lines': ['Gold_output'], 'vanishing_objects': ['vanished'], 
          'water_image': ['water_image']}

def create_answer(domain, id):
    answer = ''
    data = {}
    answer_path = os.path.join(os.getcwd(), domain, "data.json")
    with open(answer_path, 'r') as file:
        data = json.load(file)
    raw_answer = []
    for item in data:
        if item['id'] == id:
            domain_field = fields[domain]
            for field in domain_field:
                raw_answer.append(item[field])
    if domain in ['change_colour', 'circle_boxes', 'count_coloured_circles', 'counting_circles', 'mirror_image', 'vanishing_objects', 'water_image']:
        answer += 'COUNT: ' + str(raw_answer[0])
    elif domain == 'circle_location':
        answer += 'QUADRANT: ' + str(raw_answer[0]) + ' COUNT: ' + str(raw_answer[1])
    elif domain in ['circle_right_triangle', 'inside_circles']:
        answer += 'YES' if raw_answer[0]==True else 'NO'
    elif domain in ['colours_present', 'comparing_size', 'identifying_shapes']:
        answer += 'ANSWER: '
        for ans in raw_answer[0]:
            answer += str(ans) + ', '
        answer = answer.rstrip(', ')
    elif domain == 'counting_locations':
        answer += 'ABOVE: ' + str(raw_answer[0]) + ' BELOW: ' + str(raw_answer[1])
    elif domain == 'counting_shapes':
        answer += 'CIRCLES: ' + str(raw_answer[0]) + ' TRIANGLES: ' + str(raw_answer[2]) + ' SQUARES: ' + str(raw_answer[1])
    elif domain == 'cross_and_knots':
        answer += '(' + str(raw_answer[0][0][0]) + ', ' + str(raw_answer[0][0][1]) + ')'
    elif domain == 'graph_counting':
        answer += 'NODES: ' + str(raw_answer[0]) + ' EDGES: ' + str(raw_answer[1])
    elif domain in ['grid_path', 'layered_shapes', 'list_shapes']:
        answer += 'SHAPES: '
        for ans in raw_answer[0]:
            answer += str(ans) + ', '
        answer = answer.rstrip(', ')
    elif domain in ['layered_colours', 'list_colours']:
        answer += 'COLOURS: '
        for ans in raw_answer[0]:
            answer += str(ans) + ', '
        answer = answer.rstrip(', ')
    elif domain in ['locate_circles_colour', 'locate_circles_shape']:
        for i in range(len(raw_answer[0])): 
            answer += '(' + str(raw_answer[0][0][0]) + ', ' + str(raw_answer[0][0][1]) + ') '
    elif domain in ['match_outline', 'match_shadow']:
        answer += 'ANSWER: ' + str(raw_answer[0])
    elif domain in ['maze_solving', 'sort_circles', 'sort_lines']:
        #answer += 'ANSWER: '
        for ans in raw_answer[0]:
            answer += str(ans) + ', '
        answer = answer.rstrip(', ')
    elif domain == 'numbered_shapes':
        answer += 'CIRCLES: '
        for ans in raw_answer[0]:
            answer += str(ans) + ', '
        answer = answer.rstrip(', ')
    return answer

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
    elif model_name == 'gpt-5-mini':
        model = OpenAIModel(openai_api_key, args.model, args.max_new_tokens)
    elif model_name == 'gemini':
        model = Gemini(project_id)
    elif model_name == "claude":
        model = Claude(project_id)
    else:
        print(f"Model {model_name} not supported")
        sys.exit(1)
    """elif model_name == "deepseek":
        model = DeepSeek()
    elif model_name == "qwen":
        model = Qwen()
    else:
        print(f"Model {model_name} not supported")
        sys.exit(1)
        # model = Qwen()

        model = QwenWrapper()"""
    
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
        example_image = []
        gold_answer = []
        for name in ['41.png', '91.png', '141.png']:
            if args.two_images == False:
                example_image.append(posixpath.join(os.getcwd(), str(domain), 'data', name))
                gold_answer.append(create_answer(domain, example_image[-1].split('/')[-1]))         
            else:
                example_image.append([posixpath.join(os.getcwd(), str(domain), 'data', 'first'+name), posixpath.join(os.getcwd(), str(domain), 'data', 'second'+name)])
                gold_answer.append(create_answer(domain, example_image[-1][1].split('/')[-1]))
        print(gold_answer)
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
            if image_path[0] == example_image[0]:
                continue
            gpt_response = model.generate(prompt, gold_answer, image_path, example_image, temperature, args.two_images)
            gpt_response = re.sub(r'<.*>$', '', gpt_response)
            # print(gpt_response)
            # sys.exit(0)
            processed_output = output_from_text(gpt_response)
            i["gpt_response"] = gpt_response
            i["Output"] = processed_output["OUTPUT"]
            i["ERROR"] = processed_output["ERROR"]
            answer.append(i)

            #count += 1
            #if count>=20:
            #    break

        json_path_write = posixpath.join(os.getcwd(), str(domain), f'answer_few_shot_{model_name}.json')
        if append:
            with open(json_path_write, "r") as f:
                old_data = json.load(f)
                old_data.extend(answer)
            with open(json_path_write, "w") as f:
                json.dump(old_data, f, indent=2)
        else:
            with open(json_path_write, "w") as f:
                json.dump(answer, f, indent=2)
