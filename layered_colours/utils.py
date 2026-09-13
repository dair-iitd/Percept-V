import re

# def output_from_text(output_text):
#     try:
#         try:
#             lline = output_text.split("\n")[-1].strip()
#             shape = lline.split(":")[-1].strip()
#             word1 = lline.split(":")[0].strip().lower()
#             if word1 != "answer":
#                 raise Exception("Invalid output")
#             return {"OUTPUT": shape.lower(), "ERROR": None}
#         except:
#             try:
#                 lline = output_text.split("\n")[-2]
#                 shape = lline.split(":")[-1].strip()
#                 if shape.lower() not in ["circle", "rectangle", "triangle"]:
#                     raise Exception("Invalid output")
#                 return {"OUTPUT": shape.lower(), "ERROR": None}
#             except:
#                 return {"OUTPUT": None, "ERROR": "Invalid output"}
    
#     except Exception as e:
#         return {"OUTPUT": None, "ERROR": str(e)}


def output_from_text(output_text):

    try:
        lines = output_text.strip().split("\n")
        lines = list(filter(None, lines))
        last_line = list(filter(None, lines[-1].split(" ")))
        colours = ['black', 'gray', 'brown', 'maroon', 'red', 'coral', 'tan', 'orange', 'ivory', 'goldenrod', 'yellow', 'green', 'olive', 'turquoise', 'skyblue', 'blue', 'lavender', 'purple', 'pink', 'fuchsia']

        #last_line = [x.lower() for x in last_line]
        answer = []
        for x in last_line:
            word = re.sub(r'[^a-zA-Z]', '', x.lower())
            if word in colours:
                answer.append(word.lower())

        return {
                "OUTPUT": answer,
                "ERROR": None
        }

    except Exception as e:

        return {
            "OUTPUT": None,
            "ERROR": f"Unexpected error while parsing {str(e)}\n"
        }
