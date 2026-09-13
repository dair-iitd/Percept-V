import re

def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        last_line = list(filter(None, lines[-1].split(" ")))
        #last_line = [x.lower() for x in last_line]
        answer = []
        for x in last_line:
            word = re.sub(r'[^a-zA-Z]', '', x.lower())
            if word == 'no' or word == 'yes':
                answer.append(word)

        if answer != []:
            return {
                "OUTPUT": answer,
                "ERROR": None
            }
        else:
            return{
                "OUTPUT": None,
                "ERROR": 'Does not give yes/no answer'
            }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }