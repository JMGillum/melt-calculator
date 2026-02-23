# To-do list

This file will contain a list of features that are desired and should be added at some point in the future. They will be broken into multiple lists, based on how large of a feature it is. Each list will be organized in the order that tasks should be completed in.

## Small features

1. Change command line arguments for metal prices.
    * Use a single argument for all metal prices instead of individual arguments for each metal. This will reduce argument clutter.
    * The argument will be a string in a special format, such as: "metal_id:price;metal_id:price"

2. Allow for specifying multiple values in each of the filter arguments, such as multiple countries with the `-c` country flag.
    * Each one should be separated by a semicolon or some other character.
    * When used in conjunction, a size mismatch will be accepted, and the last value of the smaller one will be repeated.

        ``` text
        Ex:
        
        // This will search for "canada cent" and "switzerland franc"
        -c "canada;switzerland" -d "cent;franc"

        // This will search for "canada cent" and "switzerland cent"
        -c "canada; switzerland" -d "cent"
        ```

## Medium features

1. Create a package within the db package. This package will store all the SQL statements, which will be split up by what they do.
    * Create query module, update module, insert module, delete module.
    * Add functionality to db_interface to allow returning of the query, instead of executing it.
2. Improve tools for updating database in a safer way. Improve backup system.
    * Also improve addCoins script to be more user friendly. Should reduce bloat as well. Use tree class for display, perhaps.
3. Transactions for purchases. Every purchase and sale will be stored as an indivudal transaction. This will allow for reporting of gain or loss over time periods.
4. Obscurity feature.
    * Every country, denomination, value, and coin will have an obscurity value. They stack on each other. Higher obscurity values means that the item is more rare. This will allow for filtering out of rare coins.
5. Groups of coins, such as grouping all US 90% coins for each denomination. This will be able to be displayed on a per-design basis or for the whole metal composition.
6. Groups of Countries / States that make up a country. This can be used for German coins or similar. It can be split up if wanted, or displayed as the whole country / area.
7. Support for non-precious metals? (this one is iffy)

## Large features

1. Webui that can be hosted and accessed via a browser.
