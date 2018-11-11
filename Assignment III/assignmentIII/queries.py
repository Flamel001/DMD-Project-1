from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.db import connection


@api_view(['GET'])
def query_1(request):
    username = request.GET.get('username', 'springsergio')
    color = request.GET.get('color', 'red')
    plate_pattern = request.GET.get('plate_pattern', '%AN%')
    date = request.GET.get('date', '2018-02-03')

    cursor = connection.cursor()
    subcursor = connection.cursor()
    result = []
    cursor.execute('SELECT DISTINCT car.car_license_plate '
                   'FROM customer, car, car_order '
                   'WHERE car_order.car_license_plate = car.car_license_plate AND '
                   'car_order.customer_username = customer.username AND '
                   'car.color = %s AND customer.username = %s AND '
                   'car.car_license_plate LIKE %s AND '
                   'car_order.creating_time::date = %s', [color, username, plate_pattern, date])
    result = [plate[0] for plate in cursor.fetchall()]
    cursor.execute('SELECT * FROM car WHERE car.car_license_plate = %s', [*result])
    result = []
    for car in cursor.fetchall():
        subcursor.execute('SELECT car_type.brand, car_type.model FROM car_type WHERE car_type.car_type_id = %s',
                          [car[3]])
        result.append({'Car license plate': car[0],
                       'color:': car[2],
                       'Car type': ' '.join(subcursor.fetchall()[0]).replace('\n', '')})
    cursor.close()
    subcursor.close()

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def query_2(request):
    date = request.GET.get('date', '2018-01-31')

    cursor = connection.cursor()
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

    cursor.close()

    return Response(result, status=status.HTTP_200_OK)


def sub_query_3(cursor, start_date, end_date, start_time, end_time):
    cursor.execute('SELECT count(*) FROM car')
    number_of_car = cursor.fetchall()[0][0]

    cursor.execute('SELECT count(DISTINCT car_license_plate) '
                   'FROM car_order '
                   'WHERE car_order.creating_time::date >= %s AND '
                   'car_order.creating_time::date <= %s AND '
                   'car_order.creating_time::time >= %s AND '
                   'car_order.creating_time::time <= %s', [start_date, end_date, start_time, end_time])
    return cursor.fetchall()[0][0] / number_of_car


@api_view(['GET'])
def query_3(request):
    start_date = request.GET.get('start_date', '2018-01-01')
    end_date = request.GET.get('end_date', '2018-01-07')

    cursor = connection.cursor()
    result = {'Morning': 0, 'Afternoon': 0, 'Evening': 0}
    morning_start = '7:00'
    morning_end = '10:00'
    afternoon_start = '12:00'
    afternoon_end = '14:00'
    evening_start = '17:00'
    evening_end = '19:00'

    result['Morning'] = '{0}%'.format(
        round(sub_query_3(cursor, start_date, end_date, morning_start, morning_end) * 100, 2))
    result['Afternoon'] = '{0}%'.format(
        round(sub_query_3(cursor, start_date, end_date, afternoon_start, afternoon_end) * 100, 2))
    result['Evening'] = '{0}%'.format(
        round(sub_query_3(cursor, start_date, end_date, evening_start, evening_end) * 100, 2))

    cursor.close()

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def query_4(request):
    username = request.GET.get('username', 'kathlyndotts')
    start_date = request.GET.get('start_date', '2018-01-01')
    end_date = request.GET.get('end_date', '2018-01-31')

    cursor = connection.cursor()
    result = []
    cursor.execute(
        'SELECT payment.payment_id, car_order.car_order_id, car_order.customer_username,'
        ' car_order.cost_of_ride, car_order.creating_time '
        'FROM payment, car_order '
        'WHERE payment.car_order_id = car_order.car_order_id AND '
        'car_order.customer_username = %s AND '
        'car_order.creating_time::date >= %s AND '
        'car_order.creating_time::date <= %s', [username, start_date, end_date])

    for row in cursor.fetchall():
        result.append({'payment_id': row[0],
                       'car_order_id': row[1],
                       'username': row[2],
                       'cost_of_ride': row[3],
                       'creating_time': row[4]})

    cursor.close()

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def query_5(request):
    date = request.GET.get('date', '2018-02-10')

    cursor = connection.cursor()
    cursor.execute('SELECT AVG(car_order.distance), AVG(car_order.trip_duration) '
                   'FROM car_order '
                   'WHERE car_order.creating_time::date = %s', [date])

    buf = cursor.fetchall()[0]
    result = {'Average distance': round(float(buf[0]), 2),
              'Average duration': round(float(buf[1]), 2)}

    cursor.close()

    return Response(result, status=status.HTTP_200_OK)


def sub_query_6(cursor, start_time, end_time, limit=3):
    cursor.execute('SELECT location.city, location.street, location.zip_code, count(*) as counter '
                   'FROM car_order, location '
                   'WHERE car_order.pick_up_latitide = location.latitide AND '
                   'car_order.pick_up_longitude = location.longitude AND '
                   'car_order.creating_time::time >= %s AND '
                   'car_order.creating_time::time <= %s '
                   'GROUP BY location.city, location.street, location.zip_code '
                   'ORDER BY counter DESC LIMIT %s', [start_time, end_time, limit])

    return cursor.fetchall()


@api_view(['GET'])
def query_6(request):
    result = {'Morning': 0, 'Afternoon': 0, 'Evening': 0}
    morning_start = '7:00'
    morning_end = '10:00'
    afternoon_start = '12:00'
    afternoon_end = '14:00'
    evening_start = '17:00'
    evening_end = '19:00'
    cursor = connection.cursor()

    result['Morning'] = [{'City:': row[0],
                          'Street': row[1],
                          'ZIP-Code': row[2],
                          'Counter:': row[3]} for row in sub_query_6(cursor, morning_start, morning_end)]
    result['Afternoon'] = [{'City:': row[0],
                            'Street': row[1],
                            'ZIP-Code': row[2],
                            'Counter:': row[3]} for row in sub_query_6(cursor, afternoon_start, afternoon_end)]
    result['Evening'] = [{'City:': row[0],
                          'Street': row[1],
                          'ZIP-Code': row[2],
                          'Counter:': row[3]} for row in sub_query_6(cursor, evening_start, evening_end)]

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def query_7(request):
    percentage = request.GET.get('percentage', 0.1)

    result = []
    cursor = connection.cursor()
    subcursor = connection.cursor()
    cursor.execute('SELECT car_order.car_license_plate, count(*) as counter '
                   'FROM car_order '
                   'GROUP BY car_order.car_license_plate '
                   'ORDER BY counter ASC '
                   'LIMIT %s * (SELECT count(*) FROM car)', [percentage])

    for row in cursor.fetchall():
        subcursor.execute(
            'SELECT car_type.brand, car_type.model FROM car, car_type '
            'WHERE car.car_license_plate = %s AND car.car_type_id = car_type.car_type_id',
            [row[0]])
        result.append({'Car license plate': row[0],
                       'Car type:': ' '.join(subcursor.fetchall()[0]).replace('\n', ''),
                       'Order counter': row[1]})

    cursor.close()
    subcursor.close()

    return Response(result, status=status.HTTP_200_OK)


def sub_query_8(cursor, username, start_date, end_date):
    cursor.execute('SELECT count(*) '
                   'FROM car_order, car_charging_log '
                   'WHERE car_order.car_license_plate = car_charging_log.car_license_plate AND '
                   'car_order.creating_time::date = car_charging_log.creating_time::date AND '
                   'car_charging_log.creating_time::date >= %s AND '
                   'car_charging_log.creating_time::date <= %s AND '
                   'car_order.customer_username = %s', [start_date, end_date, username])
    return cursor.fetchall()[0][0]


@api_view(['GET'])
def query_8(request):
    start_date = request.GET.get('start_date', '2018-01-01')
    end_date = request.GET.get('end_date', '2018-02-01')

    cursor = connection.cursor()
    result = {}
    cursor.execute('SELECT username FROM customer')

    for username in cursor.fetchall():
        result[username[0]] = sub_query_8(cursor, username[0], start_date, end_date)

    cursor.close()

    return Response(result, status=status.HTTP_200_OK)


def sub_query_9(cursor, workshop_id, start_date, end_date):
    cursor.execute(
        'SELECT car_parts_order.workshop_id, car_part.part_name, '
        'car_part.car_type_id, sum(car_parts_order.amount)/9 as amount '
        'FROM car_parts_order, car_part '
        'WHERE workshop_id = %s AND '
        'car_parts_order.car_part_id = car_part.car_part_id AND '
        'car_parts_order.creating_time >= %s AND '
        'car_parts_order.creating_time <= %s '
        'GROUP BY car_parts_order.workshop_id, car_part.part_name, car_part.car_type_id '
        'ORDER BY car_parts_order.workshop_id, amount DESC LIMIT 1', [workshop_id, start_date, end_date])
    return cursor.fetchall()[0]


@api_view(['GET'])
def query_9(request):
    start_date = request.GET.get('start_date', '2018-01-01')
    end_date = request.GET.get('end_date', '2018-03-01')

    cursor = connection.cursor()

    result = []
    cursor.execute('SELECT workshop_id FROM workshop')
    for workshop_id in cursor.fetchall():
        buf = sub_query_9(cursor, workshop_id[0], start_date, end_date)
        result.append({'Workshop_id': workshop_id[0],
                       'Part_name': buf[1].replace('\ufeff', '').replace('\n', ''),
                       'Average_per_week': buf[3]})

    cursor.close()

    return Response(result, status=status.HTTP_200_OK)


@api_view(['GET'])
def query_10(request):
    start_date = request.GET.get('start_date', '2018-01-01')
    end_date = request.GET.get('end_date', '2018-03-01')

    cursor = connection.cursor()
    result = []

    cursor.execute('SELECT car_type.brand, car_type.model, SUM(inner_query_1.sum + inner_query_3.sum)/%s as sum '
                   'FROM (SELECT inner_query_2.car_license_plate, SUM(inner_query_2.avg) '
                   'FROM (SELECT car_repairing_log.car_license_plate, '
                   'car_repairing_log.broken_car_part_id, AVG(catalogue_workshop.cost) '
                   'FROM car_repairing_log, catalogue_workshop '
                   'WHERE car_repairing_log.broken_car_part_id = catalogue_workshop.car_part_id AND '
                   'car_repairing_log.date >= %s AND car_repairing_log.date <= %s '
                   'GROUP BY car_repairing_log.car_license_plate, car_repairing_log.broken_car_part_id '
                   'ORDER BY car_repairing_log.car_license_plate,'
                   'car_repairing_log.broken_car_part_id) as inner_query_2, '
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

    for row in cursor.fetchall():
        result.append({'Car type':' '.join([row[0], row[1]]).replace('\n', ''),
                       'Cost_per_week': round(row[2], 2)})

    return Response(result, status=status.HTTP_200_OK)
