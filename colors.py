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
    fg_prefix = "\033["
    suffix = "m"
    default = "\033[0m"

    red = 31
    pink = 31
    blue = 34
    teal = 36
    green = 32
    yellow = 33
    bright_yellow = 33
    purple = 35
    magenta = 35

    color_string = ""
    colors = ""

    if colors_8_bit:
        fg_prefix = "\033[38:5:"
        default = "\033[39;49m"
        red = 1
        pink = 213
        blue = 4
        teal = 6
        green = 2
        yellow = 3
        bright_yellow = 11
        purple = 5
        magenta = 163
    if custom_color:
        color_string = custom_color
    else:
        test = fg_color.lower().strip()
        match test:
            case "red":
                color_string = red
            case "pink":
                color_string = pink
            case "blue":
                color_string = blue
            case "green":
                color_string = green
            case "yellow":
                color_string = yellow
            case "bright_yellow":
                color_string = bright_yellow
            case "purple":
                color_string = purple
            case "teal":
                color_string = teal
            case "magenta":
                color_string = magenta
            case _:
                color_string = ""
        colors += f"{fg_prefix}{color_string}{suffix}"
    return f"{colors}{text}{default}"


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
