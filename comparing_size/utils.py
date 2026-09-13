import re

def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        last_line = list(filter(None, lines[-1].split(" ")))
        #last_line = [x.lower() for x in last_line]
        answer = []
        for x in last_line:
            word = re.sub(r'[^a-zA-Z]', '', x.lower())
            if word == 'blue' or word == 'green':
                answer.append(word)

        if answer != []:
            return {
                "OUTPUT": answer,
                "ERROR": None
            }
        else:
            return{
                "OUTPUT": None,
                "ERROR": 'Does not give answer in the correct format'
            }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }

"""import re
import json
import os

def output_from_text(response):
    # Define a regular expression pattern to match 'Row Number: Color'
    try:
        pattern = r"ANSWER:\s*(.*)"
        
        # Find all matches in the response
        match = re.search(pattern, response)
        
        if match:
            row_colors = match.group(1).strip(" \n\t*").split(" ")

        # strip whitespacce and stars from all elements in the list
            row_colors = [color.strip("*") for color in row_colors]

        # # Convert the matches into a dictionary
        # row_colors = [color for row, color in matches]
            return {
                "OUTPUT":{
                    "Gold_output": row_colors,
                    "num_objects": len(row_colors)
                },
                "ERROR": None
            }
        else:
            return {
                "OUTPUT": None,
                "ERROR": "Output not found"
            }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
def gold_to_output(i):
    gold_output = None
    try:
         #get directory of this file
        dir_of_file = os.path.dirname(os.path.realpath(__file__))
        #open the data file
        with open(dir_of_file + "\data.json") as f:
            data = json.load(f)
        row = data[i]
        gold_output = row['Gold_output']
        output_prompt = "ANSWER: "
        for i , col in enumerate(gold_output):
            output_prompt += f"{col} "
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }
"""    
# import json
# with open("./answer_vertexai.json", "r") as f:
#     data = json.load(f)
#     # print(data[1])
#     for i in data:
#         output_text = i["gpt_response"]
#         i["Output"] = output_from_text(output_text)["OUTPUT"]
#         i["ERROR"] = output_from_text(output_text)["ERROR"]
#         # remove OUTPU/ key
#         # i.pop("OUTPUT")
    
#     with open("./answer_vertexai.json", "w") as f:
#         json.dump(data, f, indent=4)
#         print("Output saved to answer.json")