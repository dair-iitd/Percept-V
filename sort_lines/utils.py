def output_from_text(text):
    """
    Parse the text to extract the number of objects and the path.
    Splits the text by commas and removes leading and trailing whitespace from each element.
    """
    try:
        lines = text.strip().split("\n")
        path = [int(item.strip()) for item in lines[-1].split(" ")]
        return {
            "OUTPUT": path,
            "ERROR": None
        }
    except Exception as e:
        return {
            "OUTPUT": None,
            "ERROR": str(e)
        }

