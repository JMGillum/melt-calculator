from config import show_color
def printColored(text,color,custom_color=""):
    if not show_color:
        return text
    test = color.lower().strip()
    default = "\033[39;49m"
    red = "\033[38:5:1m"
    blue = "\033[38:5:4m"
    green = "\033[38:5:2m"
    color_string = ""
    if custom_color:
        color_string = custom_color
    else:
        match test:
            case "r":
                color_string = red
            case "b":
                color_string = blue
            case "g":
                color_string = green
    return f"{color_string}{text}{default}"
