import re

def output_from_text(response):
    try:
        pattern1 = r"NODES:\s*(\d+)"
        pattern2 = r"EDGES:\s*(\d+)"

        # Extract the number of nodes and edges using regex
        match1 = re.search(pattern1, response)
        match2 = re.search(pattern2, response)

        if match1 and match2:
            num_nodes = match1.group(1).strip()
            num_edges = match2.group(1).strip()
            return {
                "OUTPUT": {
                    "num_nodes": int(num_nodes),
                    "num_edges": int(num_edges)
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
        num_nodes = row['num_nodes']
        num_edges = row['num_edges']
        output_prompt = f"NODES:{num_nodes} EDGES:{num_edges}"

    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }
    
    return {
        "OUTPUT": output_prompt,
        "ERROR": None
    }


