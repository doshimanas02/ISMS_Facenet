import connector as c

c.cursor.execute('''create table face_meta (ID INT primary key, IMG_NAME VARCHAR(10), EMBEDDING BLOB)''')
c.cursor.execute('''create table face_embeddings (FACE_ID INT, DIMENSION INT, VALUE DECIMAL(5, 30))''')

