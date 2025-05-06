import psycopg2
from database.Database import DBConnector

class MeterRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_all_meter(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM METER;")
        meters = cursor.fetchall()
        cursor.close()
        conn.close()
        return meters
    
    def get_meter_by_id(self, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM METER WHERE METER_ID = %s;",
            (meter_id,)
        )
        meter = cursor.fetchall()
        cursor.close()
        conn.close()
        return meter
    

    def create_meter(self, meter_last_reading, serial_number):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO METER (
                METER_LAST_READING, METER_LAST_READING_DATE, METER_CODE, SERIAL_NUMBER
            ) VALUES (
                %s, CURRENT_DATE,
                'MTR-' || LPAD(nextval('meter_code_alphanumeric')::text, 5, '0'), %s
            )
            RETURNING METER_ID;
        """, (
            meter_last_reading, serial_number
        ))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id
    
    def update_meter(self, pres_read, read_date, meter_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE METER 
            SET METER_LAST_READING = %s, METER_LAST_READING_DATE = %s 
            WHERE METER_ID = %s
        """, (pres_read, read_date, meter_id))
        conn.commit()
        cursor.close()
        conn.close()
