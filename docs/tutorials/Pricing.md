# Pricing

> [!Note]
> This tutorial assumes that the installed database management system is MariaDB. Parts of it may work for other databases, but it is not guaranteed.

This tutorial will walk through how to update the prices of metals in the database. The purpose of this is so that accurate melt values can be calculated.

If you would like to add a new metal to the database, see the [metal section of the adding items tutorial](./AddingItems.md#metal-queries)

## Manual

This section will cover how to manually update the prices in the database. Using the provided script is recommended, however a knowlege of what it does should be helpful.

All metal prices are stored in the `metals` table

``` SQL
select * from metals;
```

``` text
+----------+-----------+---------------+------------+
| metal_id | name      | price         | price_date |
+----------+-----------+---------------+------------+
| ag       | silver    | 74.0000000000 | 2026-02-09 |
| au       | gold      | -1.0000000000 | 1000-01-01 |
| other    | unknown   | -1.0000000000 | 1000-01-01 |
| pd       | palladium | -1.0000000000 | 1000-01-01 |
| pt       | platinum  | -1.0000000000 | 1000-01-01 |
| rh       | rhodium   | -1.0000000000 | 1000-01-01 |
+----------+-----------+---------------+------------+
```

The `metal_id` and `name` columns can be used in conjunction to determine which metal the entry is for. It is recommended to refer to an entry by its `metal_id`, as this is the only column that is guaranteed to be unique in the table.

The following query will update the `price` and `price_date`:

``` SQL
UPDATE metals SET price=<price>, price_date="<date>" where metal_id="<metal_id>";
```

* `<price>` is the price you want to set for the metal.
* `<price_date>` is the date that the price was fetched on. This date must be in the format `YYYY-mm-dd`.
* `<metal_id>` is the metal id for the metal to update.

Repeat this query for each metal you want to update the price of.

## Automatic

Invoke the script with `main.py admin prices` to update the metal prices.
