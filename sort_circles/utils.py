def output_from_text(text):
    """
    Parse the text to extract the number of objects and the path.
    Splits the text by commas and removes leading and trailing whitespace from each element.
    """
    try:
        lines = text.strip().split("\n")
        path = [int(item.strip()) for item in lines[0].split(" ")]
        return {
            "OUTPUT": path,
            "ERROR": None
        }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }

import os
import json
def gold_to_output(i):
    gold_output = None
    try:
        #get directory of this file
        dir_of_file = os.path.dirname(os.path.realpath(__file__))
        #open the data file
        with open(dir_of_file + "\data.json") as f:
            data = json.load(f)
        row = data[i]
        sorted = row['Gold_output']
        output_prompt = " ".join([str(i) for i in sorted])
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }