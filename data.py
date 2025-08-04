"""
   Author: Josh Gillum              .
   Date: 3 August 2025             ":"         __ __
                                  __|___       \ V /
                                .'      '.      | |
                                |  O       \____/  |
^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~

    This file stores structures that are referenced throughout the program.
    They are updated from the database, and prevent multiple queries from having
    to be sent.

    metals -> dictionary with metal_id as keys. Stores tuples of 
    (name,price,date) for each metal except 'other'

^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~~^~
"""

metals = {}
