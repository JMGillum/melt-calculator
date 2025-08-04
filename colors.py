#   Author: Josh Gillum              .
#   Date: 4 August 2025             ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This file stores the function for printing colored text. Running this 
#    script as main will show a preview of how the colors will look.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

from config import show_color, colors_8_bit


def printColored(text, fg_color="", custom_color=""):
    if not show_color:
        return text
    prefix = "\033["
    suffix = "m"
    default = "\033[0m"
    colors = {
        "red": 31,
        "pink": 31,
        "blue": 34,
        "teal": 36,
        "green": 32,
        "yellow": 33,
        "bright_yellow": 33,
        "purple": 35,
        "magenta": 35,
    }

    color_string = ""
    ansi_string = ""

    if colors_8_bit:
        prefix = "\033[38:5:"
        default = "\033[39;49m"
        colors.update(red=1)
        colors.update(pink=213)
        colors.update(blue=4)
        colors.update(teal=6)
        colors.update(green=2)
        colors.update(yellow=3)
        colors.update(bright_yellow=11)
        colors.update(purple=5)
        colors.update(magenta=163)
    if custom_color:
        color_string = custom_color
    else:
        test = fg_color.lower().strip()
        try:
            color_string = colors[test]
        except KeyError:
            color_string = ""
        ansi_string = f"{prefix}{color_string}{suffix}"
    return f"{ansi_string}{text}{default}"


if __name__ == "__main__":
    colors = [
        "red",
        "pink",
        "blue",
        "teal",
        "green",
        "yellow",
        "bright_yellow",
        "purple",
        "magenta",
    ]
    for color in colors:
        print(printColored(color, color))
