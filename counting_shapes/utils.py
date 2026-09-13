import json
import os
import re

"""def output_from_text(output_text):
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
            if len(out_words) != 3:
                return {
                    "OUTPUT": None,
                    "ERROR": "Output file should have a 3 words"
                }
            else:
                circ = out_words[0].split(':')
                tri = out_words[1].split(':')
                sq = out_words[2].split(':')
                if (circ[0] == 'CIRCLES' and tri[0] == 'TRIANGLES' and sq[0] == 'SQUARES'):
                    return {
                        "OUTPUT": {
                            "circles": int(circ[1]),
                            "triangles": int(tri[1]),
                            "squares": int(sq[1])
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
        }"""


def output_from_text(response):
    try:
        pattern1 = r"SQUARES:\s*(\d+)"
        pattern2 = r"TRIANGLES:\s*(\d+)"
        pattern3 = r"CIRCLES:\s*(\d+)"
        # Extract the number of circles, triangles, and squares using regex
        match1 = re.search(pattern1, response)
        match2 = re.search(pattern2, response)
        match3 = re.search(pattern3, response)
        if match1 and match2 and match3:
            circles = match3.group(1).strip()
            triangles = match2.group(1).strip()
            squares = match1.group(1).strip()
            return {
                "OUTPUT": {
                    "circles": int(circles),
                    "triangles": int(triangles),
                    "squares": int(squares)
                },
                "ERROR": None
            }
        else:
            return {
                "OUTPUT": None,
                "ERROR": "No match found"
            }

  
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": f"Unexpected error while parsing {str(e)}\n"
        }
    
"""def gold_to_output(i):
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
        output_prompt = f"CIRCLES:{circles} TRIANGLES:{triangles} SQUARES:{squares}"

    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }


# import json
# with open("./answer_vertexai.json", "r") as f:
#     data = json.load(f)
#     # print(data[1])
#     for i in data:
#         output_text = i["gpt_response"]
#         i["Output"] = output_from_text(output_text)["Output"]
#         i["ERROR"] = output_from_text(output_text)["ERROR"]
#         #remove OUTPUT key
#         i.pop("OUTPUT")
    
#     with open("./answer_vertexai.json", "w") as f:
#         json.dump(data, f, indent=4)
#         print("Output saved to answer.json")"""
