def output_from_text(output_text):
    try:
        try:
            # print(1)
            lline = output_text.split("\n")[-1].strip()
            # print(lline)
            lline = lline.split(":")[-1].strip()
            # print(lline)
            coordinates = lline.split(" ")
            # print(coordinates)
            #the list of coordinates now has in form (r,c) where r is the row and c is the column
            # i want to extract r and c and store them in a list
            coord_list = []
            for i in coordinates:
                i = i.strip("()")
                i = i.split(",")
                coord_list.append((int(i[0]), int(i[1]))
            )
            # if coord_list == ["```"]:
            #     raise Exception("Invalid output")
            return {"OUTPUT": coord_list, "ERROR": None}
        except:
            try:
                lline = output_text.split("\n")[-2]
                coordinates = lline.split(" ")
                #the list of coordinates now has in form (r,c) where r is the row and c is the column
                # i want to extract r and c and store them in a list
                coord_list = []
                for i in coordinates:
                    i = i.strip("()")
                    i = i.split(",")
                    coord_list.append((int(i[0]), int(i[1]))
                )
                return {"OUTPUT": coord_list, "ERROR": None}
            except:
                return {"OUTPUT": None, "ERROR": "Invalid output"}
    
    except Exception as e:
        return {"OUTPUT": None, "ERROR": str(e)}

 
# import json
# with open("./answer.json", "r") as f:
#     data = json.load(f)
#     # print(data[1])
#     for i in data:
#         output_text = i["gpt_response"]
#         i["Output"] = output_from_text(output_text)["OUTPUT"]
#         i["ERROR"] = output_from_text(output_text)["ERROR"]
#         #remove OUTPUT key
#         # i.pop("OUTPUT")
    
#     with open("./answer.json", "w") as f:
#         json.dump(data, f, indent=4)
#         print("Output saved to answer.json")