import pandas as pd
import mysql.connector
from mysql.connector import Error

def read_csv_file(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path)
    return df

def create_mysql_connection(host_name, user_name, user_password, db_name, port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=port
        )
        print("MySQL connection successful")
    except Error as e:
        print(f"Error: '{e}'")
    return connection

def create_table_if_not_exists(connection, table_name):
    cursor = connection.cursor()
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS `{table_name}` (
        `Id` INT AUTO_INCREMENT NOT NULL,
        `model` VARCHAR(255) NOT NULL,
        `year` INT NOT NULL,
        `motor_type` VARCHAR(255) NOT NULL,
        `running` VARCHAR(255) NOT NULL,
        `wheel` VARCHAR(255) NOT NULL,
        `color` VARCHAR(255) NOT NULL,
        `type` VARCHAR(255) NOT NULL,
        `status` VARCHAR(255) NOT NULL,
        `motor_volume` FLOAT NOT NULL,
        `price` INT NOT NULL,
        PRIMARY KEY (`Id`)
    )
    """
    try:
        cursor.execute(create_table_query)
        connection.commit()
        print(f"Table `{table_name}` is ready.")
    except Error as e:
        print(f"Error: '{e}'")
    cursor.close()

def insert_data_to_mysql(connection, df, table_name):
    cursor = connection.cursor()
    
    # Creating insert statement
    cols = ",".join([f"`{i}`" for i in df.columns.tolist()])
    
    for i, row in df.iterrows():
        sql = f"INSERT INTO `{table_name}` ({cols}) VALUES ({'%s, ' * (len(row) - 1)}%s)"
        cursor.execute(sql, tuple(row))
        connection.commit()
    cursor.close()

def main():
    # Define your CSV file path and MySQL database credentials
    csv_file_path = '../jupyter/Linear_Regression/train.csv'
    mysql_host = 'localhost'
    mysql_user = 'root'
    mysql_password = 'root'
    mysql_port  = 33060
    mysql_db = 'big-data'
    table_name = 'train'
    # Read CSV file
    df = read_csv_file(csv_file_path)
    
    # Create MySQL connection
    connection = create_mysql_connection(mysql_host, mysql_user, mysql_password, mysql_db, mysql_port)
    
    if connection is not None and connection.is_connected():
        # Create table if it does not exist
        create_table_if_not_exists(connection, table_name)
        
        # Insert data into MySQL
        insert_data_to_mysql(connection, df, table_name)
        
        # Close the connection
        connection.close()

if __name__ == "__main__":
    main()
