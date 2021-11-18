import mysql.connector
from mysql.connector import errorcode

'''
 --- Every database related functions are defined here.
'''


class Database():


    def getConnection(self):
        cnx = mysql.connector.connect(user='root', password='Sabeshnav12!@', host='127.0.0.1', database='ImpulseDB')
        return cnx
    def getCursor(self, cnx):
        cursor = cnx.cursor()
        return cursor




