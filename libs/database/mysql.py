import mysql.connector


# create a function to create a mysql database
def create_database(connection, database_name: str):


    # create a cursor object
    cursor = connection.cursor()

    # create a database if it does not exist
    cursor.execute(f'CREATE DATABASE IF NOT EXISTS {database_name}')


    # close the cursor
    cursor.close()


# create a function to get the connection to the database
def get_connection(database_name: str, user: str, password: str):
    # create a connection to the mysql server
    connection = mysql.connector.connect(host='localhost', user=user, password=password)

    return connection

# create a function to create a table in the database
def create_table_inverter(database, table_name: str):
    # create a connection to the mysql server
    connection = mysql.connector.connect(host='localhost', user=user, password=password, database=database_name)

    # create a cursor object
    cursor = connection.cursor()

    # create a table if it does not exist
    cursor.execute(f'''CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        Power FLOAT,
        Status VARCHAR(255),
        Timestamp DATETIME,
        EnergyActual FLOAT,
        EnergyDay FLOAT
    )''')

    # close the cursor
    cursor.close()