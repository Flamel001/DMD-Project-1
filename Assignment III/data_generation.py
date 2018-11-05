import psycopg2
import string
import random
import time


def str_time_prop(start, end, format, prop):
    stime = time.mktime(time.strptime(start, format))
    etime = time.mktime(time.strptime(end, format))

    ptime = stime + prop * (etime - stime)

    return time.strftime(format, time.localtime(ptime))


def random_date(start, end, prop):
    return str_time_prop(start, end, '%m/%d/%Y %I:%M %p', prop)


def get_random_car_plate():
    cursor.execute('SELECT car_license_plate FROM car ORDER BY random() LIMIT 1')
    return cursor.fetchall()[0]


def get_random_customer():
    cursor.execute('SELECT username FROM customer ORDER BY random() LIMIT 1')
    return cursor.fetchall()[0]


def get_random_manager():
    cursor.execute('SELECT username FROM manager ORDER BY random() LIMIT 1')
    return cursor.fetchall()[0]


def get_random_username():
    cursor.execute('SELECT username FROM user_account ORDER BY random() LIMIT 1')
    return cursor.fetchall()[0]


def get_random_coord():
    cursor.execute('SELECT latitide, longitude FROM location ORDER BY random() LIMIT 1')
    return cursor.fetchall()[0]


def get_all_charging_station():
    cursor.execute('SELECT charging_station_id FROM charging_station')
    return cursor.fetchall()


def get_all_car_type():
    cursor.execute('SELECT car_type_id FROM car_type')
    return cursor.fetchall()


def get_all_plug():
    cursor.execute('SELECT plug_id FROM plug')
    return cursor.fetchall()


def get_all_car_orders():
    cursor.execute('SELECT car_order_id FROM car_order')
    return cursor.fetchall()


def get_all_cars():
    cursor.execute('SELECT car_license_plate FROM car')
    return cursor.fetchall()


def gen_phone_number():
    return ''.join([random.choice(string.digits) for _ in range(11)])


def gen_car_plate():
    return ''.join([random.choice(string.ascii_uppercase) for _ in range(2)]) \
           + ''.join(random.choice(string.digits) for _ in range(3))


def gen_vin():
    return ''.join([random.choice(string.ascii_uppercase + string.digits) for _ in range(17)])


connection = psycopg2.connect(database='car_sharing', host='db', port='5432', user='root', password='root')

"""LOCATION"""
cursor = connection.cursor()
street = [st.replace('\n', '') for st in open('source/street.txt', 'r')]
zipcode = [zp.replace('\n', '') for zp in open('source/zipcode.txt', 'r')]
for _ in range(100):
    cursor.execute('INSERT INTO location (latitide, longitude, country, city, street, zip_code)'
                   'VALUES (%s, %s, %s, %s, %s, %s)',
                   [round(random.uniform(59.5, 60.5), 3), round(random.uniform(29.5, 30.5), 3), 'Russia',
                    'Saint-Petersburg', random.choice(street), random.choice(zipcode)])
connection.commit()
cursor.close()

"""CAR TYPE"""
cursor = connection.cursor()
for car in open('source/car_type.txt', 'r'):
    cursor.execute('INSERT INTO car_type (brand, model) '
                   'VALUES (%s, %s)', car.split(' ', 1))
connection.commit()
cursor.close()

"""CAR"""
cursor = connection.cursor()
car_type_id = get_all_car_type()
color = ['yellow', 'red', 'black', 'white', 'brown', 'blue', 'green', 'purple']

for _ in range(20):
    cursor.execute('INSERT INTO car (car_license_plate, vin, color, car_type_id) '
                   'VALUES (%s, %s, %s, %s)', [
                       gen_car_plate(), gen_vin(), random.choice(color), random.choice(car_type_id)])
cursor.close()
connection.commit()

"""CAR PART"""
cursor = connection.cursor()
part_name = [cp for cp in open('source/car_part.txt', 'r')]
for _ in range(100):
    cursor.execute('INSERT INTO car_part (part_name, car_type_id) '
                   'VALUES (%s, %s)', [random.choice(part_name), random.choice(car_type_id)])
cursor.close()
connection.commit()

"""CAR PARTS PROVIDER"""
cursor = connection.cursor()
for cpp in open('source/car_parts_provider.txt', 'r'):
    coord = get_random_coord()
    cursor.execute('INSERT INTO car_parts_provider (name, phone_number, latitide, longitude) '
                   'VALUES (%s, %s, %s, %s)', [cpp, gen_phone_number(), coord[0], coord[1]])
cursor.close()
connection.commit()

"""USER ACCOUNT"""
cursor = connection.cursor()
for full_name in open('source/user_account.txt', 'r'):
    username = full_name.replace('\n', '').replace(' ', '').lower()
    cursor.execute('INSERT INTO user_account (username, email, full_name) '
                   'VALUES (%s, %s, %s)', [username, username + '@gmail.com', full_name])
cursor.close()
connection.commit()

"""CUSTOMER"""
cursor = connection.cursor()
for _ in range(35):
    coord = get_random_coord()
    cursor.execute('INSERT INTO customer (phone_number, home_latitide, home_longitude, username) '
                   'VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING ',
                   [gen_phone_number(), coord[0], coord[1], get_random_username()])
cursor.close()
connection.commit()

"""MANAGER"""
cursor = connection.cursor()
cursor.execute('SELECT user_account.username '
               'FROM user_account LEFT JOIN customer ON user_account.username = customer.username '
               'WHERE customer.username IS NULL')
for manager_username in cursor.fetchall():
    cursor.execute('INSERT INTO manager (username) '
                   'VALUES (%s)', [manager_username])
cursor.close()
connection.commit()

"""CHARGING STATION"""
cursor = connection.cursor()
for _ in range(10):
    coord = get_random_coord()
    cursor.execute('INSERT INTO charging_station (price, latitide, longitude) '
                   'VALUES (%s, %s, %s)', [random.randint(1, 5), coord[0], coord[1]])
cursor.close()
connection.commit()

"""CAR ORDER"""
cursor = connection.cursor()
for _ in range(1000):
    pick_up_coord = get_random_coord()
    dist_coord = get_random_coord()
    cursor.execute('INSERT INTO car_order (cost_of_ride, pick_up_latitide, pick_up_longitude,'
                   ' dist_latitide, dist_longitude, distance, trip_duration, car_license_plate,'
                   ' customer_username, manager_username, creating_time) '
                   'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)',
                   [random.randint(10, 100), pick_up_coord[0], pick_up_coord[1], dist_coord[0], dist_coord[1],
                    random.randint(5, 30), random.randint(10, 120), get_random_car_plate(), get_random_customer(),
                    get_random_manager(), random_date('1/1/2018 1:00 AM', '3/1/2018 1:00 AM', random.random())])
cursor.close()
connection.commit()

"""PLUG"""
cursor = connection.cursor()
shape = ['rectangle', 'circle', 'triangle', 'star']
for _ in range(10):
    cursor.execute('INSERT INTO plug (size, shape) '
                   'VALUES (%s, %s)', [random.randint(1, 5), random.choice(shape)])
cursor.execute('DELETE FROM plug as A USING plug as B '
               'WHERE A.plug_id < B.plug_id '
               'AND A.shape = B.shape '
               'AND A.size = B.size')
cursor.close()
connection.commit()

"""CHARGING STATION PLUG"""
cursor = connection.cursor()
charging_station_id = get_all_charging_station()
plug_id = get_all_plug()
for cs_id in charging_station_id:
    for _ in range(3):
        cursor.execute('INSERT INTO charging_station_plug (charging_station_id, plug_id, amount_of_available) '
                       'VALUES (%s, %s, %s) ON CONFLICT DO NOTHING',
                       [cs_id, random.choice(plug_id), random.randint(2, 5)])
cursor.close()
connection.commit()

"""CAR CHARGING LOG"""
cursor = connection.cursor()
car_license_plate = get_all_cars()
charging_station_id = get_all_charging_station()
plug_id = get_all_plug()
for _ in range(1000):
    cursor.execute('INSERT INTO car_charging_log (creating_time, time_of_charging,'
                   ' car_license_plate, charging_station_id, plug_id) '
                   'VALUES (%s, %s, %s, %s, %s)',
                   [random_date('1/1/2018 1:00 AM', '3/1/2018 1:00 AM', random.random()), random.randint(30, 60),
                    random.choice(car_license_plate), random.choice(charging_station_id)], random.choice(plug_id))
cursor.close()
connection.commit()

"""WORKSHOP"""
cursor = connection.cursor()
for _ in range(30):
    coord = get_random_coord()
    cursor.execute('INSERT INTO workshop (open_time, close_time, latitide, longitude) '
                   'VALUES (%s, %s, %s, %s)',
                   ['9:00 AM', '10:00 PM', coord[0], coord[1]])
cursor.close()
connection.commit()

"""PAYMENT"""
cursor = connection.cursor()
for co_id in get_all_car_orders():
    cursor.execute('INSERT INTO payment (car_order_id) '
                   'VALUES (%s)', [co_id])
cursor.close()
connection.commit()
