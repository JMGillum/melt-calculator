# Creating the database

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

This tutorial will walk through how to setup the database with the provided data. This will not cover installing the the database management system, refer to the provider for that.

> [!Note]
> This method will work to update the database to a new version, however an incrmental update will be more efficient. See the tutorial in [UpdateDatabase.md](./UpdateDatabase.md) and follow it if possible.

> [!Warning]
> If updating from a previous version, it is crucial to backup the database before continuing. At the very least, backup the purchases table as all data will be lost during this process. See the tutorial in [Backups.md](./Backups.md)

There are two ways to setup the database, automatic and manual. The automatic method is preferred as it handles the ordering for you, however doing it manually will perform the same function.

## Automatic

1. Run the provided script:

    ``` SHELL
    python3 main.py admin setup-db --help
    ```

    * This will provide a list of the supported arguments
    * The most important argument is the `--order` parameter. This specifies which order the series will be loaded in. You must always load the `base` series first.
    * This method does not drop any tables except within the `setup.sql` of the `base series`. Thus you can load one series, then load another at another time. This method also allows flexibility for which of the optional series you would like.


## Manual

The manual method requires feeding the various files to the database management software by hand. This can be done interactively or by passing the name of the file.
Each series belongs is stored within its own directory within the `database/data` directory and must be passed in the following exact order:

1. `setup.sql`: Stores the queries that creates the tables in the database.
2. `countries.sql`: Stores information about countries.
3. `denominations.sql`: Stores information about denominations.
4. `values.sql`: Stores information about face values of denominations.
5. `coins.sql`: Stores information about series of coins of the various face values.
6. `years.sql`: Stores what years each of the coins in `coins.sql` were available.
7. `purchases.sql`: Will not ship with the repository. This file is optional and stores purchases made. It is generated through the use of the program.
8. Any files for custom items. See the tutorial in [AddingItems.md](./AddingItems.md) if you would like to add your own custom items.

> [!Warning]
> The base series must always be loaded first, as this series contains the database schema

### Interactively

1. `mariadb -u <user> -p <database name>`
2. Enter password.
3. `\. <path to file>`
4. Repeat step three for each update.

### Non-interactively

1. `mariadb -u <user> -p <database name> < <path to file>`
2. Repeat for each file.
