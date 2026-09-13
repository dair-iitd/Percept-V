import re
import json
import os

def output_from_text(output_text):
    try:
        output_text = output_text.split('\n')
        # print(output_text)
        out_line = output_text[-1].strip()
        #print(out_line)
        if out_line == "None":
            return {
                "OUTPUT": None,
                "ERROR": None
            }
        else:
            try:
                match = re.search(r'\((-?\d+)\s*,\s*(-?\d+)\)', out_line)
                
                if match:
                    # Extract x and y values as integers
                    #print(match.group(1))
                    #print(match.group(2))
                    x, y = map(int, match.groups())
                    print(x, y)
                    return {
                        "OUTPUT": (x, y),
                        "ERROR": None
                    }
                else:
                    out_line = output_text[-1].strip()
                    match = re.search(r'\[(-?\d+),\s*(-?\d+)\]', out_line)
    
                    if match:
                        # Extract x and y values as integers
                        x, y = map(int, match.groups())
                        print(x, y)
                        return {
                            "OUTPUT": (x, y),
                            "ERROR": None
                        }
                    else:
                        return {
                            "OUTPUT": None,
                            "ERROR": "Output file should have a single tuple of integers"
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
    

def gold_to_output(i):
    gold_output = None
    try:
        #get directory of this file
        dir_of_file = os.path.dirname(os.path.realpath(__file__))
        #open the data file
        with open(dir_of_file + "\data.json") as f:
            data = json.load(f)
        row = data[i]
        gold_output = row['gold_output']    
        x = gold_output[-1][0]
        y = gold_output[-1][1]
        output_prompt = f"({x}, {y})"

    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }


# # Test the function
"""with open("./answer_deepseek.json", "r") as f:
    print(int("123"))
    data = json.load(f)
         # print(data[1])
    for i in data:
        output_text = i["gpt_response"]
        i["Output"] = output_from_text(output_text)["OUTPUT"]
        i["ERROR"] = output_from_text(output_text)["ERROR"]
        #remove OUTPUT key
        # i.pop("OUTPUT")
    
    with open("./answer_deepseek.json", "w") as f:
        json.dump(data, f, indent=4)
        print("Output saved to answer.json")"""