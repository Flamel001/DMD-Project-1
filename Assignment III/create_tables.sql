DROP SCHEMA public CASCADE;
CREATE SCHEMA public;

CREATE TABLE IF NOT EXISTS location (
  latitide  FLOAT,
  longitude FLOAT,
  country   VARCHAR(32),
  city      VARCHAR(32),
  street    VARCHAR(64),
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
  car_type_id SERIAL PRIMARY KEY,
  brand       VARCHAR(32),
  model       VARCHAR(32)
);

CREATE TABLE IF NOT EXISTS car_part (
  car_part_id SERIAL PRIMARY KEY,
  part_name   VARCHAR(128),
  car_type_id INT REFERENCES car_type (car_type_id)
);

CREATE TABLE IF NOT EXISTS car_parts_provider (
  provider_id  SERIAL PRIMARY KEY,
  name         VARCHAR(64),
  phone_number VARCHAR(16),
  latitide     FLOAT,
  longitude    FLOAT,
  FOREIGN KEY (latitide, longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS workshop (
  workshop_id SERIAL PRIMARY KEY,
  open_time   TIME,
  close_time  TIME,
  latitide    FLOAT,
  longitude   FLOAT,
  FOREIGN KEY (latitide, longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS catalogue_workshop (
  workshop_id         INT REFERENCES workshop (workshop_id),
  car_part_id         INT REFERENCES car_part (car_part_id),
  amount_of_available INT,
  cost                FLOAT,
  PRIMARY KEY (workshop_id, car_part_id)
);

CREATE TABLE IF NOT EXISTS catalogue_provider (
  provider_id         INT REFERENCES car_parts_provider (provider_id),
  car_part_id         INT REFERENCES car_part (car_part_id),
  amount_of_available INT,
  cost                FLOAT,
  PRIMARY KEY (provider_id, car_part_id)
);

CREATE TABLE IF NOT EXISTS car (
  car_license_plate VARCHAR(16) PRIMARY KEY,
  vin               VARCHAR(128) UNIQUE,
  color             VARCHAR(16),
  car_type_id       INT REFERENCES car_type (car_type_id)
);

CREATE TABLE IF NOT EXISTS charging_station (
  charging_station_id SERIAL PRIMARY KEY,
  price               FLOAT,
  latitide            FLOAT,
  longitude           FLOAT,
  FOREIGN KEY (latitide, longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS plug (
  plug_id SERIAL PRIMARY KEY,
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
  car_order_id      SERIAL PRIMARY KEY,
  creating_time     TIMESTAMP DEFAULT current_timestamp,
  status            INT       DEFAULT 0,
  cost_of_ride      INT,
  pick_up_latitide  FLOAT,
  pick_up_longitude FLOAT,
  dist_latitide     FLOAT,
  dist_longitude    FLOAT,
  distance          FLOAT,
  trip_duration     INT,
  car_license_plate VARCHAR(16) REFERENCES car (car_license_plate) ON UPDATE CASCADE,
  customer_username VARCHAR(32) REFERENCES customer (username),
  manager_username  VARCHAR(32) REFERENCES manager (username),
  FOREIGN KEY (pick_up_latitide, pick_up_longitude) REFERENCES location (latitide, longitude),
  FOREIGN KEY (dist_latitide, dist_longitude) REFERENCES location (latitide, longitude)
);

CREATE TABLE IF NOT EXISTS payment (
  payment_id   SERIAL PRIMARY KEY,
  car_order_id INT REFERENCES car_order (car_order_id)
);

CREATE TABLE IF NOT EXISTS car_repairing_log (
  date               DATE,
  manager_username   VARCHAR(32) REFERENCES manager (username),
  workshop_id        INT REFERENCES workshop (workshop_id),
  car_license_plate  VARCHAR(16) REFERENCES car (car_license_plate) ON UPDATE CASCADE,
  broken_car_part_id INT REFERENCES car_part (car_part_id),
  PRIMARY KEY (car_license_plate, broken_car_part_id, date)
);

CREATE TABLE IF NOT EXISTS car_parts_order (
  car_parts_order_id    SERIAL PRIMARY KEY,
  description           VARCHAR(512),
  status                INT,
  creating_time         DATE,
  amount                INT,
  car_part_id           INT REFERENCES car_part (car_part_id),
  workshop_id           INT REFERENCES workshop (workshop_id),
  car_parts_provider_id INT REFERENCES car_parts_provider (provider_id)
);

CREATE TABLE IF NOT EXISTS car_charging_log (
  creating_time       TIMESTAMP,
  price               INT,
  plug_id             INT REFERENCES plug (plug_id),
  car_license_plate   VARCHAR(16) REFERENCES car (car_license_plate) ON UPDATE CASCADE,
  charging_station_id INT REFERENCES charging_station (charging_station_id),
  PRIMARY KEY (creating_time, car_license_plate)
);

CREATE TABLE IF NOT EXISTS customer_issues (
  issue_id          SERIAL PRIMARY KEY,
  status            INT,
  creating_time     TIMESTAMP,
  customer_username VARCHAR(32) REFERENCES customer (username),
  manager_username  VARCHAR(32) REFERENCES manager (username)
);