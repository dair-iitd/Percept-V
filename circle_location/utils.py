import re


def output_from_text(response):
    try:
        pattern1 = r"QUADRANT:\s*(\d+)"
        pattern2 = r"COUNT:\s*(\d+)"

        # Extract the number of nodes and edges using regex
        match1 = re.search(pattern1, response)
        match2 = re.search(pattern2, response)
        #print(match1)
        #print(match2)

        if match1 and match2:
            quad = match1.group(1).strip()
            count = match2.group(1).strip()
            #print(quad)
            #print(count)
            return {
                "OUTPUT": {
                    "Quadrant": int(quad),
                    "Count": int(count)
                },
                "ERROR": None
            }
        else:
            #print(match1)
            #print(match2)
            return {
                "OUTPUT": None,
                "ERROR": "No match found"
            }
  
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": f"Unexpected error while parsing {str(e)}\n"
        }