#!/bin/bash
mv test_setup_db.sql temp
touch test_setup_db.sql
touch test_setup_countries.sql
touch test_setup_denominations.sql
touch test_setup_values.sql
touch test_setup_coins.sql

cat test_setup_countries.sql >> setup_countries.sql
cat test_setup_denominations.sql >> setup_denominations.sql
cat test_setup_values.sql >> setup_values.sql
cat test_setup_coins.sql >> setup_coins.sql

rm -rf test_*.sql
mv temp test_setup_db.sql
