from config import show_color
def printColored(text,color,custom_color=""):
    if not show_color:
        return text
    test = color.lower().strip()
    prefix = "\033[38:5:"
    suffix = "m"
    default = "\033[39;49m"
    red = 1
    blue = 4
    green = 2
    yellow = 3
    purple = 5
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
            case "y":
                color_string = yellow
            case "p":
                color_string = purple
        color_string = f"{prefix}{color_string}{suffix}"
    return f"{color_string}{text}{default}"
