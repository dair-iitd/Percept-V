import re


def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        pattern = r'^[^a-zA-Z0-9\s]+$'
        lines = [s for s in lines if not re.fullmatch(pattern, s)]
        diff = -1
        diff = int(re.findall(r"\b\d+\b", lines[-1])[0])

        if diff != -1:
            return {
                "OUTPUT": diff,
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
        out_words = output_text[-1].split(' ')
        if len(out_words) != 1:
            return {
                "OUTPUT": None,
                "ERROR": "Output file should have only 1 word"
            }
        else:
            count = out_words[0].split(':')
            if (count[0] == 'COUNT'):
                return {
                    "OUTPUT": {
                        "vanished": int(count[1])
                    },
                    "ERROR": None
                }
            else:
                return {
                    "OUTPUT": None,
                    "ERROR": "Output format is not correct"
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
        circles = row['circles']
        triangles = row['triangles']
        squares = row['squares']
        vanished = row['vanished']
        output_prompt = f"CIRCLES:{circles} TRIANGLES:{triangles} SQUARES:{squares} VANISHED:{vanished}"

    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }"""
