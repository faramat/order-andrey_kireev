import sqlite3
import openpyxl
from datetime import datetime


connectDb = sqlite3.connect('users.db')
cursorDb = connectDb.cursor()
# response = cursorDb.execute('''SELECT date('now');''')
# response = response.fetchone()
# print(response[0])
# full_name = 'Шакиров Адель Маратович'
# sex = 'муж'
# phone = '+893949238498'
# cursorDb.execute(f'INSERT INTO children(full_name,sex,date_of_birth,phone) VALUES (?,?,?,?);',(full_name,sex,response[0],phone))
# ------------------------------------------
# ДОБАВИТЬ В АДМИНЫ
# tg_login = 'test'
# tg_id = '1983853146'
# cursorDb.execute(f'INSERT INTO admins(tg_login,tg_id) VALUES (?,?);',(tg_login,tg_id))
# connectDb.commit()
# ------------------------------------------
# ДОБАВИТЬ В РОДИТЕЛИ
# cursorDb.execute(f'''INSERT INTO parents(tg_id,child_id,full_name,phone,email,date_registration) 
#                     VALUES (?,?,?,?,?,?);''',('19838531460',9999999,'test','test','test','test'))
# connectDb.commit()
# tg_login = 'test'
# tg_id = '1123123123'
# r = ((cursorDb.execute('''SELECT strftime('%d.%m.%Y', 'now');''')).fetchone())[0]
# r = ((cursorDb.execute('SELECT DATE();')).fetchone())[0]

# cursorDb.execute(f'INSERT INTO parents(tg_login,tg_id,child_id) VALUES (?,?,?);',(tg_login,tg_id,3))
# connectDb.commit()
# print(r)


#Имя РЕБЕНКА	
#Телефон РЕБЕНКА	
# Пол РЕБЕНКА	
# Дата Рождения РЕБЕНКА	
# ФИО РОДИТЕЛЯ	
# Телефон Родителя	
# Email родителя
# workbook = openpyxl.load_workbook('clients.xlsx')
# worksheet = workbook.active
# # 1658 строк
# i = 2
# while i <= 1658:
#     row_values = [cell.value for cell in worksheet[i]]
#     name_child = row_values[0]
#     phone_child = row_values[1]
#     sex_child = row_values[2]
#     dateOfBirth_child = row_values[3]
#     name_parent = row_values[4]
#     phone_parent = row_values[5]
#     email_parent = row_values[6]
#     date = datetime.now()
#     cursorDb.execute(f'INSERT INTO children(full_name,sex,date_of_birth,phone) VALUES (?,?,?,?);',(name_child,sex_child,dateOfBirth_child,phone_child))
#     cursorDb.execute(f'''INSERT INTO parents(child_id,full_name,phone,email,date_registration) 
#                         VALUES (?,?,?,?,?);''',(i-1,name_parent,phone_parent,email_parent,date))
#     connectDb.commit() 
#     i+=1

# print('End')

# response = cursorDb.execute(f'''SELECT * FROM parents WHERE phone LIKE '%96007%';''')
# connectDb.commit()
# response = response.fetchall()
# print(len(response))