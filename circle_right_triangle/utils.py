import re
import json

def output_from_text(output_text):

    try:
        output_text = output_text.split('\n')
        # print(output_text)
        if len(output_text) < 2:
            out_line = output_text[-1].strip()
        else:
            out_line = output_text[-2].strip()
        
        try:
            match = re.search(r'\s*(yes|no)\s*', out_line.lower(), re.IGNORECASE)
            if match:
                return {
                    "OUTPUT": (match.group(1).capitalize() == "Yes"),
                    "ERROR": None
                }
            else:
                out_line = output_text[-1].strip()
                match = re.search(r'\s*(yes|no)\s*', out_line, re.IGNORECASE)
                if match:
                    return {
                    "OUTPUT": (match.group(1).capitalize() == "Yes"),
                    "ERROR": None
                }
                else:
                    return {
                        "OUTPUT": None,
                        "ERROR": "Output file should have last line as either 'yes' or 'no'"
                    }
        except Exception as e:
            return {
                "OUTPUT": None,
                "ERROR": f"Unexpected error while parsing {str(e)}\n"
            }
    except Exception as e:

        return {
            "OUTPUT": None,
            "ERROR": f"Unexpected error while parsing {str(e)}\n"
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
        ans = row['right']
        output_prompt = "YES" if ans else "NO"
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }


# # # Test the function
# with open("./answer.json", "r") as f:
#     data = json.load(f)
#     # print(data[1])
#     for i in data:
#         output_text = i["gpt_response"]

#         i["Output"] = output_from_text(output_text)["OUTPUT"]
#         i["ERROR"] = output_from_text(output_text)["ERROR"]
    
#     with open("./answer.json", "w") as f:
#         json.dump(data, f, indent=4)
#         print("Output saved to answer.json")