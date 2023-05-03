import psycopg2
from config import *



def sql_start():
    try:
        global connection
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
        return False
    finally:
        if connection:
            print('[INFO] PostgreSQL connection closed')
            return True

# Поиск в бд по фамилии
def search_surname(data):
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
            SELECT count(*) FROM employee WHERE last_name='{data['surname']}';
            '''
        )
        response = cursor.fetchone()
    return(response)
# Поиск в бд по имени
def search_name(data):
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
            SELECT count(*) FROM employee WHERE first_name='{data['name']}';
            '''
        )
        response = cursor.fetchone()
    return(response)
# Поиск в бд сотрудника
def search_employee(data):
    if data['surname'] and data['name'] and data['patronymic']: #111
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE last_name = 
                '{data['surname']}' AND first_name = '{data['name']}' AND patronymic = '{data['patronymic']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False 
    elif data['surname'] and data['name'] and data['patronymic'] == None: #110
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE last_name = 
                '{data['surname']}' AND first_name = '{data['name']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False
    elif data['surname'] and data['name'] == None and data['patronymic']: #101
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE last_name = 
                '{data['surname']}' AND patronymic = '{data['patronymic']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False
    elif data['surname'] and data['name'] == None and data['patronymic'] == None: #100
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE last_name = 
                '{data['surname']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False
    elif data['surname'] == None and data['name'] and data['patronymic']: #011
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE first_name = '{data['name']}' 
                AND patronymic = '{data['patronymic']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False
    elif data['surname'] == None and data['name']  and data['patronymic'] == None: #010
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE first_name = '{data['name']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False
    elif data['surname'] == None and data['name'] == None and data['patronymic']: #001
        with connection.cursor() as cursor:
            cursor.execute(
                f'''
                SELECT id_employee,name_mail,id_phone,id_room FROM employee WHERE patronymic = '{data['patronymic']}';
                '''
            )
            try:
                response = cursor.fetchall()[0]
                return get_info(response)
            except:
                return False
    else: 
        return False

def get_info(response):
    info = {
        'surname' : '',
        'name' : '',
        'patronymic' : '',
        'unit' : '',
        'department' : '',
        'position' : '',
        'mail' : '', 
        'phone' : '',
        'ext_phone' : '',
        'building' : '',
        'room' : '',
        'adress' : '',
        'id_employee': '', 
        'id_phone': '', 
        'id_room': '',
        'id_position': '',
        'id_unit': '', 
        'id_department': '', 
    }
    with connection.cursor() as cursor:
        info['id_employee'] = response[0]
        info['mail'] = response[1]
        info['id_phone'] = response[2]
        info['id_room'] = response[3]
        
        cursor.execute(
            f'''
            SELECT position.id_position,unit.id_unit,department.id_department FROM employee_info JOIN position ON 
            position.id_position=employee_info.id_position AND employee_info.id_employee = {info['id_employee']} JOIN unit ON 
            unit.id_unit=employee_info.id_unit AND employee_info.id_employee = {info['id_employee']} JOIN department ON 
            department.id_department=employee_info.id_department AND employee_info.id_employee = {info['id_employee']};
            '''
        )
        response = cursor.fetchall()[0]
        info['id_position'] = response[0]
        info['id_unit'] = response[1]
        info['id_department'] = response[2]
        cursor.execute(
            f'''
            SELECT employee.last_name,employee.first_name,employee.patronymic,employee.name_mail,room.number_room,
            phone.number_phone,phone.ext_phone,building.name_building,building.adress,unit.name_unit,department.name_department,
            position.name_position FROM employee JOIN phone ON employee.id_phone=phone.id_phone AND employee.id_employee = 
            {info['id_employee']} JOIN room ON employee.id_room=room.id_room AND room.id_room = {info['id_room']} 
            JOIN building ON room.id_room = building.id_building AND room.id_room = {info['id_room']} JOIN unit ON room.id_room 
            = unit.id_unit AND room.id_room = {info['id_room']} JOIN department ON unit.id_unit = department.id_unit AND 
            unit.id_unit = {info['id_unit']} JOIN employee_info ON employee.id_employee = employee_info.id_employee AND 
            employee.id_employee = {info['id_employee']} JOIN position ON position.id_position = employee_info.id_position 
            AND employee.id_employee = {info['id_employee']};
            '''
        )
        response = cursor.fetchall()[0]
    return(response)

def search_unit():
    with connection.cursor() as cursor:
        cursor.execute(
            f'''
            SELECT * FROM unit;
            '''
        )
        response = cursor.fetchall()
    return(response)