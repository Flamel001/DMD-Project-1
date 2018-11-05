import psycopg2

LENGTH = 120
connection = psycopg2.connect(database='car_sharing', host='db', port='5432', user='root', password='root')

# QUERY 1 BEGIN
cursor = connection.cursor()
cursor.execute("""
            SELECT car
            FROM customer, car_order, car
            WHERE customer.username = car_order.customer_username AND
                  car.car_license_plate = car_order.car_license_plate AND
                  car.car_license_plate LIKE %s AND
                  car.color=%s AND
                  date_trunc('day', car_order.creating_time)=date_trunc('day', current_timestamp);
            """, ['AN%', 'red'])
print('QUERY 1:\n\t',
      [raw[0] for raw in cursor.fetchall()],
      '\n', '-' * LENGTH)
cursor.close()
# QUERY 1 END

# QUERY 4 BEGIN
cursor = connection.cursor()
cursor.execute("""
            SELECT P
            FROM customer as C, payment as P
            WHERE C.username=P.username AND
                  date_trunc('month', P.time)=date_trunc('month', current_timestamp)  
            """)
print('QUERY 4:\n\t',
      [row[0] for row in cursor.fetchall()],
      '\n', '-' * LENGTH)
cursor.close()
# QUERY 4 END

