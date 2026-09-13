import json
import os
import re

def output_from_text(output_text):
    try:
        
        lines = output_text.strip().split("\n")
        lines = list(filter(None, lines))
        last_line = list(filter(None, lines[-1].split(" ")))

        answer = []
        for x in last_line:
            word = re.sub(r'[^a-zA-Z]', '', x.lower())
            if word != 'answer':
                answer.append(word)
        if answer != []:
            return {
                "OUTPUT": answer,
                "ERROR": None
            }
        else:
            return{
                "OUTPUT": None,
                "ERROR": 'Does not give answer in correct format'
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
        gold_output = row['num_objects']
        output_prompt = "COUNT:" + str(gold_output)
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }