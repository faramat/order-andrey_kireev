import psycopg2
from any.config import *

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
                name_building VARCHAR(35),
                adress VARCHAR(35) 
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
                FOREIGN KEY (id_building) REFERENCES building (id_building) ON UPDATE CASCADE ON DELETE CASCADE
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
                FOREIGN KEY (id_unit) REFERENCES unit (id_unit) ON UPDATE CASCADE ON DELETE CASCADE
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
    # Сотрудник
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employee(
                id_employee SERIAL PRIMARY KEY,
                last_name VARCHAR(70),
                first_name VARCHAR(70),
                patronymic VARCHAR(70),
                name_mail VARCHAR(70),
                id_phone INTEGER,
                id_room INTEGER,
                FOREIGN KEY (id_phone) REFERENCES phone (id_phone) ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (id_room) REFERENCES room (id_room) ON UPDATE CASCADE ON DELETE CASCADE
            );
            '''
        )
    # Сотрудник разное
    with connection.cursor() as cursor:
        cursor.execute(
            '''
            CREATE TABLE IF NOT EXISTS employee_info(
                id_info SERIAL PRIMARY KEY,
                id_employee INTEGER,
                id_position INTEGER,
                id_unit INTEGER,
                id_department INTEGER,
                FOREIGN KEY (id_employee) REFERENCES employee (id_employee) ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (id_position) REFERENCES position (id_position) ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (id_unit) REFERENCES unit (id_unit) ON UPDATE CASCADE ON DELETE CASCADE,
                FOREIGN KEY (id_department) REFERENCES department (id_department) ON UPDATE CASCADE ON DELETE CASCADE
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