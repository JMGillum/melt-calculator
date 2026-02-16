# Creating the database

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

This tutorial will walk through how to setup the database with the provided data. This will not cover installing the the database management system, refer to the provider for that. 

> [!Note]
> This method will work to update the database to a new version, however an incrmental update will be more efficient. See the tutorial in [UpdateDatabase.md](./UpdateDatabase.md) and follow it if possible.

> [!Warning]
> If updating from a previous version, it is crucial to backup the database before continuing. At the very least, backup the purchases table as all data will be lost during this process. See the tutorial in [Backups.md](./Backups.md)

There are two ways to setup the database, automatic and manual. The automatic method is preferred as it handles the ordering for you, however doing it manually will perform the same function.

### Automatic

1. Enter the `database` directory
2. The script should be used like so `./db.sh <user> <database> <directory>`. Execute the script and follow its prompts.
    * The user argument specifies which user to connect to the database as.
    * The database argument specifies which database to connect to.
    * The directory argument specifies the path to the updates directory. This is optional and defaults to `./` if not provided.

### Manual

The manual method requires feeding the various files to the database management software by hand. This can be done interactively or by passing the name of the file. The files are all located within the `database` directory and must be passed in the following exact order:

1. `setup_db.sql`: Stores the queries that creates the tables in the database.
2. `setup_countries.sql`: Stores information about countries.
3. `setup_denominations.sql`: Stores information about denominations.
4. `setup_values.sql`: Stores information about face values of denominations.
5. `setup_coins.sql`: Stores information about series of coins of the various face values.
6. `setup_coins_years.sql`: Stores what years each of the coins in `setup_coins.sql` were available.
7. `setup_purchases.sql`: Will not ship with the repository. This file is optional and stores purchases made. It is generated through the use of the program.
8. Any files for custom items. See the tutorial in [AddingItems.md](./AddingItems.md) if you would like to add your own custom items.

#### Interactively

1. `mariadb -u <user> -p <database name>`
2. Enter password.
3. `\. <path to file>`
4. Repeat step three for each update.

#### Non-interactively

1. `mariadb -u <user> -p <database name> < <path to file>`
2. Repeat for each file.