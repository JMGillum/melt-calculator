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
  nickname varchar(255),
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
  FOREIGN KEY (metal) REFERENCES metals(metal_id) ON UPDATE CASCADE
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

INSERT INTO denominations(denomination_id,country_id,name,alternative_name) values("fra_centime","fra","centime","centimes");
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
