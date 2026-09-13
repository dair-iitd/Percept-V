import re
import json


def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        pattern = r'^[^a-zA-Z0-9\s]+$'
        lines = [s for s in lines if not re.fullmatch(pattern, s)]
        above, below = -1, -1
        above = int(re.findall(r"\b\d+\b", lines[-1])[0])
        below = int(re.findall(r"\b\d+\b", lines[-1])[1])
        if above != -1 and below != -1:
            return {
                "OUTPUT": {
                    "num_objects_over_table": int(above),
                    "num_objects_under_table": int(below),


                },
                "ERROR": None
            }
        else:
            return{
                "OUTPUT": None,
                "ERROR": 'Does not give correct format'
            }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }

"""import json
import os

def output_from_text(output_text):
    try:
        
        output_text = output_text.split('\n')
        # print(output_text)
        num_lines = len(output_text)

        if num_lines != 1:
            return {
                "OUTPUT": None,
                "ERROR": "Output file should have a single line"
            }
        else:
            out_words = output_text[0].split(' ')
            if len(out_words) != 2:
                return {
                    "OUTPUT": None,
                    "ERROR": "Output file should have a two words"
                }
            else:
                above = out_words[0].split(':')
                below = out_words[1].split(':')
                if (above[0] != 'ABOVE' or below[0] != 'BELOW'):
                    return {
                        "OUTPUT": None,
                        "ERROR": "Output file should have format ABOVE:<number> BELOW:<number>"
                    }
                else:
                    return {
                        "OUTPUT": {
                            "num_objects_over_table": int(above[1]),
                            "num_objects_under_table": int(below[1])
                        },
                        "ERROR": None
                    }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": f"Unexpected error while parsing {str(e)}\n"
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
        num_objects_over_table = row['num_objects_over_table']
        num_objects_under_table = row['num_objects_under_table']
        output_prompt = "ABOVE:" + str(num_objects_over_table)
        output_prompt += " BELOW:" + str(num_objects_under_table)
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }"""