import psycopg2

connection = psycopg2.connect(database='car_sharing', host='db', port='5432', user='root', password='root')
cursor = connection.cursor()


# -----------------------------------------------------------------------------------------------------
def query_1(username, color, plate_pattern, date):
    result = []
    cursor.execute('SELECT DISTINCT car.car_license_plate '
                   'FROM customer, car, car_order '
                   'WHERE car_order.car_license_plate = car.car_license_plate AND '
                   'car_order.customer_username = customer.username AND '
                   'car.color = %s AND customer.username = %s AND '
                   'car.car_license_plate LIKE %s AND '
                   'car_order.creating_time::date = %s', [color, username, plate_pattern, date])

    return [plate[0] for plate in cursor.fetchall()]


print(query_1('springsergio', 'red', '%AN%', '2018-02-03'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------


def query_2(date):
    result = {}
    for hour in range(0, 24):
        start = '{0}:00'.format(hour)
        end = '{0}:00'.format(hour + 1)
        cursor.execute('SELECT count(*) '
                       'FROM car_charging_log '
                       'WHERE creating_time::date = %s '
                       'AND creating_time::time > %s AND '
                       'creating_time::time < %s', [date, start, end])
        result[start + '-' + end] = cursor.fetchall()[0][0]
    return result


print(query_2('2018-01-31'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def sub_query_3(start_date, end_date, start_time, end_time):
    cursor.execute('SELECT count(*) FROM car')
    number_of_car = cursor.fetchall()[0][0]

    cursor.execute('SELECT count(DISTINCT car_license_plate) '
                   'FROM car_order '
                   'WHERE car_order.creating_time::date >= %s AND '
                   'car_order.creating_time::date <= %s AND '
                   'car_order.creating_time::time >= %s AND '
                   'car_order.creating_time::time <= %s', [start_date, end_date, start_time, end_time])
    return cursor.fetchall()[0][0] / number_of_car


def query_3(start_date, end_date):
    result = {'Morning': 0, 'Afternoon': 0, 'Evening': 0}
    morning_start = '7:00'
    morning_end = '10:00'
    afternoon_start = '12:00'
    afternoon_end = '14:00'
    evening_start = '17:00'
    evening_end = '19:00'

    result['Morning'] = '{0}%'.format(
        round(sub_query_3(start_date, end_date, morning_start, morning_end) * 100, 2))
    result['Afternoon'] = '{0}%'.format(
        round(sub_query_3(start_date, end_date, afternoon_start, afternoon_end) * 100, 2))
    result['Evening'] = '{0}%'.format(round(sub_query_3(start_date, end_date, evening_start, evening_end) * 100, 2))

    return result


print(query_3('2018-01-01', '2018-01-07'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def query_4(username, start_date, end_date):
    cursor.execute(
        'SELECT payment.payment_id, car_order.car_order_id, car_order.customer_username,'
        ' car_order.cost_of_ride, car_order.creating_time '
        'FROM payment, car_order '
        'WHERE payment.car_order_id = car_order.car_order_id AND '
        'car_order.customer_username = %s AND '
        'car_order.creating_time::date >= %s AND '
        'car_order.creating_time::date <= %s', [username, start_date, end_date])

    return cursor.fetchall()


print(query_4('kathlyndotts', '2018-01-01', '2018-01-31'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def query_5(date):
    cursor.execute('SELECT AVG(car_order.distance), AVG(car_order.trip_duration) '
                   'FROM car_order '
                   'WHERE car_order.creating_time::date = %s', [date])

    buf = cursor.fetchall()[0]
    result = {'Average distance': round(float(buf[0]), 2),
              'Average duration': round(float(buf[1]), 2)}
    return result


print(query_5('2018-02-10'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def sub_query_6(start_time, end_time, limit=3):
    cursor.execute('SELECT location.city, location.street, location.zip_code, count(*) as counter '
                   'FROM car_order, location '
                   'WHERE car_order.pick_up_latitide = location.latitide AND '
                   'car_order.pick_up_longitude = location.longitude AND '
                   'car_order.creating_time::time >= %s AND '
                   'car_order.creating_time::time <= %s '
                   'GROUP BY location.city, location.street, location.zip_code '
                   'ORDER BY counter DESC LIMIT %s', [start_time, end_time, limit])

    return cursor.fetchall()


def query_6():
    result = {'Morning': 0, 'Afternoon': 0, 'Evening': 0}
    morning_start = '7:00'
    morning_end = '10:00'
    afternoon_start = '12:00'
    afternoon_end = '14:00'
    evening_start = '17:00'
    evening_end = '19:00'

    result['Morning'] = sub_query_6(morning_start, morning_end)
    result['Afternoon'] = sub_query_6(afternoon_start, afternoon_end)
    result['Evening'] = sub_query_6(evening_start, evening_end)

    return result


print(query_6())


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def query_7(percentage):
    cursor.execute('SELECT car_order.car_license_plate, count(*) as counter '
                   'FROM car_order '
                   'GROUP BY car_order.car_license_plate '
                   'ORDER BY counter ASC '
                   'LIMIT %s * (SELECT count(*) FROM car)', [percentage])

    return cursor.fetchall()


print(query_7(0.1))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def sub_query_8(username, start_date, end_date):
    cursor.execute('SELECT count(*) '
                   'FROM car_order, car_charging_log '
                   'WHERE car_order.car_license_plate = car_charging_log.car_license_plate AND '
                   'car_order.creating_time::date = car_charging_log.creating_time::date AND '
                   'car_charging_log.creating_time::date >= %s AND '
                   'car_charging_log.creating_time::date <= %s AND '
                   'car_order.customer_username = %s', [start_date, end_date, username])
    return cursor.fetchall()[0][0]


def query_8(start_date, end_date):
    result = {}
    cursor.execute('SELECT username FROM customer')

    for username in cursor.fetchall():
        result[username[0]] = sub_query_8(username[0], start_date, end_date)

    return result


print(query_8('2018-01-01', '2018-02-01'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def sub_query_9(workshop_id, start_date, end_date):
    cursor.execute('SELECT car_parts_order.car_part_id, sum(car_parts_order.amount) as amount '
                   'FROM car_parts_order '
                   'WHERE workshop_id = %s AND '
                   'car_parts_order.creating_time >= %s AND '
                   'car_parts_order.creating_time <= %s '
                   'GROUP BY car_parts_order.workshop_id, car_parts_order.car_part_id '
                   'ORDER BY car_parts_order.workshop_id, amount DESC LIMIT 1', [workshop_id, start_date, end_date])
    return cursor.fetchall()[0]


def query_9(start_date, end_date):
    result = {}
    cursor.execute('SELECT workshop_id FROM workshop')
    for workshop_id in cursor.fetchall():
        result[workshop_id[0]] = sub_query_9(workshop_id[0], start_date, end_date)

    return result


print(query_9('2018-01-01', '2018-03-01'))


# -----------------------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------------------

def query_10(start_date, end_date):
    cursor.execute('SELECT car_type.brand, car_type.model, SUM(inner_query_1.sum + inner_query_3.sum)/%s as sum '
                   'FROM (SELECT inner_query_2.car_license_plate, SUM(inner_query_2.avg) '
                   'FROM (SELECT car_repairing_log.car_license_plate, '
                   'car_repairing_log.broken_car_part_id, AVG(catalogue_workshop.cost) '
                   'FROM car_repairing_log, catalogue_workshop '
                   'WHERE car_repairing_log.broken_car_part_id = catalogue_workshop.car_part_id AND '
                   'car_repairing_log.date >= %s AND car_repairing_log.date <= %s '
                   'GROUP BY car_repairing_log.car_license_plate, car_repairing_log.broken_car_part_id '
                   'ORDER BY car_repairing_log.car_license_plate, car_repairing_log.broken_car_part_id) as inner_query_2, '
                   'car, car_type '
                   'WHERE inner_query_2.car_license_plate = car.car_license_plate AND '
                   'car.car_type_id = car_type.car_type_id '
                   'GROUP BY inner_query_2.car_license_plate) as inner_query_1, '
                   '(SELECT car_type.brand, car_type.model, sum(car_charging_log.price) as sum '
                   'FROM car_charging_log, car, car_type '
                   'WHERE car_charging_log.car_license_plate = car.car_license_plate AND '
                   'car.car_type_id = car_type.car_type_id AND '
                   'car_charging_log.creating_time::date >= %s AND car_charging_log.creating_time::date <= %s '
                   'GROUP BY car_type.brand, car_type.model '
                   'ORDER BY sum DESC) as inner_query_3, car, car_type '
                   'WHERE inner_query_1.car_license_plate = car.car_license_plate AND '
                   'car.car_type_id = car_type.car_type_id '
                   'GROUP BY car_type.brand, car_type.model '
                   'ORDER BY sum DESC', [90, start_date, end_date, start_date, end_date])
    return cursor.fetchall()


print(query_10('2018-01-01', '2018-03-01'))
