# Backups

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

The provided backup script is meant to be a lightweight, customizable backup option for items in the database that are subject to change, such as purchases or custom made items. The backups are stored as SQL scripts that can be run to add the content back into a database. This is a passion project, and no guarantees can be made that the provided backup script will be 100% reliable. Because of this, it is recommended to periodically do a full backup of the database as well.

See the [official backup](https://mariadb.com/docs/server/server-usage/backup-and-restore/mariadb-backup/full-backup-and-restore-with-mariadb-backup) tutorial before continuing.

Invoke the script with `main.py admin backup`. Pass the `--help` flag to get a list of options for customizing the backup.
