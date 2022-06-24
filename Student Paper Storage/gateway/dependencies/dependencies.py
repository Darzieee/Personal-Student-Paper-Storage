import uuid

import mysql.connector
from mysql.connector import Error
from mysql.connector import pooling

from nameko.extensions import DependencyProvider

class DatabaseWrapper:

    connection = None

    def __init__(self, connection):
        self.connection = connection

    def add_user(self, nrp,account,email, password):
        ## checking if user already exist or not
    
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM dbuser 
        WHERE name = %s;
        """, (account,))
        for row in cursor.fetchall():
            result.append({
                'id': row['id'],
                'account': row['name']
            })

        if result:
            cursor.close()
            return "email already exist"
        
        ## if user doesnt exist yet, create the account
        
        else:
            cursor = self.connection.cursor(dictionary=True)
            generateUUID = str(uuid.uuid4())
            print(generateUUID)
            cursor.execute("""
            INSERT INTO dbuser (id,nrp,name,email,password)
            VALUES (%s, %s, %s,%s,%s);
            """, ( generateUUID,nrp,account,email, password))
            cursor.close()
            self.connection.commit()
            return "register success!"
        
    def add_file(self, account, file):
        # check if user already exist
        cursor = self.connection.cursor(dictionary=True)
    
        cursor.execute("""
        INSERT INTO filestorage (id_user,file)
        VALUES (%s, %s);
        """, ( account,file))
        cursor.close()
        self.connection.commit()
        return "File uploaded!"
    
    # get user for login
    def get_user(self, email, password):
        cursor = self.connection.cursor(dictionary=True)
        result = []
        cursor.execute("""
        SELECT * FROM dbuser 
        WHERE email = %s AND password = %s;
        """, (email, password))
        for row in cursor.fetchall():
            result.append({
                'session_id':'',
                'id': row['id'],
                'email': row['email']
            })
        cursor.close()
        return result

class Database(DependencyProvider):

    connection_pool = None

    def __init__(self):
        try:
            self.connection_pool = mysql.connector.pooling.MySQLConnectionPool(
                pool_name="database_pool",
                pool_size=5,
                pool_reset_session=True,
                host='localhost',
                database='simple_cloud_storage',
                user='root',
                password=''
            )
        except Error as e :
            print ("Error", e)
    
    def get_dependency(self, worker_ctx):
        return DatabaseWrapper(self.connection_pool.get_connection())