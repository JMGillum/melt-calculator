#   Author: Josh Gillum              .
#   Date: 10 February 2026          ":"         __ __
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
    """ Provides a method for printing colored text

    Attributes: 
        colors: Stores all of the defined colors. Each value is a tuple of (3 bit value, 8 bit value)
    """

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


    def PrintColored(text, show_color:bool=False, colors_8_bit:bool=False, fg_color:str="", custom_color:str=""):
        """Generates a string to print the text in the specified color

        Args:
            show_color: Whether the text is supposed to be colored.
            colors_8_bit: Pass True to use 8 bit colors and False to use 3 bit colors.
            fg_color: A key for the Colors.colors dictionary. Defines which color to print in
            custom_color: Ansi escape sequence for the color to print.

        Returns: String of the form <ansi_escape_colored> <text> <ansi_reset_to_default_color>
            
        """

        # Returns the text with no changes if show_color is False
        if not show_color:
            return text

        # If no color is specified, return text unaltered
        if not fg_color and not custom_color:
            return text

        index = 1 if colors_8_bit else 0 # Which index in the tuples to use

        # Ansi codes for printing colors
        prefix = ("\033[","\033[38:5:")
        suffix = ("m","m")
        default = ("\033[0m","\033[39;49m")

        color_string = ""
        ansi_string = ""

        # Uses the custom color string
        if custom_color:
            color_string = custom_color

        # fg_color was specified
        else:

            # Attempts to retrieve color from dictionary
            try: 
                color_string = Colors.colors[fg_color.lower().strip()][index]

            # Color is not defined, so return text unchanged
            except KeyError:
                return text

        # Entire ansi sequence for colored text
        ansi_string = f"{prefix[index]}{color_string}{suffix[index]}"

        return f"{ansi_string}{text}{default[index]}"


if __name__ == "__main__":

    # Fetches and validates config
    from check_config import ValidateConfig
    config, errors = ValidateConfig()

    # Some sort of errors in the config
    for error in errors:
        print(error,flush=True)
    if config is None:
        print("Config error. Aborting...")
        exit(1)

    # Prints out relevant config settings
    print(f"Current config - show_color:{config['show_color']}, colors_8_bit:{config['colors_8_bit']}")

    # Prints out every defined color, using current config.
    for color in Colors.colors.keys():
        print(Colors.PrintColored(color, config["show_color"],config["colors_8_bit"], color))
