This readme functions as documentation for the Coins class and associated data.

The Coins class is stored in coins.py, and serves as an access point for all the data on coins.
Data for the coins is stored in separate files, one per country. These files should be named something unique
that identifies the country, so they are typically named <country name>.py, with underscores instead of spaces. They should also be all lowecase.

    Ex: United States -> united_states.py

Within each country file, several variables are necessary. These are: 
* `coins` of type dict 
* `values` of type dict
* `denominations` of type dict
* `coins_reverse_build` of type dict 
* <metal>_coins of type list for each metal type that is defined in the program.
* * Currently silver,gold,platinum, and palladium

coins is to be filled with objects of type Node, with Node.data being a CoinData object representing the
coin. These are Node objects so that purchases can be linked as child nodes of the coins later. See the documentation on the CoinData object (coinData.py) for information on the values used by CoinData.
The key for each value needs to be unique across all countries, so it is helpful to prefix the key with the country's name. 

Ex: Canadian nickel could have key 'canada_nickel_1'

values is a dictionary of NamedList objects that represent all of the iterations of a face value for a coin. The key should describe the face value as a whole, so something like 'canada_nickel' would be appropriate. Note that these must be unique across all countries.
The value stored here is a NamedList object, see namedList.py for more information. Basically, it requires a name as the first value, and a list of strings as the second value. There is a third optional argument, which a string containing a face value to use for sorting. This is useful if the coin does not have a face value or its name is not an integer.
The name of the NamedList can also be an AlternativeNames object (see AlternativeNames.py for more information).
This object takes a string as the main name, and a list of alternative name strings.

    Ex: "canada_nickel": NamedList(AlternativeNames("Nickel",["Nickels","5"]),["canada_nickel_1","canada_nickel_2","canada_nickel_3"],"5")

    Using this example: the primary name of the coin is "Nickel", but "Nickels" and "5" are also equivalent (useful for searching)
    It stores three iterations of the nickel:
        "canada_nickel_1"
        "canada_nickel_2"
        "canada_nickel_3"
    And it has a sort name of "5". This means that it is treated as if the name was "5" for the purpose of sorting. (Necessary to keep coins sorted by face value)

denominations needs to be dictionary storing unique keys and values that represent all the face values of the denomination. Like with the values dictionary, these values are NamedList objects, which can have an AlternativeNames object as the name.

    Ex: "canada_cent": NamedList(AN("Cent",["Cents"]), ["canada_nickel","canada_dime","canada_cents_20","canada_quarter","canada_half"]),


These three variables need to be manually updated whenever changes occur. The next few can be updated using the helper.py script. 

coins_reverse_build is a dictionary with a key for every key in the coins dictionary. The value for these keys is a tuple of the form (value,denomination,country). These are used for building a tree from a coin.

<metal_coins> is a list of keys in the coins dict that are of that metal type.
    
    Ex: "canada_nickel_1" is a silver coin, so inside of silver_coins would be the entry "canada_nickel_1"

even if a country doesn't have coins of a particular metal type, the list for the metal type must still be present, it will just be empty.

See helper.py for instructions on how to update these values easily

Whenever a new country is created, values within coins.py must be updated. The first is to add an import statement at the top of the file. It should be of the form:
    `import coins.<country_name> as <country_name`
    Ex: import coins.switzerland as switzerland
Then, the countries_list list must be updated to also include this new country name.
Finally, the countries dictionary must be updated with the key being the country name, and the value being a named list with the name being the proper country name and a list of the keys corresponding to the country's denominations.

If only a new denomination is added, just the list of denominations needs to be updated

Finally, a value in search.py must be added. This is an AlternativeNames object for the country's name (needed for searching)
in countryNames() within search.py, add a line of the form:
    `<country_name> = AlternativeNames("<proper_name>",[<alternative_names>])`
then in the return statement's list, add the country_name variable

This should be everything needed to update the coin data!






