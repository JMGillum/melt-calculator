# Adding Items

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

This tutorial will walk through how to add custom items to the database in way that makes updating the database in the future easy.

> [!Warning]
> It is crucial to backup the database before continuing. See the tutorial in [Backups.md](./Backups.md)

## Item structure

In order to add a new item to the database, its parent object must first exist. To add a coin, there must first be a face value object that represents that amount of the denomination. The face value object must have a parent denomination object, which represents the denomination or series of the object. The denomination object must have a parent country object, which represents the country or issuing authority of the coin. Thus, to add a new coin, a minimum of three other entries must be made. The advantage of this approach is a reduction in redundancy for objects that derive from a common parent. Ex:

``` text
1933-1934 Swiss 20 Franc
^-------^ ^---^ ^^ ^---^
|         |     |  |> The denomination object
|         |     |> The face value object
|         |> The country object
|> The individual coin
```

A face value object can parent multiple sets of years, a denomination object can parent multiple face values, and a country object can parent multiple denominations.

You can reuse any existing objects and add children to them as necessary.

## Storing custom items

All items belong to a series, which identifies where they came from. All of the items that ship with the repository belong to the **base** series. In order to add custom items, you need to decide on a name for the series. The series enables splitting of items during backups and other procedures, so choose a descriptive name other than **base**. The steps below will have you store queries in files. Both the queries and filenames will include `<series>`. Simply replace this (including the angle brackets) with the name of the series you have chosen. Ex if the series is *ngo*: `<series>_setup.sql` -> `ngo_setup.sql`.

> [!Note]
> To ensure portability, choose names that use only letters 'a-z', 'A-Z', numbers '0-9', underscores '_', and hyphens '-'

## Queries

The specific queries needed to create the various objects will follow. To maintain structure and order, it is recommended to follow the file naming conventions specified in each section. Some sections may require adding values to multiple different tables.

> [!Note]
> You can skip any of the following steps if it already exists. You can add onto any existing items.

> [!Note]
> Do remember that all SQL queries must be ended with a semicolon ';'. This is not optional and bad things can happen if you forget the semicolon.

> [!Note]
> Pay special attention when some values that you replace in queries are enclosed in quotes. These quotes are necessary.

It is recomomended to read all of the following sections in full before attempting any of their contents. An example that covers all of the sections will follow them.

### Country queries

This section will cover how to add a new country object to the database. The term country will be used, however it refers to any group that issued the items, whether it is a state government or a private company, for instance.

All queries in this section should be stored in the file `<series>_setup_countries.sql`

Before continuing, think about how the country can be uniquely identified. The convention for the countries in the **base** series is to use the ISO 3166-1 alpha-3 codes whenever possible. In the event that a code did not exist for the country, it was up to discretion. The code you use must be unique amongst all countries in the table. Any mention of `<country_id>` for the rest of this section is to be replaced with this code.

The query to add a country to the country table is:

``` SQL
INSERT INTO countries(country_id, display_name, series) VALUES("<country_id>", "<name>", "<series>");
```

* Replace `<name>` with the official name of the country that will be displayed.

To enable search functionality, you must create name associations to this country object that you just created. These name associations will link the name to the country object. Anytime a name is encountered, the table is searched to determine which country it belongs to, thus every name in this table must be unique. There is no limit to the number of associations you can add.

``` text
Name associations for France, which has a country_id of 'fra':
+-----------+------------+
| name      | country_id |
+-----------+------------+
| francais  | fra        |
| francaise | fra        |
| france    | fra        |
| french    | fra        |
+-----------+------------+
```

``` text
The entries for South Africa with country_id of 'zaf':
+---------------+------------+
| name          | country_id |
+---------------+------------+
| s africa      | zaf        |
| s african     | zaf        |
| s. africa     | zaf        |
| s. african    | zaf        |
| south africa  | zaf        |
| south african | zaf        |
+---------------+------------+
```

The South African entries demonstrate the downfall of abbreviations. They require many more associations, as they must cover every combination of abbreviated with unabbreviated words within the name. As a general rule of thumb, you should include a version in which a period succeeds the abbreviation, and one in which it doesn't.

The query to create a name association:

``` SQL
INSERT INTO country_names(country_id, name, series) VALUES(\"<country_id>\", \"<name>\", \"<series>\");
```

> [!Note]
> You will need multiple of this query, one for every name association. You will also need a name association for the official display name you used when creating the country object.

### Denomination queries

This section will cover how to add a new denomination object. The term 'denomination' will be used, but it represents the series of items. The **base** series made a distinction between decimal subparts of a denomination (Cents are distinct denomination from Dollars, despite a cent being 1/100th of a dollar). This can help organization and improve structure. It also made searching easier. The **base** series did things this way, but you do not have to. Choose whatever you see fit.

``` text
Using Canada as an example:
* Cent: Any coin worth less than 1 dollar or those that used the term cent on them.
* Dollar: Any coin worth one dollar or more.
* Sovereign: The gold sovereigns briefly issued.
* Maple: All of the bullion coinage.
```

All queries in this section should be stored in the file `<series>_setup_denominations.sql`

The first step in creating a denomination is to choose a unique id for it. The convention for the **base** series was to do: `<country_id>_<name>`, where coutnry_id is the country id of the parent country and name is the display name of the denomination in all lowercase characters.

The query to create a new denomination is:

``` SQL
INSERT INTO denominations(denomination_id, country_id, display_name, tags, series) VALUES("<denomination_id>","<country_id>","<display_name>","<tags>","<series");
```

* The country_id column exists to establish the relationship between this denomination object and its parent. It must be the exact same value as the `country_id` value of its parent country.
* Replace `<display_name>` with the name of the denomination that will be displayed.
* The `tags` column is currently unique among all of the objects covered in this tutorial. Its only function currently is to allow a denomination to flagged as bullion. Replace `<tags>` with `bullion` to flag it is bullion or `none` to not. By default, the bullion flag has the following consequences:
  * Changes the color that the denomination name will be printed in
  * Adds a special identifier after the name of the denomination to indicate that it is bullion.
  * Allows filtering (selecting either only bullion denominations or only non-bullion denominations).
  
Denominations require name associations to be set, exactly the same as with countries. See the [Countries](#country-queries) section for in-depth coverage of how they work and why they are necessary.

The query to create a name association is:

``` SQL
INSERT INTO denomination_names(denomination_id, name, series) VALUES("<denomination_id>", "<name>", "<series>");
```

> [!Note]
> As with the name associations for countries, this query will be repeated multiple times, once for each association. The display name must also be added as a name association.

### Face value queries

This section will cover how to create face value objects. Face values represent the nominal amount of the denomination for the coin. For example: A United States quarter dollar is classified under the *cents* denomination. The face value object for it has a value of 25, as the coin is worth 25 cents. All quarter dollars will then derive from this face value object.

All queries in this section should be stored in the file `<series>_setup_values.sql`

The first order of business for creating a face value object is to determine the id of it, referred to as the `value_id`. This id must be unique amongst all face values in the table. The convention for the **base** series is: `<denomination_id>_<value>`. Where `<denomination_id>` is the same value as the `denomination_id` of the parent. `<value>` is the nominal value of the item.

Face values support an optional display name, so there are two different queries that can be used.

Below is a comparison of how face value objects will be displayed by default.

``` text
Object A (value = 5, no display name)
displayed as: '5'

Object B (value = 5, display name = "Nickel")
displayed as: 'Nickel (5.00)'
    * The value in parentheses will always be displayed to decimal places.
```

To create a face value object with a display name:  

``` SQL
INSERT INTO face_values(value_id, denomination_id, value, display_name, series) VALUES("<value_id>", "<denomination_id>", <value>, "<display_name>", "<series>");
```

To create a face value object without a display name:  

``` SQL
INSERT INTO face_values(value_id, denomination_id, value, series) VALUES("<value_id>", "<denomination_id>", <value>, "<series>");
```

Regardless of whether you have a display name or not, `<denomination_id>` must be the exact same value as the `denomination_id` of the parent denomination. This is what establishes the relationship between the two.

> [!Note]
> There are no quotes around `<value>`. This is intentional. A decimal value is stored in this column instead of the usual string value that we have been using so far. This datatype supports 10 digits on either side of the decimal point. The **base** series writes out all 10 decimal places, even if they are all zeros, although this is not required. ex: 5.0000000000 instead of 5.

As with countries and denominations, face values with display names require name associations. See [Country queries](#country-queries) for an explanation of why and what they do. Face values differ from countries and denominations in that their names need not be unique. Any number of face values can share the same name. For example: A 10 cent coin from Canada and a 10 cent coin from the United States can both be called 'dime'.

The query to create a name association is:

``` SQL
INSERT INTO face_values_names(value_id, name, series) VALUES("<value_id>","<name>", "<series>");
```

#### Fractional values

Some items have nominal values that are a fractional amount, such as the Mexican 2.5 peso coin. To ensure optimal support, the following should be done:

* The value portion of the `value_id` should be `fractional_<whole amount>_<numerator>_<denominator>`

``` text
Examples:
Mexico 2.5 peso would be `mex_peso_fractional_2_1_2`

Russia 37.5 ruble would be `rus_ruble_fractional_37_1_2`
```

* If there is no specific display name for the item, use:
  * `<whole amount>-<numerator>/<denominator>` (the same format as the first format in both of the two examples below)
* The following name associations should be added, along with any for the display name:
  * `<whole amount>-<numerator>/<denominator>`
  * `<whole amount> <numerator>/<denominator>`
  * `<whole amount * denominator>/<denominator>`

``` text
Examples:
Russia 37.5 ruble:

37-1/2
37 1/2
75/2

Romania 12.5 leu:

12-1/2
12 1/2
25/2
```

#### Bullion values

Bullion can pose issues for values when its nominal value is effectively worthless compared to how it is normally traded / interacted with, by weight. Because of this, the **base** series followed the convention of:

* Items with a nominal face value, such as the silver maple, have the value column set to this nominal value.
* Items without a nominal face value, such as the silver krugerrand, have the value column set to the number of troy ounces of precious metal in the coin.
* The display name will be set to `<weight of precious metal in coin> <denomination name>`
* The value portion of the value_id relates to the precious metal weight of the coin.
* Name associations are created for the weight of the coin and for the weight of the coin along with its denomination.

``` text
Some examples
1 gram gold maple from Canada:
value_id = "can_maple_1_gram"
value = 0.5000000000 (this is the nominal face value)
display_name = "1 gram maple"
name associations = "1", "1 gram maple"

1/10 oz silver krugerrand:
value_id = "zaf_krugerrand_fractional_1_10_oz"
value = 0.1000000000 (this is the weight in troy ounces. They have no nominal face value)
display_name = "1/10 oz krugerrand"
name associations = "1/10", "1/10 oz krugerrand"
```

### Coin queries

This section will cover how to create coin objects. These represent the runs of coins that have common compositions or designs. The term 'coin' will be used, but it represents an issued item. When multiple coins that share a composition need to be added, a decision will have to be made, to split them or keep them consolidated.

``` text
The United States half dollar that weights 12.5g and is 90% silver as an example.

Option A, split into four separate coin objects:

* Barber half dollar
* Walking liberty half dollar
* Benjamin half dollar
* Kennedy 90% half dollar

Option B, combine into one single coin object:

* 90% half dollar.
```

There is no right or wrong approach to this, and it is up to you to decide which is appropriate given the situation. The **base** series has bias and split the United States issues, and consolidate most other issues. This was just due to personal preference however. The route of creating multiple issues is not any special process, it just requires creating more of coin objects.

All queries in this section should be stored in the file `<series>_setup_coins.sql`

Coins support an optional display name, similar to face values.

The query to create a coin object with a display name:

``` SQL
INSERT INTO coins(coin_id, face_value_id, gross_weight, fineness, precious_metal_weight, metal, name, series) VALUES("<coin_id>", "<face_value_id>", <gross_weight>, <fineness>, <precious_metal_weight>, "<metal>", "<name>", "<series>");
```

The query to create a coin object without a display name:

``` SQL
INSERT INTO coins(coin_id, face_value_id, gross_weight, fineness, precious_metal_weight, metal, series) VALUES("<coin_id>", "<face_value_id>", <gross_weight>, <fineness>, <precious_metal_weight>, "<metal>","<series>");
```

> [!Warning]
> `<gross_weight>` must be in grams and `<precious_metal_weight>` must be in troy ounces.

* The `coin_id` of each coin must be unique within the table. The convention of the **base** series is to append a counter to the end of the `value_id`, in the format `<value_id>_<counter>`. This counter starts at 1 and goes up by one for each subsequent coin with that value as a parent.
* `<value_id>` must be exactly the same as the `value_id` of the parent face value, as this is what establishes the realtionship between the two.
* `<gross_weight>` is a **decimal** value that can hold 10 digits on either side of the decimal point. It stores the weight of the coin, as it is measured on a scale. **THIS VALUE MUST BE IN GRAMS**
* `<fineness>` is a **decimal** value that can hold 1 digit to the left of the decimal point, and 10 to the right. It stores the fineness of coin (percentage of the coin that is the precious metal) as a decimal (90% -> 0.9).
* `<precious_metal_weight>` is a **decimal** value that can hold 10 digits on either side of the decimal point. It stores the actual precious metal content of the coin. This should be equivalent to `<gross_weight>` * `<fineness>`. **THIS VALUE MUST BE IN TROY OUNCES**
* `<metal>` must be exactly the same as one value in the `metal_id` column in the metal table. This table stores the various precious metals that the database knows about. See the [Metal queries](#metal-queries) section below for how to add new metals.

> [!Note]
> `SELECT * from metals;` will list the metals currently defined.

#### Years

All coin objects need to have additional rows added that state which years the coin object was minted in.

The query to associate a year with a coin:

``` SQL
INSERT INTO years(coin_id,year,series) VALUES("<coin_id>", <year>,"<series>");
```

* `<coin_id>` must be exactly the same as the `coin_id` of the coin object, as this is what links the year to the coin.
* `<year>` is an integer that stores the individual year the coin was minted.

> [!Note]
> This step can be quite tedious, as you will need one query for each year the coin was minted.

### Metal queries

This section will cover how to add new metals (precious or not) to the database. The **base** series comes with the most common precious metals already defined.

All queries in this section should be stored in the file `<series>_setup_db.sql`

The query to add a new metal is:

``` SQL
INSERT INTO metals(metal_id, name, price, price_date) VALUES("<metal_id>", "<name>", <price>, "<price_date>");
```

* `<metal_id>` must be some unique value. The convention of the **base** series is to use the periodic symbol for the element.
* `<name>` is the display name of the metal.
* `<price>` is a **decimal** value that can hold 20 digits to the left of and 10 digits to the right of the decimal point. It must be present, but you can enter -1 if you do not know the current price. This is the safe default value for when the price has not been set. It is easy to update the price later.
* `<price_date>` is a **datetime** value that stores the date on which the `price` column was set. If you set `price` to -1, enter "1000-01-01". This is the safe default value. If you set `price`, enter the current date in the form `YYYY-mm-dd`.

## Example

> [!Note]
> A script exists to create most of the queries for you, however it is not perfect, hence why you need to understand the queries so that you can double check its output. See the [script](#script) section for a walkthrough of the script.

This walkthrough will feature several examples that increase in complexity. The first example will mostly reuse **base** series objects. The amount of reuse will increase as we progress through the examples.

Each example will assume that you are connected to MariaDb interactively. Do this with `mariadb -u <user> -p <database name>`. Each example will also belong to the **tutorial** series.

> [!Note]
> SQL conditions are case insensitive, such that x = "example" will return the same results as x = "EXAMPLE"

### Example 1

This example will create a new coin object and associate years with it.

``` text
The coin for this example will have the following attributes:
country = Russia
denomination = Ruble
face value = 10
metal = platinum
gross weight = 10g
fineness = 75%
years minted = 1899-1902
name = shiny pinckett
```

1. Check if country exists and find `country_id`:

    ``` SQL
    SELECT country_id from country_names where name = "russia";
    ```

2. Step 1 told us that the `country_id` is `rus`. Check if the denomination exists and find `denomination_id`:

    ```SQL
    SELECT denomination_id from denominations where country_id = "rus" and (denomination_id = "rus_ruble" or denomination_id like "%ruble");
    ```

3. Step 2 returns the `denomination_id` of `rus_ruble`. Check if face value exists and find `value_id`:

    ``` SQL
    SELECT value_id from face_values where denomination_id = "rus_ruble" and (value = 5 or value_id = "rus_ruble_5");
    ```

4. Step 3 returns the `value_id` of `rus_ruble_5`. Check if any child coins of this face value already exists:

    ``` SQL
    SELECT coin_id from coins where face_value_id = "rus_ruble_5";
    ```

5. Step 4. returns `rus_ruble_5_1` `rus_ruble_5_2` `rus_ruble_5_3`. Which indicates that there are three child coins of our face value. To continue with the naming convention, our new coin should have the `coin_id` of `rus_ruble_5_4`.
6. Check if metal exists and find `metal_id`:

    ``` SQL
    SELECT metal_id from metals where name = "platinum";
    ```

7. Step 6 returns `pt`. Calculate precious metal weight: gross weight * fineness = 10g \* 0.75 = 7.5g = 0.24113 toz

8. Create coin object:

    ``` SQL
    INSERT INTO coins(coin_id, face_value_id, gross_weight, fineness, precious_metal_weight, metal, name, series) VALUES("rus_ruble_5_4", "rus_ruble_5", 10.0000000000, 0.7500000000, 0.2411300000, "pt", "shiny pinckett", "tutorial");
    ```

9. Create year associations for the coin:

    ``` SQL
    INSERT INTO years(coin_id,year) VALUES("rus_ruble_5_4",1899);
    INSERT INTO years(coin_id,year) VALUES("rus_ruble_5_4",1900);
    INSERT INTO years(coin_id,year) VALUES("rus_ruble_5_4",1901);
    INSERT INTO years(coin_id,year) VALUES("rus_ruble_5_4",1902);
    ```

10. Add the queries to files:
    1. Those from step 8 to `tutorial_setup_coins.sql`
    2. Those from step 9 to `tutorial_setup_coins_years.sql`

### Example 2

This example will create a bullion coin with a new metal.

``` text
The coin for this example will have the following attributes:
country = Great Britain
denomination = Britannia
tags = Bullion
face value = 2000 (nominal)
metal = Copper
precious metal weight = 3 toz
fineness = 91.7%
years minted = 2000
```

1. Perform steps 1-4 of [Example 1](#example-1) with the info of this coin. We find that:

    * `country_id` = `gbr`
    * `denomination_id` = `gbr_britannia`
    * `value_id` returns empty set, indicating that it does not exist.

2. Create new value with `value` column equal to the nominal value, and `display_name` following the [bullion naming conventions](#bullion-values)

    ``` SQL
    INSERT INTO face_values(value_id, denomination_id, value, display_name) VALUES("gbr_britannia_2000", "gbr_britannia", 2000, "3 oz britannia");
    ```

3. Check if metal exists:

    ``` SQL
    SELECT metal_id from metals where name = "copper";
    ```

4. Step 3 returns empty set, so add new metal with `metal_id` of `cu` and `name` of `copper`, and default `price` and `price_date`:

    ``` SQL
    INSERT INTO metals(metal_id, name, price, price_date, series) VALUES("cu", "copper", -1, "1000-01-01", "tutorial");
    ```

5. Calculate gross weight: 3 / 0.917 = 3.27153762268 toz = 101.755
6. Create new coin object:

    ``` SQL
    INSERT INTO coins(coin_id, face_value_id, gross_weight, fineness, precious_metal_weight, metal, series) VALUES("gbr_britannia_2000_1", "gbr_britannia_2000", 101.7550000000, 0.9170000000, 3.0000000000, "cu", "tutorial");
    ```

7. Create year associations for the coin:

    ``` SQL
    INSERT INTO years(coin_id,year) VALUES("gbr_britannia_2000_1",2000);
    ```

8. Add the queries to files:
    1. Those from step 2 to `tutorial_setup_values.sql`
    2. Those from step 4 to `tutorial_setup_db.sql`
    3. Those from step 6 to `tutorial_setup_coins.sql`
    4. Those from step 7 to `tutorial_setup_coins_years.sql`

### Example 3

This example will create a new country, denomination, fractional face value, and coin.

``` text
The coin for this example will have the following attributes:
country = West Zagafar
denomination = Dilmar
face value = 6-1/4
metal = silver
gross weight = 1.5625g
fineness = 90%
years minted = 1800-1802,1805
```

1. Repeat step 1 of [Example 1](#example-1) with the info of this coin. We find that:
    * `country_id` returns empty set, indicating that the country does not exist.
2. Check if country code `zaf` is already in use:

    ``` SQL
    SELECT * from countries where country_id like "zaf";
    ```

3. Step 2 returns `South Africa`, which indicates that the code is already in use. Repeat step 2 but replace with a new code until it returns empty set.
4. Create country object:

    ``` SQL
    INSERT INTO countries(country_id, display_name, series) VALUES("zag", "West Zagafar", "tutorial");
    ```

5. Create name associations for country:

    ``` SQL
    INSERT INTO country_names(name, country_id, series) VALUES ("West Zagafar","zag","tutorial");
    INSERT INTO country_names(name, country_id, series) VALUES ("West Zagafarian","zag","tutorial");
    INSERT INTO country_names(name, country_id, series) VALUES ("W Zagafar","zag","tutorial");
    INSERT INTO country_names(name, country_id, series) VALUES ("W Zagafarian","zag","tutorial");
    INSERT INTO country_names(name, country_id, series) VALUES ("W. Zagafar","zag","tutorial");
    INSERT INTO country_names(name, country_id, series) VALUES ("W. Zagafarian","zag","tutorial");
    ```

6. Create new denomination:

    ``` SQL
    INSERT INTO denominations(denomination_id, country_id, display_name, series) VALUES("zag_dilmar", "zag", "dilmar", "tutorial");
    ```

7. Create name associations for denomination:

    ``` SQL
    INSERT INTO denomination_names(denomination_id, name, series) VALUE("zag", "dilmar", "tutorial");
    INSERT INTO denomination_names(denomination_id, name, series) VALUE("zag", "dilmars", "tutorial");
    ```

8. Create new face value:

    ``` SQL
    INSERT INTO face_values(value_id, denomination_id, value, display_name, series) VALUE ("zag_dilmar_fractional_6_1_2", "zag_dilmar", 6.2500000000, "6-1/4", "tutorial");
    ```

9. Add name associations for face value:

    ``` SQL
    INSERT INTO face_values_names(value_id, name, series) VALUES("zag_dilmar_fractional_6_1_4", "6-1/4", "tutorial");
    INSERT INTO face_values_names(value_id, name, series) VALUES("zag_dilmar_fractional_6_1_4", "6 1/4", "tutorial");
    INSERT INTO face_values_names(value_id, name, series) VALUES("zag_dilmar_fractional_6_1_4", "25/4", "tutorial");
    ```

10. Add the queries to files:
    1. Those from step 4-5 to `tutorial_setup_countries.sql`
    2. Those from step 6-7 to `tutorial_setup_denominations.sql`
    3. Those from step 8-9 to `tutorial_setup_values.sql`
11. Perform steps 5-7, 8.3-8.4 of [Example 2](#example-2)

## Script

Bundles with the `main.py` script is a script for adding new items to the database. Invoke it with `main.py admin new-items` to enter the wizard for adding new items. Follow the on screen instructions and prompts.
