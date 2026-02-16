# Adding Items

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

This tutorial will walk through how to add custom items to the database in way that makes updating the database in the future easy. 

> [!Warning]
> It is crucial to backup the database before continuing. See the tutorial in [Backups.md](./Backups.md)

## Item structure

Data is structured into four distinct tiers that function like a tree.
1. countries: the top level tier. It stores information about the issuer of the items. Ex: "Switzerland"
2. denominations: The type of issue. It stores information about the denomination or series of the issue. Ex: "Francs"
3. face_values: The face value of the item. Ex: 10.
4. coins: Information about the actual item. 
5. coins_years: Information about which years the coin was available.

Below is a tree that demonstrates the structure.

```
Switzerland (country)
|-> Franc (denomination)
|   |-> 20 (face value)
|   |   |-> (coin)
|   |   |-> (coin)
|   |-> 100 (face value)
|   |   |-> (coin)
|-> Rappen (denomination)
|   |-> 5 (face value)
|   |   |-> (coin)   
```

A coin must originate from a face value, which must originate from a denomination, which must originate from a country.

## Queries

### Storing Queries

Create the following files to store the queries that will create the custom items:
* `custom_setup_countries.sql`
* `custom_setup_denominations.sql`
* `custom_setup_values.sql`
* `custom_setup_coins.sql`
* `custom_setup_coins_years.sql`
* `custom_purchases.sql`

> [!Note]
> All SQL queries must be ended with a semicolon ';'

> [!Note]
> You can skip any of the following steps if it already exists. You can add onto any existing items.

#### Country Queries
The following query template will add a country item to the database. This query should be placed in `custom_setup_countries.sql`.  

To create a country: `INSERT INTO countries(country_id, display_name) VALUES('<id>','<name>');`

* Replace id with a string representing the id of the country or issuer. It must be unique among all items in the country table. All the official entries use the ISO Alpha-3 codes, however you can use any unique value.
* Replace name with a string representing the name of the country that will be displayed whenever it is printed.

Along with adding the country to the countries table, information must also be added to the countries_names table. This table stores all of the names associated with the country, which enables search functionality. There is no limit to the number of names that can be associated with the country.  

To create the name association: `INSERT INTO country_names(country_id,name) VALUES('<country_id>','<name>');`

* Replace country_id with the same country id from the previous step.
* Replace name with the name associated with the country.

Create one of the queries for every name associated with the country.