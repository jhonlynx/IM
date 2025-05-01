import psycopg2
from database.Database import DBConnector

class BillingRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def get_billing_by_id(self, billing_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM BILLING WHERE ID = %s;", (billing_id,))
        bill = cursor.fetchone()
        cursor.close()
        conn.close()
        return bill
    
    
    def create_billing(self, billing_due, billing_total, billing_consumption, reading_id, client_id, categ_id, billing_date):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO BILLING (BILLING_DUE, BILLING_TOTAL, BILLING_CONSUMPTION, READING_ID, CLIENT_ID, CATEG_ID, BILLING_DATE) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING BILLING_ID;",
            (billing_due, billing_total, billing_consumption, reading_id, client_id, categ_id, billing_date)
        )
        new_bill = cursor.fetchone()[0]
        conn.commit()
        cursor.close()
        conn.close()
        return new_bill
    
    def get_all_billing(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT b.billing_code, b.issued_date, b.billing_due, c.client_id, c.client_name, c.client_location,
                            b.billing_total, b.billing_status
                FROM BILLING b
                JOIN CLIENT c ON b.client_id = c.client_id
            """)

            billings = cursor.fetchall()

            # Prepare data for the table (formatted_clients)
            formatted_clients = [
                (
                    billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, billing_status
                )
                for billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, billing_status in billings
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




    def update_billing(self, user_id, username, password, role):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE USER_ID = %s;", (user_id,))
        user = cursor.fetchone()

        if user:
            cursor.execute("UPDATE USERS SET USERNAME = %s, PASSWORD = %s, ROLE = %s WHERE USER_ID = %s;",
                (username, password, role, user_id))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False
