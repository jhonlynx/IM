import psycopg2
from database.Database import DBConnector

class ClientRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_client_by_id(self, client_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM CLIENT WHERE ID = %s;",
            (client_id,)
        )
        client = cursor.fetchall()
        cursor.close()
        conn.close()
        return client


    def get_all_clients(self): 
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT c.CLIENT_ID, c.CLIENT_NUMBER, c.CLIENT_NAME, c.CLIENT_MNAME, c.CLIENT_LNAME, c.CLIENT_CONTACT_NUM,
                    cat.CATEG_NAME,  a.ADDRESS_NAME, c.CLIENT_LOCATION, c.STATUS
                FROM CLIENT c
                JOIN CATEGORY cat ON c.CATEG_ID = cat.CATEG_ID
                JOIN ADDRESS a ON c.ADDRESS_ID = a.ADDRESS_ID
                ORDER BY client_id ASC
            """)
            clients = cursor.fetchall()

            formatted_clients = [
                (
                    client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, status
                )
                for  client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, status in clients
            ]

            return formatted_clients

        except Exception as e:
            print(f"Database error: {e}")
            return []

        finally:
            if 'cursor' in locals():
                cursor.close()
            if 'conn' in locals():
                conn.close()



    def create_client(self, client_name, client_lname, client_contact_num, client_location, meter_id, address_id, categ_id, client_mname, status):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO CLIENT (
                CLIENT_NAME, CLIENT_LNAME, CLIENT_CONTACT_NUM, CLIENT_LOCATION,
                METER_ID, ADDRESS_ID, CATEG_ID, CLIENT_MNAME, STATUS, CLIENT_NUMBER
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                'CL-' || LPAD(nextval('client_number_seq')::text, 5, '0')        
            )
            RETURNING CLIENT_ID;
        """, (
            client_name, client_lname, client_contact_num, client_location,
            meter_id, address_id, categ_id, client_mname, status
        ))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id


    def update_client(self, client_id, client_name,client_mname, client_lname, client_contact_num, payment_id, address_id, categ_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CLIENT WHERE CLIENT_ID = %s;", (client_id,))
        client = cursor.fetchone()
        if client:
            cursor.execute("UPDATE CLIENT SET CLIENT_NAME = %s, CLIENT_MNAME = %s, CLIENT_LNAME = %s, CLIENT_CONTACT_NUM = %s, PAYMENT_ID = %s, ADDRESS_ID = %s, CATEG_ID = %s WHERE CLIENT_ID = %s;",
                           (client_name, client_lname, client_mname, client_contact_num, payment_id, address_id, categ_id, client_id))
            conn.commit()
            success = True
        else:
            success = False
        cursor.close()
        conn.close()
        return success

    def delete_client(self, client_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CLIENT WHERE CLIENT_ID = %s;", (client_id,))
        client = cursor.fetchone()

        if client:
            cursor.execute("DELETE FROM CLIENT WHERE CLIENT_ID = %s;", (client_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False