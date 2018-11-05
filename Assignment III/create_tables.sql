DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS location (
  latitide  FLOAT,
  longitude FLOAT,
  country   VARCHAR(32),
  city      VARCHAR(32),
  street    VARCHAR(32),
  zip_code  VARCHAR(32),
  PRIMARY KEY (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS user_account (
  username  VARCHAR(32) PRIMARY KEY,
  email     VARCHAR(32),
  full_name VARCHAR(64)
);

CREATE TABLE IF NOT EXISTS manager (
  username VARCHAR(32) REFERENCES user_account (username) PRIMARY KEY
);

CREATE TABLE IF NOT EXISTS customer (
  phone_number   VARCHAR(16),
  home_latitide  FLOAT,
  home_longitude FLOAT,
  username       VARCHAR(32) REFERENCES user_account (username) PRIMARY KEY,
  FOREIGN KEY (home_latitide, home_longitude) REFERENCES location (latitide, longitude)
);


CREATE TABLE IF NOT EXISTS car_type (
  car_type_id INT PRIMARY KEY,
  brand       VARCHAR(32),
  model       VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS car_part (
  car_part_id INT PRIMARY KEY,
  part_name   VARCHAR(128),
  car_type_id INT REFERENCES car_type (car_type_id)
);

CREATE TABLE IF NOT EXISTS car_parts_provider (
  provider_id  INT PRIMARY KEY,
  name         VARCHAR(32),
  phone_number VARCHAR(16),
  latitide     FLOAT,
  longitude    FLOAT,
  FOREIGN KEY (latitide, longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS workshop (
  workshop_id INT PRIMARY KEY,
  open_time   TIME,
  close_time  TIME,
  latitide    FLOAT,
  longitude   FLOAT,
  FOREIGN KEY (latitide, longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS catalogue_workshop (
  workshop_id INT REFERENCES workshop (workshop_id),
  car_part_id INT REFERENCES car_part (car_part_id),
  PRIMARY KEY (workshop_id, car_part_id)
);

CREATE TABLE IF NOT EXISTS catalogue_provider (
  provider_id INT REFERENCES car_parts_provider (provider_id),
  car_part_id INT REFERENCES car_part (car_part_id),
  PRIMARY KEY (provider_id, car_part_id)
);

CREATE TABLE IF NOT EXISTS car (
  car_license_plate varchar(16) PRIMARY KEY,
  vin               INT UNIQUE,
  car_type_id       INT REFERENCES car_type (car_type_id)
);

CREATE TABLE IF NOT EXISTS charging_station (
  charging_station_id INT PRIMARY KEY,
  price               FLOAT,
  time_of_charging    INT,
  latitide            FLOAT,
  longitude           FLOAT,
  FOREIGN KEY (latitide, longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS plug (
  plug_id INT PRIMARY KEY,
  size    INT,
  shape   VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS charging_station_plug (
  charging_station_id INT REFERENCES charging_station (charging_station_id),
  plug_id             INT REFERENCES plug (plug_id),
  amount_of_available INT,
  PRIMARY KEY (charging_station_id, plug_id)
);

CREATE TABLE IF NOT EXISTS car_order (
  car_order_id      INT PRIMARY KEY,
  creating_time     TIMESTAMP,
  status            INT,
  cost_of_ride      INT,
  pick_up_latitide  FLOAT,
  pick_up_longitude FLOAT,
  car_license_plate VARCHAR(16) REFERENCES car (car_license_plate),
  customer_username VARCHAR(32) REFERENCES customer (username),
  manager_username  VARCHAR(32) REFERENCES manager (username),
  FOREIGN KEY (pick_up_latitide, pick_up_longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS payment (
  payment_id   INT PRIMARY KEY,
  time         TIMESTAMP,
  amount       INT,
  username     VARCHAR(32) REFERENCES customer (username),
  car_order_id INT REFERENCES car_order (car_order_id)
);

CREATE TABLE IF NOT EXISTS car_repairing_log (
  date              TIMESTAMP,
  manager_username  VARCHAR(32) REFERENCES manager (username),
  workshop_id       INT REFERENCES workshop (workshop_id),
  car_license_plate VARCHAR(16) REFERENCES car (car_license_plate),
  PRIMARY KEY (car_license_plate, date)
);

CREATE TABLE IF NOT EXISTS car_parts_order (
  car_parts_order_id    INT PRIMARY KEY,
  description           VARCHAR(512),
  status                INT,
  creating_time         TIMESTAMP,
  workshop_id           INT REFERENCES workshop (workshop_id),
  car_parts_provider_id INT REFERENCES car_parts_provider (provider_id)
);

CREATE TABLE IF NOT EXISTS car_charging_log (
  creating_time       TIMESTAMP,
  car_license_plate   VARCHAR(16) REFERENCES car (car_license_plate),
  charging_station_id INT REFERENCES charging_station (charging_station_id),
  PRIMARY KEY (creating_time, car_license_plate)
);

CREATE TABLE IF NOT EXISTS customer_issues (
  issue_id          INT PRIMARY KEY,
  status            INT,
  creating_time     TIMESTAMP,
  customer_username VARCHAR(32) REFERENCES customer (username),
  manager_username  VARCHAR(32) REFERENCES manager (username)
)





