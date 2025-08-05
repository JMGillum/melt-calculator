#!/bin/bash
touch test_setup_countries.sql
touch test_setup_denominations.sql
touch test_setup_values.sql
touch tests_setup_coins.sql
> test_setup.sql
cat test_setup_db.sql >> test_setup.sql
cat test_setup_countries.sql >> test_setup.sql
cat test_setup_denominations.sql >> test_setup.sql
cat test_setup_values.sql >> test_setup.sql
cat test_setup_coins.sql >> test_setup.sql
