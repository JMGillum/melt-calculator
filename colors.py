#   Author: Josh Gillum              .
#   Date: 7 February 2026           ":"         __ __
#                                  __|___       \ V /
#                                .'      '.      | |
#                                |  O       \____/  |
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
#
#    This file stores the function for printing colored text. Running this 
#    script as main will show a preview of how the colors will look.
#
#~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~


class Colors:
    """Provides a method for printing colored text"""
    # Stores all of the defined colors. Each value is a tuple of (3 bit value, 8 bit value)
    colors = {
        "blue": (34,4),
        "bright_yellow": (33,11),
        "bronze": (31,202),
        "green": (32,2),
        "lime": (32,82),
        "magenta": (35,163),
        "pink": (31,213),
        "purple": (35,5),
        "red": (31,1),
        "rose": (31,204),
        "silver": (37,231),
        "teal": (36,6),
        "yellow": (33,3),
    }


    def PrintColored(text, show_color=False, colors_8_bit=False, fg_color="", custom_color=""):
        """Generates a string to print the text in the specified color

        Args:
            show_color (): Whether the text is supposed to be colored.
            colors_8_bit (): Pass True to use 8 bit colors and False to use 3 bit colors.
            fg_color (): A key for the Colors.colors dictionary. Defines which color to print in
            custom_color (): Ansi escape sequence for the color to print.

        Returns: String of the form <ansi_escape_colored> <text> <ansi_reset_to_default_color>
            
        """
        if not show_color:
            return text
        index = 1 if colors_8_bit else 0 # Which index in the tuples to use

        # Ansi codes for printing colors
        prefix = ("\033[","\033[38:5:")
        suffix = ("m","m")
        default = ("\033[0m","\033[39;49m")

        color_string = ""
        ansi_string = ""

        if custom_color:
            color_string = custom_color
        else: # fg_color was specified
            test = fg_color.lower().strip()
            try: # Attempts to retrieve color from dictionary
                color_string = Colors.colors[test][index]
            except KeyError:
                color_string = ""
            # Entire ansi sequence for colored text
            ansi_string = f"{prefix[index]}{color_string}{suffix[index]}"
        return f"{ansi_string}{text}{default[index]}"


if __name__ == "__main__":
    for color in Colors.colors:
        print(Colors.PrintColored(color, color))
