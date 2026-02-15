\* This tutorial assumes that the installed database is MariaDB. It may work for other databases, but it is not guaranteed. \*

# Updating the database

This tutorial will walk through how to update the database in place when a new release is available. If you would like to start fresh or do not have the database already set up, see the `CreateDatabase.md` tutorial.
> [!Warning]
> It is crucial that you backup the contents of the database before proceeding. See the `BackupDatabase.md` tutorial for how to do so.

## Database versioning

The database stores its version number in a simple table structure. The name of the table is `version`, and it contains the two columns: `major` and `minor`. There should only ever be one entry in this table, which stores the version number of the database. Each release of the database will be either minor (a change in only the minor column) or major (a change in the major column and the minor column gets set to 0). Any release that does not change the schema of the database (such as adding/removing tables or modifying their columns) will be classified as a minor release. All other releases will be major. 
> [!Tip]
> To check the version number of your database, execute the SQL query: `SELECT major,minor from version;`

### Git
The database contents are stored within SQL files that are within a git repository separate from the main project repository. To pull changes from the git repository, you must execute `git pull` from within the `database` directory. This will pull all changes. Because this project is still in development, changes may be pushed to the repository, however it may not be in a finished state yet. Changes are tested and packaged into releases to indicate that they are tested and safe to apply to the database.  
It is recommended to only pull changes whenever a new release is published, and to then checkout the release tag using: `git checkout <tag name>`. Tags indicate the state of the repository at the point of release, and guarantee that you do not have any untested changes within the directory.

## Updates

There are two methods for performing the incremental update, automatic or manual. Automatic should be preferred as it ensures that the database is updated in the correct order in the event that there are multiple pending updates. The manual method will work the same however, so it is up to you.  
All incremental updates to the database are stored within the `updates` directory inside the `database` directory. The file names follow a strict format and are used to determine what the update is for. The file names are of the format `<starting major version>_<starting minor version>_to_<end major version>_<end minor version>.sql`. Ex: `1_0_to_1_1.sql` will update from version 1.0 to 1.1. Updates may skip versions as well, ex: `1_0_to_1_2.sql`. These may be provided as a consolidation of multiple updates, and function the same as doing each of the skipped updates individually.

> [!Caution]
> Changing the file names within the `updates` directory will confuse the update script and may ruin the database. Only change the names if you are using the manual update method or you know what you are doin.

### Automatic

>[!Note]
> Is available for Linux users, via BASH. For those on Windows, use the manual method.

1. Enter the `database` directory
2. The update script should be used like so: `./update.sh <user> <database> <directory>`. Execute the script and follow its prompts.
    * The user argument specifies which user to connect to the database as.
    * The database argument specifies which database to connect to.
    * The directory argument specifies the path to the updates directory. This is optional and defaults to `./updates/` if not provided.

### Manual 

The manual method requires feeding the update scripts to the database management software by hand. This can be done interactively or by passing the name of the script. Updates must be performed sequentially and none should be skipped.

#### Interactively

1. `mariadb -u <user> -p <database name>`
2. Enter password.
3. `\. <path to update file>`
4. Repeat step three for each update.

#### Non-interactively

1. Enter the `updates` directory
2. `mariadb -u <user> -p <database name> < <path to update file>`
3. Repeat step three for each update.

In the event of error with either method, you can attempt to fix it (if you know how), or do a fresh database setup.
