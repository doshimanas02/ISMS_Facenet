import sqlite3

connection = sqlite3.connect(r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db')
cursor = connection.cursor()
# print(cursor)