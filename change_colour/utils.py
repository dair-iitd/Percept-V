import re


def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        pattern = r'^[^a-zA-Z0-9\s]+$'
        lines = [s for s in lines if not re.fullmatch(pattern, s)]
        quad = -1
        quad = int(re.findall(r"\b\d+\b", lines[-1])[0])

        if quad != -1:
            return {
                "OUTPUT": quad,
                "ERROR": None
            }
        else:
            return{
                "OUTPUT": None,
                "ERROR": 'Does not give correct format'
            }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)}