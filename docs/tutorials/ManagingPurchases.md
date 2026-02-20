# Managing Purchases

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

This tutorial will walk through how to add and delete purchases from the database. These purchases are used to form the collection for the user.

> [!Warning]
> It is crucial to backup the database before continuing. See the tutorial in [Backups.md](./Backups.md)

This process can be done manually or with the provided script. You should read through the manual section even if using the script, as knowing what the script does can be beneficial.

## Structure

Purchase information is spread out across two tables: `purchases` and `specific_coins`. The `purchases` table stores the price, quantity, and date information for the purchases. The `specific_coins` table stores mintmark and year information for coins purchased. This information is split up, as the mintmark and mint year information is optional for the purchase.

## Manual

### Adding

1. Determine the `coin_id` of the coin:
    * The easiest way to do this is by using the main program and refining the search until only the desired coin is found.

    ``` text
    python3 main.py -S "1933 Polish 10 Zlotych"

    |
    v

    Results for '1933 Polish 10 zlotych'
    └─Poland
      └─Zloty
        └─10
          └─[1932-1939] ... 
    ```

    Then append the -i flag:

    ``` text
    python3 main.py -S "1933 Polish 10 Zlotych" -i

    |
    v

    Results for '1933 Polish 10 zlotych'
    └─Poland
      └─Zloty
        └─10
          └─pol_zloty_10_1 
    ```

    This replaced the coin information with its id.
    * The other method is to find the country id of the country for it, then the denomination id, then the value id, then find all coins with the value id, and determine which one you are interested in.
2. If you are not adding specific coin information, skip to step 4. Otherwise, determine if the specific coin information is already stored in the table (perhaps there were other coins with the same mintmark and mint year):

    ``` SQL
    SELECT * FROM specific_coins WHERE coin_id = "<coin_id>";
    ```

    * Replace `<coin_id>` with the `coin_id` from step 1.

3. If the specific coin information is already stored, take note of the value of the `id` column and skip to step 4. Otherwise, use the following query to insert the information:

    ``` SQL
    INSERT INTO specific_coins(coin_id,year,mintmark) VALUES("<coin_id>",<year>,"<mintmark>");
    ```

    * Use `NULL` for either value if you do not want it. If using `NULL` for `<mintmark>`, remove the quotes around it.

    ``` SQL
    -- Query to add a year and mintmark
    INSERT INTO specific_coins(coin_id,year,mintmark) VALUES("some_coin",1966,"a");

    -- Query to add a year and no mintmark
    INSERT INTO specific_coins(coin_id,year,mintmark) VALUES("some_coin",1966,NULL);

    -- Query to add a mintmark and no year
    INSERT INTO specific_coins(coin_id,year,mintmark) VALUES("some_coin",NULL,"a");
    ```

4. Create the entry in the `purchases` table:

    ``` SQL
    INSERT INTO purchases(coin_id,purchase_date,unit_price,purchase_quantity,specific_coin) VALUES("<coin_id>","<purchase_date>",<unit_price>,<quantity>,<specific_coin>)
    ```

    * `<coin_id>` is the coin id from step 1.
    * `<purchase_date>` is the date of the purchase, in the format "YYYY-mm-dd"
    * `<unit_price>` is the price **per coin**
    * `<quantity>` is the number of the coin purchased.
    * `<specific_coin>` is the id from step 3 for the specific coin information. If you don't have this, enter `NULL`.

### Deleting

1. Follow steps 1 and 2 of the [adding](#adding) section.

2. If no results were found from step 2 of the [adding](#adding) section, skip to step 4. Otherwise, check if other coins use the specific coin information:

    ``` SQL
    SELECT * FROM purchases WHERE specific_coin = <specific_coin>;
    ```

    * `<specific_coin>` is the specific coin id from the previous step 2.

3. Skip this step if step 2 returned any results or if you would like to keep the information stored for the future. Otherwise, delete the specific coin entry:

    ``` SQL
    DELETE FROM specific_coins WHERE id = <specific_coin>;
    ```

    * `<specific_coin>` is the specific coin id from the previous step 2.
4. Determine which purchase to delete:

    ``` SQL
    SELECT * FROM purchases where coin_id = "<coin_id>";
    ```

    * `<coin_id>` is the coin id from the previous step 1.

5. Delete the purchase entry:

    ``` SQL
    DELETE FROM purchases where purchase_id = <purchase_id>;
    ```

    * `<purchase_id>` is the value of the `purchase_id` column of the purchase you want to delete, as found in step 4.

## Automatic

Invoke the script with `main.py manage-purchases` and follow the prompts. Pass the `-d` flag to delete entries instead of adding them.
