import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

class TransactionsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.showMaximized()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title, search bar, and dropdown
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("TRANSACTIONS")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Search container
        search_container = QtWidgets.QHBoxLayout()

        # Dropdown for filter criteria and search inputs
        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["Transaction ID", "Client Name", "Employee", "Date"])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 150px;
                background-color: white;
            }
        """)
        search_container.addWidget(self.filter_combo)

        # Search inputs
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search transactions...")
        self.search_input_date = QtWidgets.QDateEdit()
        self.search_input_date.setCalendarPopup(True)
        self.search_input_date.hide()

        input_style = """
            QLineEdit, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
                background-color: white;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input_date.setStyleSheet(input_style)

        search_container.addWidget(self.search_input)
        search_container.addWidget(self.search_input_date)
        
        # Connect signals
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input_date.dateChanged.connect(self.filter_table)
        self.filter_combo.currentTextChanged.connect(self.toggle_search_input)

        # Add search container directly to header layout
        header_layout.addLayout(search_container)

        # Transaction type dropdown
        self.transaction_type_combo = QtWidgets.QComboBox()
        self.transaction_type_combo.addItems(["Daily Transaction", "Monthly Transaction"])
        self.transaction_type_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        self.transaction_type_combo.currentIndexChanged.connect(self.switch_table)
        header_layout.addWidget(self.transaction_type_combo)

        layout.addLayout(header_layout)

        # Create and populate tables
        self.daily_table = self.create_transactions_table()
        self.monthly_table = self.create_transactions_table()

        # Daily sample data
        daily_data = [
            ("TR001", "2023-10-15", "2023-10-15", "13001 ", "jhon", "raymond", "67.00", "980", "COMPLETED"),
            ("TR002", "2023-10-15", "2023-10-15", "13001 ", "jhon", "raymond", "67.00", "890", "PENDING"),
            ("TR003", "2023-10-15", "2023-10-15", "13001 ", "jhon", "raymond", "67.00", "980", "FAILED"),
            ("TR004", "2023-10-15", "2023-10-15", "13001 ", "jhon", "raymond", "67.00", "980", "FAILED"),
        ]
        self.populate_table(self.daily_table, daily_data)

        # Monthly sample data
        monthly_data = [
            ("MT001", "2023-10-15", "2023-10-15", "Jane Smith", "jhon", "raymond", "67.00", "890", "PENDING"),
            ("MT002", "2023-10-15", "2023-10-15", "Jane Smith", "jhon", "raymond", "67.00", "890", "FAILED"),
            ("MT003", "2023-10-15", "2023-10-15", "Jane Smith", "jhon", "raymond", "67.00", "980", "PENDING"),
            ("MT004", "2023-10-15", "2023-10-15", "Jane Smith", "jhon", "raymond", "67.00", "980", "COMPLETED"),
        ]
        self.populate_table(self.monthly_table, monthly_data)

        # Stack the tables for toggling
        self.table_stack = QtWidgets.QStackedWidget()
        self.table_stack.addWidget(self.daily_table)
        self.table_stack.addWidget(self.monthly_table)
        layout.addWidget(self.table_stack)


    def create_transactions_table(self):
        table = QtWidgets.QTableWidget()
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
        """)
        table.setColumnCount(9)
        table.setHorizontalHeaderLabels([
            "TRANSACTION ID", "PAYMENT DATE", "DUE DATE", "CLIENT NUMBER", "CLIENT NAME", "EMPLOYEE", "CONSUMPTION", "AMOUNT", "STATUS"
        ])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        return table

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, (trans_id, payment_due, due_date, client_number, client_name, employee, consumption, amount, status) in enumerate(data):
            table.setItem(row, 0, QtWidgets.QTableWidgetItem(trans_id))
            table.setItem(row, 1, QtWidgets.QTableWidgetItem(payment_due))
            table.setItem(row, 2, QtWidgets.QTableWidgetItem(due_date))
            table.setItem(row, 3, QtWidgets.QTableWidgetItem(client_number))
            table.setItem(row, 4, QtWidgets.QTableWidgetItem(client_name))
            table.setItem(row, 5, QtWidgets.QTableWidgetItem(employee))
            table.setItem(row, 6, QtWidgets.QTableWidgetItem(consumption))
            table.setItem(row, 7, QtWidgets.QTableWidgetItem(amount))
            table.setItem(row, 8, QtWidgets.QTableWidgetItem(status))
            status_item = QtWidgets.QTableWidgetItem(status)
            status_item.setForeground(
                QtGui.QColor("#4CAF50") if status == "COMPLETED"
                else QtGui.QColor("#FFA726") if status == "PENDING"
                else QtGui.QColor("#E57373")
            )
            table.setItem(row, 8, status_item)

    def switch_table(self, index):
        self.table_stack.setCurrentIndex(index)

    def toggle_search_input(self, text):
        if text == "Date":
            self.search_input.hide()
            self.search_input_date.show()
        else:
            self.search_input.show()
            self.search_input_date.hide()

    def filter_table(self):
        current_table = self.daily_table if self.transaction_type_combo.currentIndex() == 0 else self.monthly_table
        filter_by = self.filter_combo.currentText()
        
        # Get search text based on input type
        if filter_by == "Date":
            search_text = self.search_input_date.date().toString("yyyy-MM-dd").lower()
        else:
            search_text = self.search_input.text().lower()

        # Column mapping
        column_indices = {
            "Transaction ID": 0,
            "Client Name": 4,
            "Employee": 5,
            "Date": 2
        }
        
        column_index = column_indices.get(filter_by, 0)

        # Filter rows
        for row in range(current_table.rowCount()):
            item = current_table.item(row, column_index)
            if item:
                item_text = item.text().lower()
                match = search_text in item_text if filter_by != "Date" else search_text == item_text
                current_table.setRowHidden(row, not match)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransactionsPage()
    window.show()
    sys.exit(app.exec_())
