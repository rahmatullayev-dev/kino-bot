import mysql.connector
import config

def create_connection():
    return mysql.connector.connect(
        host=config.host,
        user=config.db_user,
        password=config.db_password,
        database=config.db_databse
    )

def create_user(id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = f"select * from users where chat_id = '{id}'"
        cursor.execute(query)
        user = cursor.fetchone()

        if not user:
            cursor.execute(f"insert into users(chat_id, blocked) values({id}, 0)")
            connection.commit()
    finally:
        cursor.close()
        connection.close()


def add_movie(video_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        query = f"select * from data where video_id = '{video_id}'"
        cursor.execute(query)
        user = cursor.fetchone()

        if user:
            res = False
        else:
            cursor.execute(f"insert into `data` (`video_id`, `views`) values('{video_id}', 0)")
            connection.commit()
            res = cursor.lastrowid
        
        cursor.close()
        connection.close()
        return res
    except mysql.connector.Error as e:
        print(e)

def get_movie(file_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM `data` WHERE `id` = '{file_id}'")
        data2 = cursor.fetchone()

        if data2:
            views = data2[2]
            view = views + 1
            cursor.execute(f"SELECT * FROM `data` WHERE `id` = '{file_id}'")
            res = cursor.fetchall()
            cursor.execute(f"UPDATE `data` SET `views` = '{view}' WHERE `id` = '{file_id}'")
            connection.commit()
        else: 
            res = None

        return res
    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


def delete_movie(file_id):
    connection = create_connection()
    cursor = connection.cursor()

    try:
        cursor.execute(F"DELETE FROM data WHERE id = {file_id}")
        # cursor.execute(F"DELETE FROM data")
        connection.commit()
        res = True
    except mysql.connector.Error as e:
        print(e)
        res = False

    cursor.close()
    connection.close()


def add_channel(channel):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM `channels` WHERE `username` = '{channel}'")
        row = cursor.fetchone()

        if row == None:
            cursor.execute(f"INSERT INTO `channels`(`username`) VALUES('{channel}')")
            connection.commit()
            return True
        else:
            return False 


    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def remove_channel(kanal):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        cursor.execute(f"SELECT * FROM `channels` WHERE `username` = '{kanal}'")
        row = cursor.fetchone()

        if row:
            cursor.execute(f"DELETE FROM `channels` WHERE `username` = '{kanal}'")
            connection.commit()
            return True
        else:
            return False

    except mysql.connector.Error as e:
        print(e)
    finally:
        cursor.close()
        connection.close()

def all_channel():
    try:
        connection = create_connection()
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM `channels`")
        row = cursor.fetchall()

        data = []

        for channel in row:
            data.append(channel)
        
        return data
    finally:
        cursor.close()
        connection.close()


def disable_user(chat_id):
    try:
        connection= create_connection()
        cursor = connection.cursor()

        cursor.execute(f"UPDATE `users` SET `blocked` = 1 WHERE `chat_id` = '{chat_id}'")
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()
def enable_user(chat_id):
    try:
        connection= create_connection()
        cursor = connection.cursor()

        cursor.execute(f"UPDATE `users` SET `blocked` = 0 WHERE `chat_id` = '{chat_id}'")
        connection.commit()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        connection.close()


connection = create_connection()
cursor = connection.cursor()

try:
    cursor.execute("""CREATE TABLE IF NOT EXISTS users(
                id INT AUTO_INCREMENT PRIMARY KEY,
                chat_id varchar(20) not null,
                date varchar(20),
                blocked boolean
                )""")
    connection.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS channels(
                id INT AUTO_INCREMENT PRIMARY KEY,
                username varchar(20) not null
                )""")
    connection.commit()
    cursor.execute("""CREATE TABLE IF NOT EXISTS data(
                id INT AUTO_INCREMENT PRIMARY KEY,
                video_id varchar(255) not null,
                views int
                )""")
    connection.commit()

except mysql.connector.Error as e:
    print(f"Xatolik yuz berdi\nXatolik: {e}")


cursor.close()
connection.close()