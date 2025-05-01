import psycopg2
from database.Database import DBConnector

class UserRepository:
    def __init__(self):
        self.db_connector = DBConnector()

    def get_connection(self):
        return self.db_connector.get_connection()

    def check_user(self, username, password):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT ROLE FROM USERS WHERE USERNAME = %s AND PASSWORD = %s;", (username, password))
        role = cursor.fetchone()
        cursor.close()
        conn.close()
        return role[0] if role else None

    def get_all_users(self):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS;")
        users = cursor.fetchall()
        cursor.close()
        conn.close()
        return users
    
    def get_all_employee(self):
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT u.USER_ID, u.NAME, u.USERNAME
                FROM USERS u
            """)
            users = cursor.fetchall()

            formatted_clients = [
                (
                    user_id, name, username
                )
                for user_id, name, username in users
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
    
    def create_user(self, username, password, role, name):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO  (USERNAME, PASSWORD, ROLE, NAME) VALUES (%s, %s, %s, %s) RETURNING _ID;",
                       (username, password, role, name))
        new_id = cursor.fetchone()
        conn.commit()
        cursor.close()
        conn.close()
        return new_id

    def update_user(self, user_id, username, password, role):
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

    def delete_user(self, user_id):
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM USERS WHERE USER_ID = %s;", (user_id,))
        user = cursor.fetchone()

        if user:
            cursor.execute("DELETE FROM USERS WHERE USER_ID = %s;", (user_id,))
            conn.commit()
            cursor.close()
            conn.close()
            return True
        else:
            cursor.close()
            conn.close()
            return False
