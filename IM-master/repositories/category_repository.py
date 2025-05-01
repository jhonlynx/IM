import psycopg2
from database.Database import DBConnector

class CategoryRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()
    
    def get_category(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM CATEGORY;")
        category = cursor.fetchall()
        cursor.close()
        conn.close()
        return category
    
    def get_category_by_id(self, categ_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT * FROM CATEGORY WHERE ID = %s;",
            (categ_id,)
        )
        category = cursor.fetchall()
        cursor.close()
        conn.close()
        return category
    
    def create_category(self, categ_name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO CATEGORY (CATEG_NAME) VALUES (%s) RETURNING CATEG_ID;",
                       (categ_name))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id


    # def get_all_category(self, user_type): 
    #     try:
    #         conn = self.get_connection()
    #         cursor = conn.cursor()

    #         if user_type == 'Employee':
    #             cursor.execute("""
    #                 SELECT c.CLIENT_NAME, c.CLIENT_MNAME, c.CLIENT_LNAME, c.CLIENT_CONTACT_NUM,
    #                     cat.CATEG_NAME, c.ADDRESS_ID, c.CLIENT_LOCATION, c.STATUS
    #                 FROM CLIENT c
    #                 JOIN CATEGORY cat ON c.CATEG_ID = cat.CATEG_ID
    #             """)
    #             clients = cursor.fetchall()

    #             formatted_clients = [
    #                 (
    #                     fname, middle_name, lname, contact, categ_name, address_id, location, status
    #                 )
    #                 for fname, middle_name, lname, contact, categ_name, address_id, location, status in clients
    #             ]

    #         elif user_type == 'Admin':
    #             cursor.execute("""
    #                 SELECT c.CLIENT_ID, c.CLIENT_NAME, c.CLIENT_MNAME, c.CLIENT_LNAME, c.CLIENT_CONTACT_NUM,
    #                     cat.CATEG_NAME, c.ADDRESS_ID, c.CLIENT_LOCATION, c.STATUS
    #                 FROM CLIENT c
    #                 JOIN CATEGORY cat ON c.CATEG_ID = cat.CATEG_ID
    #             """)
    #             clients = cursor.fetchall()

    #             formatted_clients = [
    #                 (
    #                     cid, fname, middle_name, lname, contact, categ_name, address_id, location, status
    #                 )
    #                 for cid, fname, middle_name, lname, contact, categ_name, address_id, location, status in clients
    #             ]

    #         else:
    #             print("Invalid user type.")
    #             return []

    #         return formatted_clients

    #     except Exception as e:
    #         print(f"Database error: {e}")
    #         return []

    #     finally:
    #         if 'cursor' in locals():
    #             cursor.close()
    #         if 'conn' in locals():
    #             conn.close()



    def create_client(self, client_id, client_name, client_lname, client_contact_num, payment_id, address_id, categ_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO CLIENT (CLIENT_NAME, CLIENT_LNAME, CLIENT_CONTACT_NUM, PAYMENT_ID, ADDRESS_ID, CATEG_ID) VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING CLIENT_ID;",
                       (client_name, client_lname, client_contact_num, payment_id, address_id, categ_id))
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