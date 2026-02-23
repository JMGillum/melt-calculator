# Changelog

## v1.0.0 (February 27, 2026)

* Started versioning the database. From now on, database changes will be reflected in the database changelog.
* Enabled database [version 1.0](./database/changelog.md#v1.0)
* Refactored codebase to improve maintainability.
* Cleaned up python package requirements and made setup simpler.
* Added documentation, namely rewriting the install instructions and creating tutorials.
* Moved config to a static location and changed to toml file.
* Reorganized structure of arguments and how to call various scripts.
* Changed longform of -i flag from --only-coin-ids to --show-coin-ids
* Other general housekeeping.
* Bugfixes:
  * Able to search by coin id in manage-purchases
  * backup output directory

## v0.8.1 (February 6, 2026)

> [!warning]
> This update is not compatible with previous releases

* Refactored database to create a new table for storing the years that coins were available. Removed this column from the coins table.
* Improved color support: added more predefined colors and metal types are colored.
* Improved config: Added more documentation and more color configuration.
* Refactored some general purpose code into a new module that can be reused in other projects.
* Fixed issue that caused purchases to print in the wrong order. They now print sorted by date, the coin year, then mintmark.
* Added option to display fineness in permille instead of percent
* Made it easier to call the script from a bash script.
* Able to backup database into sql files.

## v0.8.0 (January 23, 2026)

> [!warning]
> This update is not compatible with previous releases

* This release refactored how alternative names are stored in the database.
* The various scripts associated with this project are all now callable from the main.py script.
  * Ex: main.py search, main.py collection manage.
* A backup feature was implemented, which can be invoked through: main.py manage backup
* Data for the following countries:
  * Guatemala
  * Iran
  * Israel
  * Liechtenstein
  * Newfoundland
  * Thailand
  * Turkey
  * United Arab Republic

## v0.7.4 (September 5, 2025)

* Data for the following countries:
  * El Salvador
  * Eritrea
  * Estonia
  * Fiji
  * Iraq
  * Lithuania
  * Mongolia

## v0.7.3 (August 29, 2025)

* Data for the following countries:
  * Afghanistan
  * Albania
  * Bermuda
  * Chile
  * Czechoslovakia
  * Ecuador

## v0.7.2 (August 22, 2025)

* Data for the following countries:
  * Bolivia
  * Brazil
  * Bulgaria
  * Burma (Myanmar)
  * China
  * Costa Rica
  * Hungary
  * Norway
  * Peru
  * Portugal
  * Romania

## v0.7.1 (August 15, 2025)

* Added US Silver Eagle
* Data for the following countries:
  * Austria
  * Belgium
  * Denmark
  * Egypt
  * Finland
  * Great Britain
  * Japan
  * The Netherlands
  * Sweden
  * Venezuela
  * Cambodia
  * Hawaii

## v0.7.0 (August 8, 2025)

* Script for adding coins to the database, as well as one for adding/deleting/backing up purchases
* Abstraction for the database so it could be changed in the future if needed
* Rewritten collection report script
* Script for updating metal prices in the database
* Windows color support
  * Note that python version 3.11.0 or greater is now required for the program to work out of the box. Python version 3.10.0 will work with the deletion of the import colorama and just_fix_windows_consoles() lines in main.py. Note that these lines are only needed for color support for windows, so those on another OS don't need them anyways.
* Data for the following countries:
  * Argentina
  * Australia
  * Colombia
  * Comoros
  * Cuba
  * Curacao
  * Cyprus
  * Greece
  * Haiti
  * Honduras
  * Hong Kong
  * Iceland
  * India
  * Ireland
  * Jamaica
  * Kuwait
  * Latvia
  * Lebanon
  * Liberia
  * Luxembourg
  * Macau
  * Paraguay
  * Poland

## v0.6.0 (August 1, 2025)

* This release is a major refactor of the codebase. All coin data was moved to a database (mariadb). Purchases have also been moved to the same database. This will make it MUCH easier to add coin data in the future, and greatly improved maintainability. 4118 less lines of project code.
* Revision of year availability of coins from France and Russia
* Data for the following countries:
  * Suriname
  * Serbia
* Improved searching to fetch country names from the database.

## v0.5.0 (July 25, 2025)

* This release has added support for searching for fraction face values via the form x-y/z, as well as x/z and x.y. Coin data for Mexico and Russia has been added, and has bullion coins from the United States.

## v0.4.3 (July 25, 2025)

* This release added documentation in the coins directory, as well as a template file for adding new country files. There is also the --no_coins and --only_coin_ids flags, which don't show coins at all and shows only the id of the coin, respectively.

## v0.4.2 (July 25, 2025)

* This release features an improved collection report script, which now prints out a tree of owned coins. It then prints out summary statistics for the whole collection, as well as on a metal type basis. This update also completed the coin data for Italy and added data for Switzerland.

## v0.4.1 (July 25, 2025)

* This release brought improvements to bullion coins. Now there is the ability to filter bullion out with --hide_bullion. Alternatively, only bullion can be showed with --only_bullion. Bullion coins now have "face values". These are different than their actual legal face values, and refer to the fraction of an ounce that they weigh. For example, a $50 gold maple has a legal face value of 50, but in this system, its face value is 1, because it is a 1 ounce coin. Thus, searching by a fractional value is now supported. The face value can be supplied either as a decimal or as x/y.

* General search performance and result quality was also improved.

## v0.4.0 (July 24, 2025)

* Introduced support for platinum and palladium coins, as well as specifying the metal values via command line.
* Fixed a bug with searching that would cause it to not find countries by name.
* Able to show coins that are only in or out of the personal collection.
* Added data on bullion from Canada, Great Britain, and South Africa.
* Completed Canada and Germany for standard issue coinage (not bullion)
* Added config file with several useful options
* Colorized output

## v0.3.0 (July 18, 2025)

* Major refactoring of the core structures. All of the collection objects have been replaced by the Tree class. Coins are stored inside the Coins class, and purchases are separate from them. Searching is also much easier. No new features, but it will be much easier to maintain and update in the future.

## v0.2.2 (July 16, 2025)

* Implemented piping of an input file

## v0.2.1 (July 16, 2025)

* Various bug fixes, including one that would print multiple trees or the entire tree after a search
* Implemented the search by string --search_string flag, which allows passing of a string via command line.
* Implemented the search by file of strings --search_file flag, which allows performing multiple searches, defined in an external file

## v0.2.0 (July 16, 2025)

* Melt-calculator has many of the desired basic functionalities. Still lacking in data. Searches can be performed via the command line using the corresponding flags.
