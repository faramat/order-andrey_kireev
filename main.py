import psycopg2
from config import *

try:
    connection = psycopg2.connect(
        host=host,
        user=user,
        password=password,
        database = db_name
        )
    connection.autocommit = True

    with connection.cursor() as cursor:
        cursor.execute(
            '''
            SELECT version();
            '''
        )
        print(f'[INFO] Server version: {cursor.fetchone()}')
    
    # Корпус вуза
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS building(
                id_building SERIAL PRIMARY KEY,
                name_building VARCHAR(35) NOT NULL,
                adress VARCHAR(35) NOT NULL
            );
            '''
        )
    # Помещение в здании
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS room(
                id_room SERIAL PRIMARY KEY,
                id_building INTEGER,
                number_room VARCHAR(50),
                FOREIGN KEY (id_building) REFERENCES building (id_building) ON DELETE CASCADE
            );
            '''
        )
    # Должность
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS position(
                id_position SERIAL PRIMARY KEY,
                name_position VARCHAR(100)
            );
            '''
        )
    # Подразделение
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS unit(
                id_unit SERIAL PRIMARY KEY,
                name_unit VARCHAR(150)
            );
            '''
        )
    # Отдел
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS department(
                id_department SERIAL PRIMARY KEY,
                id_unit INTEGER,
                name_department VARCHAR(100),
                FOREIGN KEY (id_unit) REFERENCES unit (id_unit) ON DELETE CASCADE
            );
            '''
        )
    # Номера
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS phone(
                id_phone SERIAL PRIMARY KEY,
                number_phone VARCHAR(8),
                ext_phone VARCHAR(4)
            );
            '''
        )










except Exception as _ex:
    # в случае сбоя подключения будет выведено сообщение в STDOUT
    print('[INFO] Error while working with PostgreSQL: ', _ex)
finally:
    if connection:
        connection.close()
        print('[INFO] PostgreSQL connection closed')