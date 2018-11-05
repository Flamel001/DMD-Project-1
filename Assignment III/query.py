import psycopg2

connection = psycopg2.connect(database='car_sharing', host='db', port='5432', user='root', password='root')

# DATA FOR QUERY 1 BEGIN
cursor = connection.cursor()
cursor.execute(
    'INSERT INTO user_account (username, email, full_name) '
    'VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
    ['kathryn', 'kathryn@gmail.com', 'Kathryn Christian'])
cursor.execute(
    'INSERT INTO user_account (username, email, full_name) '
    'VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
    ['manager_1', 'manager_1@gmail.com', 'Deanna Richmond'])
cursor.execute(
    'INSERT INTO manager (username) '
    'VALUES (%s) ON CONFLICT DO NOTHING',
    ['manager_1'])
cursor.execute(
    'INSERT INTO location (latitide, longitude, country, city, street, zip_code) '
    'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
    [59.93863, 30.31413, 'Russian', 'Saint-Petersburg', 'Nevsky Prospect', '187021'])
cursor.execute(
    'INSERT INTO customer (home_latitide, home_longitude, username, phone_number) '
    'VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
    [59.93863, 30.31413, 'kathryn', '89501336992'])
cursor.execute(
    'INSERT INTO car_type (brand, model) '
    'VALUES (%s, %s) ON CONFLICT DO NOTHING', ['Tesla', 'Model S'])
cursor.execute(
    'INSERT INTO car (car_license_plate, vin, color, car_type_id) '
    'VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
    ['AN128', '1XP5DB9X6XD484666', 'red', 1])
cursor.execute(
    'INSERT INTO car (car_license_plate, vin, color, car_type_id) '
    'VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
    ['AN324', 'JYAVP19Y26A081761', 'red', 1])
cursor.execute(
    'INSERT INTO car (car_license_plate, vin, color, car_type_id) '
    'VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING',
    ['BN534', '1FAPP39S5JK136944', 'red', 1])
cursor.execute(
    'INSERT INTO car_order (cost_of_ride, pick_up_latitide, pick_up_longitude, car_license_plate, customer_username, manager_username) '
    'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
    [32, 59.93863, 30.31413, 'AN128', 'kathryn', 'manager_1'])
cursor.execute(
    'INSERT INTO car_order (cost_of_ride, pick_up_latitide, pick_up_longitude, car_license_plate, customer_username, manager_username) '
    'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
    [45, 59.93863, 30.31413, 'AN324', 'kathryn', 'manager_1'])
cursor.execute(
    'INSERT INTO car_order (cost_of_ride, pick_up_latitide, pick_up_longitude, car_license_plate, customer_username, manager_username) '
    'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
    [102, 59.93863, 30.31413, 'BN534', 'kathryn', 'manager_1'])
cursor.execute(
    'INSERT INTO car_order (cost_of_ride, pick_up_latitide, pick_up_longitude, car_license_plate, customer_username, manager_username) '
    'VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT DO NOTHING',
    [80, 59.93863, 30.31413, 'AN128', 'kathryn', 'manager_1'])
connection.commit()
cursor.close()
# DATA FOR QUERY 1 END

# DATA FOR QUERY 4 BEGIN
cursor = connection.cursor()
cursor.execute(
    'INSERT INTO payment (username, car_order_id) '
    'VALUES (%s, %s)', ['kathryn', 1])
cursor.execute(
    'INSERT INTO payment (username, car_order_id) '
    'VALUES (%s, %s)', ['kathryn', 2])
cursor.execute(
    'INSERT INTO payment (username, car_order_id) '
    'VALUES (%s, %s)', ['kathryn', 3])
cursor.execute(
    'INSERT INTO payment (username, car_order_id) '
    'VALUES (%s, %s)', ['kathryn', 4])
connection.commit()
cursor.close()
# DATA FOR QUERY 4 END



