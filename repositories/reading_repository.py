import psycopg2
from database.Database import DBConnector

class ReadingRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_all_reading(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM READING;")
        readings = cursor.fetchall()
        cursor.close()
        conn.close()
        return readings
    
    def get_reading_by_id(self, reading_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM METER WHERE READING_ID = %s;",
            (reading_id,)
        )
        reading = cursor.fetchall()
        cursor.close()
        conn.close()
        return reading
    

    def create_reading(self, read_date, prev_read, pres_read, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO READING (READING_DATE, READING_PREV, READING_CURRENT, METER_ID)
            VALUES (%s, %s, %s, %s)
            RETURNING READING_ID;
        """, (read_date, prev_read, pres_read, meter_id))
        new_reading_id = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return new_reading_id




    # def update_meter(self, reading_id,  prev, role):
    #     conn = self.get_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM USERS WHERE USER_ID = %s;", (user_id,))
    #     user = cursor.fetchone()

    #     if user:
    #         cursor.execute("UPDATE USERS SET USERNAME = %s, PASSWORD = %s, ROLE = %s WHERE USER_ID = %s;",
    #             (username, password, role, user_id))
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         return True
    #     else:
    #         cursor.close()
    #         conn.close()
    #         return False

    # def delete_user(self, user_id):
    #     conn = self.get_connection()
    #     cursor = conn.cursor()
    #     cursor.execute("SELECT * FROM USERS WHERE USER_ID = %s;", (user_id,))
    #     user = cursor.fetchone()

    #     if user:
    #         cursor.execute("DELETE FROM USERS WHERE USER_ID = %s;", (user_id,))
    #         conn.commit()
    #         cursor.close()
    #         conn.close()
    #         return True
    #     else:
    #         cursor.close()
    #         conn.close()
    #         return False
