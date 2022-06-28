import sqlite3

connection = sqlite3.connect(
        r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db')
cursor = connection.cursor()
cursor.execute('''create table face_meta (ID INTEGER primary key AUTOINCREMENT, IMG_NAME VARCHAR(10), EMBEDDING BLOB)''')
cursor.execute('''create table face_embeddings (FACE_ID INTEGER, DIMENSION INT, VALUE DECIMAL(5, 30))''')

