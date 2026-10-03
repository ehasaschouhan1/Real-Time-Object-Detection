import mysql.connector
from mysql.connector import Error
import config


def create_database_if_needed():
    connection = mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
    )
    cursor = connection.cursor()
    cursor.execute(
        f"CREATE DATABASE IF NOT EXISTS `{config.DB_NAME}` "
        "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
    )
    cursor.close()
    connection.close()


def get_connection():
    return mysql.connector.connect(
        host=config.DB_HOST,
        port=config.DB_PORT,
        user=config.DB_USER,
        password=config.DB_PASSWORD,
        database=config.DB_NAME,
    )


def initialize_database():
    create_database_if_needed()
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS detection_logs (
            log_id INT AUTO_INCREMENT PRIMARY KEY,
            timestamp DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
            object_class VARCHAR(100) NOT NULL,
            confidence DECIMAL(6,4) NOT NULL,
            bbox_x INT NOT NULL,
            bbox_y INT NOT NULL,
            bbox_w INT NOT NULL,
            bbox_h INT NOT NULL
        )
        """
    )
    connection.commit()
    cursor.close()
    connection.close()


def log_detection(object_class, confidence, bbox):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        query = """
            INSERT INTO detection_logs
            (object_class, confidence, bbox_x, bbox_y, bbox_w, bbox_h)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        x, y, w, h = bbox
        cursor.execute(query, (object_class, confidence, x, y, w, h))
        connection.commit()
        return True
    except Error as error:
        print(f"MySQL logging error: {error}")
        return False
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_recent_logs(limit=15):
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(
            """
            SELECT log_id, timestamp, object_class, confidence,
                   bbox_x, bbox_y, bbox_w, bbox_h
            FROM detection_logs
            ORDER BY log_id DESC
            LIMIT %s
            """,
            (limit,),
        )
        return cursor.fetchall()
    except Error as error:
        print(f"MySQL read error: {error}")
        return []
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
