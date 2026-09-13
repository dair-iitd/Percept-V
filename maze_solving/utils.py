def output_from_text(text):
    """
    Parse the text to extract the number of objects and the path.
    Splits the text by commas and removes leading and trailing whitespace from each element.
    """
    try:
        lines = text.strip().split("\n")
        if len(lines) < 2:
            out_line = lines[-1].strip()
        else:
            out_line = lines[-2].strip()
        
        path = [item.strip() for item in out_line.split(",")]
        if len(path) < 2:
            out_line = lines[-1].strip()
            path = [item.strip() for item in out_line.split(",")]

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
        path = row['path']
        output_prompt = ",".join(path)

    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }