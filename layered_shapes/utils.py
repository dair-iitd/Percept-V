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
        output_text = output_text.split(':')
        # print(output_text)
        # if len(output_text) < 2:
        out_line = output_text[-1].strip()
        # else:
        #     out_line = output_text[-2].strip()
            
        try:
            path = [word.strip() for word in out_line.split(",")]

            # if len(path) >= 2:
            return {
                "OUTPUT": path,
                "ERROR": None
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
