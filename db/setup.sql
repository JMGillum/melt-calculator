CREATE DATABASE coin_data;
USE coin_data;

CREATE TABLE countries (
  country_id varchar(255) PRIMARY KEY,
  name varchar(255) NOT NULL,
  alternative_name_1 varchar(255),
  alternative_name_2 varchar(255),
  alternative_name_3 varchar(255),
  alternative_name_4 varchar(255),
  alternative_name_5 varchar(255)
);

CREATE TABLE denominations (
  denomination_id varchar(255) PRIMARY KEY,
  country_id varchar(255) NOT NULL,
  FOREIGN KEY (country_id) REFERENCES countries(country_id) ON UPDATE CASCADE,
  name varchar(255) NOT NULL,
  alternative_name_1 varchar(255),
  alternative_name_2 varchar(255),
  alternative_name_3 varchar(255),
  alternative_name_4 varchar(255),
  alternative_name_5 varchar(255)
);

CREATE TABLE face_values (
  value_id varchar(255) PRIMARY KEY,
  denomination_id varchar(255) NOT NULL,
  FOREIGN KEY (denomination_id) REFERENCES denominations(denomination_id) ON UPDATE CASCADE,
  value decimal(20,10) NOT NULL,
  name varchar(255),
  alternative_name_1 varchar(255),
  alternative_name_2 varchar(255),
  alternative_name_3 varchar(255),
  alternative_name_4 varchar(255),
  alternative_name_5 varchar(255)
);

CREATE TABLE metals (
  metal_id varchar(5) PRIMARY KEY,
  name varchar(255) NOT NULL
);

CREATE TABLE tags (
  tag_id varchar(255) PRIMARY KEY,
  bullion boolean
);

CREATE TABLE coins (
  coin_id varchar(255) PRIMARY KEY,
  face_value_id varchar(255) NOT NULL,
  FOREIGN KEY (face_value_id) REFERENCES face_values(value_id) ON UPDATE CASCADE,
  gross_weight decimal(20,10) NOT NULL,
  fineness decimal(11,10) NOT NULL,
  precious_metal_weight decimal(20,10),
  years varchar(1024) NOT NULL,
  tags varchar(255),
  FOREIGN KEY (tags) REFERENCES tags(tag_id) ON UPDATE CASCADE,
  metal varchar(5) NOT NULL,
  FOREIGN KEY (metal) REFERENCES metals(metal_id) ON UPDATE CASCADE,
  name varchar(255)
);

CREATE TABLE specific_coins (
  id int PRIMARY KEY AUTO_INCREMENT,
  coin_id varchar(255) NOT NULL,
  FOREIGN KEY (coin_id) REFERENCES coins(coin_id) ON UPDATE CASCADE,
  year int,
  mintmark varchar(255)
);

CREATE TABLE purchases (
  purchase_id int PRIMARY KEY AUTO_INCREMENT,
  coin_id varchar(255) NOT NULL,
  FOREIGN KEY (coin_id) REFERENCES coins(coin_id) ON UPDATE CASCADE,
  purchase_date date NOT NULL,
  unit_price decimal(30,10) NOT NULL,
  purchase_quantity int DEFAULT 1,
  specific_coin int,
  FOREIGN KEY (specific_coin) REFERENCES specific_coins(id) ON UPDATE CASCADE
);

-- Metal types
insert into metals(metal_id,name) values("au","gold"),("ag","silver"),("pd","palladium"),("pt","platinum"),("rh","rhodium"),("other","unknown");

-- Countries
insert into countries(country_id,name,alternative_name_1) values("can","canada","canadian");
insert into countries(country_id,name,alternative_name_1,alternative_name_2,alternative_name_3) values("fra","france","french","francais","francaise");
insert into countries(country_id,name,alternative_name_1,alternative_name_2) values("deu","germany","german","deutschland");
insert into countries(country_id,name,alternative_name_1) values("gbr","great britain","british");
insert into countries(country_id,name,alternative_name_1) values("ita","italy","italian");
insert into countries(country_id,name,alternative_name_1) values("mex","mexico","mexican");
insert into countries(country_id,name,alternative_name_1) values("rus","russia","russian");
insert into countries(country_id,name,alternative_name_1,alternative_name_2,alternative_name_3,alternative_name_4,alternative_name_5) values("zaf","south africa","south african","s africa","s. africa","s african","s. african");
insert into countries(country_id,name,alternative_name_1,alternative_name_2,alternative_name_3) values("che","switzerland","swiss","helvetia","confoederatio helvetica");
insert into countries(country_id,name,alternative_name_1,alternative_name_2,alternative_name_3,alternative_name_4) values("usa","united states of america","usa","us","united states","united states america");

-- Denominations
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("can_cent","can","cent","cents");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("can_sovereign","can","sovereign","sovereigns");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("can_dollar","can","dollar","dollars");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("can_maple","can","maple","maples");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("fra_centime","fra","centime","centimes");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("fra_franc","fra","franc","francs");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("deu_pfennig","deu","pfennig","pfennigs");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("deu_mark","deu","mark","marks");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("gbr_britannia","gbr","britannia","britannias");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1,alternative_name_2) values("ita_centesimo","ita","centesimo","centesimi","centesimis");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1,alternative_name_2) values("ita_lira","ita","lira","lire","liras");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("mex_real","mex","real","reales");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("mex_escudo","mex","escudo","escudos");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("mex_centavo","mex","centavo","centavos");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("mex_peso","mex","peso","pesos");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("rus_kopek","rus","kopek","kopeks");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("rus_ruble","rus","ruble","rubles");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("zaf_krugerrand","zaf","krugerrand","krugerrands");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("che_franc","che","franc","francs");

INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("usa_cent","usa","cent","cents");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("usa_dollar","usa","dollar","dollars");
INSERT INTO denominations(denomination_id,country_id,name,alternative_name_1) values("usa_bullion","usa","bullion","bullions");

-- Values
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_cent_5","can_cent",5,"nickel","nickels");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_cent_10","can_cent",10,"dime","dimes");
INSERT INTO face_values(value_id,denomination_id,value) VALUES("can_cent_20","can_cent",20);
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_cent_25","can_cent",25,"quarter","quarters");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_cent_50","can_cent",50,"half","halves");
INSERT INTO face_values(value_id,denomination_id,value) VALUES("can_sovereign_1","can_sovereign",1);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("can_dollar_1","can_dollar",1);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("can_dollar_5","can_dollar",5);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("can_dollar_10","can_dollar",10);
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_maple_1_oz","can_maple",50,"1 oz maple","1");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_maple_fractional_1_2_oz","can_maple",20,"1/2 oz maple","1/2");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_maple_fractional_1_4_oz","can_maple",10,"1/4 oz maple","1/4");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_maple_fractional_1_10_oz","can_maple",5,"1/10 oz maple","1/10");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_maple_fractional_1_20_oz","can_maple",1,"1/20 oz maple","1/20");
INSERT INTO face_values(value_id,denomination_id,value,name,alternative_name_1) VALUES("can_maple_1_gram","can_maple",0.5,"1 gram maple","1");
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_centime_20","fra_centime",20);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_centime_50","fra_centime",50);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_1","fra_franc",1);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_2","fra_franc",2);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_5","fra_franc",5);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_10","fra_franc",10);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_20","fra_franc",20);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_50","fra_franc",50);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("fra_franc_100","fra_franc",100);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_pfennig_20","deu_pfennig",20);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_pfennig_50","deu_pfennig",50);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_mark_1","deu_mark",1);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_mark_2","deu_mark",2);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_mark_3","deu_mark",3);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_mark_5","deu_mark",5);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_mark_10","deu_mark",10);
INSERT INTO face_values(value_id,denomination_id,value) VALUES("deu_mark_20","deu_mark",20);

-- Coins
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES('can_cent_5_1','can_cent_5',1.162,0.925,0.0346,'1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910','ag');
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_5_2","can_cent_5",1.1664,0.925,0.0347,"1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_5_3","can_cent_5",1.1664,0.8,0.03,"1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_1","can_cent_10",2.324,0.925,0.0691,"1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_10_2","can_cent_10",2.3328,0.925,0.0694,"1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_10_3","can_cent_10",2.3328,0.8,0.06,"1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_20_1","can_cent_20",4.648,0.925,0.1382,"1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_25_1","can_cent_25",5.81,0.925,0.1728,"1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_25_2","can_cent_25",5.8319,0.925,0.1734,"1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_25_3","can_cent_25",5.8319,0.8,0.15,"1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_50_1","can_cent_50",11.62,0.925,0.3456,"1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_50_2","can_cent_50",11.6638,0.925,0.3469,"1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_cent_50_3","can_cent_50",11.6638,0.8,0.3,"1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_dollar_1","can_dollar_1",23.3276,0.8,0.6,"1920, 1921, 1922, 1923, 1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939, 1940, 1941, 1942, 1943, 1944, 1945, 1946, 1947, 1948, 1949, 1950, 1951, 1952, 1953, 1954, 1955, 1956, 1957, 1958, 1959, 1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_dollar_5_1","can_dollar_5",8.3591,0.9,0.2419,"1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_dollar_10_1","can_dollar_10",16.7181,0.9,0.4837,"1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("can_sovereign_1_1","can_sovereign_1",7.9881,0.917,0.2354,"1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_1_oz_1","can_maple_1_oz",31.11,0.9999,1.0,"1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","ag","silver");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_1_oz_2","can_maple_1_oz",31.11,0.9999,1.0,"1979, 1980, 1981, 1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","au","gold");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_2_oz_1","can_maple_fractional_1_2_oz",15.555,0.9999,0.5,"1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","au","gold");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_4_oz_1","can_maple_fractional_1_4_oz",7.7775,0.9999,0.25,"1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","au","gold");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_10_oz_1","can_maple_fractional_1_10_oz",3.111,0.9999,0.1,"1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","au","gold");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_20_oz_1","can_maple_fractional_1_20_oz",1.5555,0.9999,0.05,"1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","au","gold");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_1_gram_1","can_maple_1_gram",1.0,0.9999,0.03215075,"2024, 2025","au","gold");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_1_oz_3","can_maple_1_oz",31.11,0.9999,1.0,"2009, 2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","pt","platinum");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_1_oz_4","can_maple_1_oz",31.11,0.9995,1.0,"1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002","pt","platinum (old purity)");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_2_oz_2","can_maple_fractional_1_2_oz",15.555,0.9995,0.5,"1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002","pt","platinum (old purity)");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_4_oz_2","can_maple_fractional_1_4_oz",7.7775,0.9995,0.25,"1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002","pt","platinum (old purity)");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_10_oz_2","can_maple_fractional_1_10_oz",3.111,0.9995,0.1,"1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002","pt","platinum (old purity)");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_fractional_1_20_oz_2","can_maple_fractional_1_20_oz",1.5555,0.9995,0.05,"1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000, 2001, 2002","pt","platinum (old purity)");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal,name) VALUES("can_maple_1_oz_5","can_maple_1_oz",31.11,0.9995,1.0,"2005, 2006, 2009, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025","pd","palladium");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_centime_20_1","fra_centime_20",1.0,0.9,0.0289,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_centime_50_1","fra_centime_50",2.5,0.9,0.0723,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_centime_50_2","fra_centime_50",2.5,0.835,0.0671,"1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_1_1","fra_franc_1",5.0,0.9,0.1447,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_1_2","fra_franc_1",5.0,0.835,0.1342,"1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_2_1","fra_franc_2",10.0,0.9,0.2894,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_5_1","fra_franc_5",25.0,0.9,0.7234,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919, 1920","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_5_2","fra_franc_5",12.0,0.835,0.3222,"1960, 1961, 1962, 1963, 1964, 1965, 1966, 1967, 1968, 1969","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_5_3","fra_franc_5",1.6129,0.9,0.0467,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_10_1","fra_franc_10",10.0,0.68,0.2186,"1929, 1930, 1931, 1932, 1933, 1934, 1937, 1938, 1939","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_10_2","fra_franc_10",3.2258,0.9,0.0933,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_20_1","fra_franc_20",6.4516,0.9,0.1867,"1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_20_2","fra_franc_20",20.0,0.68,0.4373,"1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_50_1","fra_franc_50",16.129,0.9,0.4667,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_100_1","fra_franc_100",15.0,0.9,0.434,"1982, 1983, 1984, 1985, 1986, 1987, 1988, 1989, 1990, 1991, 1992, 1993, 1994, 1995, 1996, 1997, 1998, 1999, 2000","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_100_2","fra_franc_100",32.2581,0.9,0.9334,"1848, 1849, 1850, 1851, 1852, 1853, 1854, 1855, 1856, 1857, 1858, 1859, 1860, 1861, 1862, 1863, 1864, 1865, 1866, 1867, 1868, 1869, 1870, 1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("fra_franc_100_3","fra_franc_100",6.55,0.9,0.1895,"1929, 1930, 1931, 1932, 1933, 1934, 1935, 1936","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_pfennig_20_1","deu_pfennig_20",1.1111,0.9,0.0322,"1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_pfennig_50_1","deu_pfennig_50",2.7777,0.9,0.0804,"1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_1_1","deu_mark_1",5.5555,0.9,0.1608,"1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918, 1919","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_1_2","deu_mark_1",5.0,0.5,0.0804,"1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_2_1","deu_mark_2",11.1111,0.9,0.3215,"1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_2_2","deu_mark_2",10.0,0.5,0.1608,"1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_2_3","deu_mark_2",8.0,0.625,0.1608,"1933, 1934, 1935, 1936, 1937, 1938, 1939","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_3_1","deu_mark_3",16.6666,0.9,0.4823,"1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_3_2","deu_mark_3",15.0,0.5,0.2411,"1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_5_1","deu_mark_5",27.7777,0.9,0.8038,"1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915, 1916, 1917, 1918","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_5_2","deu_mark_5",1.9913,0.9,0.0576,"1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_5_3","deu_mark_5",25.0,0.5,0.4019,"1924, 1925, 1926, 1927, 1928, 1929, 1930, 1931, 1932, 1933","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_5_4","deu_mark_5",13.8888,0.9,0.4019,"1933, 1934, 1935, 1936, 1937, 1938, 1939","ag");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_10_1","deu_mark_10",3.9825,0.9,0.1152,"1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915","au");
INSERT INTO coins(coin_id,face_value_id,gross_weight,fineness,precious_metal_weight,years,metal) VALUES("deu_mark_20_1","deu_mark_20",7.965,0.9,0.2305,"1871, 1872, 1873, 1874, 1875, 1876, 1877, 1878, 1879, 1880, 1881, 1882, 1883, 1884, 1885, 1886, 1887, 1888, 1889, 1890, 1891, 1892, 1893, 1894, 1895, 1896, 1897, 1898, 1899, 1900, 1901, 1902, 1903, 1904, 1905, 1906, 1907, 1908, 1909, 1910, 1911, 1912, 1913, 1914, 1915","au");
