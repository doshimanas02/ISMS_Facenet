import sqlite3
#
# connection = None
# cursor = None
# # print(cursor)
#
# def main():
#     global connection
#     global cursor
#     connection = sqlite3.connect(r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db')
#     cursor = connection.cursor()
#
#
#

def connection():
    connection = sqlite3.connect(r'C:\Users\Administrator\PycharmProjects\ISMS_DeepFace\webcam_server\server\database\facialdb.db')
    cursor = connection.cursor()

    return cursor
