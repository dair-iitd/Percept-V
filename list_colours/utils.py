import re
import matplotlib.colors as mcolors


def output_from_text(text):
    #extract the number in the last line of text
    try:
        lines = text.strip().split("\n")
        lines = list(filter(None, lines))
        last_line = list(filter(None, lines[-1].split(" ")))
        colours = sorted(mcolors.CSS4_COLORS, key=lambda c: tuple(mcolors.rgb_to_hsv(mcolors.to_rgb(c))))
        #last_line = [x.lower() for x in last_line]
        answer = list()
        for x in last_line:
            word = re.sub(r'[^a-zA-Z]', '', x.lower())
            if word in colours:
                answer.append(word.lower())

        if answer:
            return {
                "OUTPUT": sorted(answer),
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
            "ERROR": str(e)
        }