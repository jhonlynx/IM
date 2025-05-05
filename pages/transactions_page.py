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

        self.filter_combo.currentTextChanged.connect(self.toggle_search_input)
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input_date.dateChanged.connect(self.filter_table)

        header_layout.addLayout(search_container)

        # Transaction type dropdown
        self.transaction_type_combo = QtWidgets.QComboBox()
        self.transaction_type_combo.addItems(["All Transactions", "Daily Transaction", "Monthly Transaction"])
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

        # Create and populate single transactions table
        self.transactions_table = self.create_transactions_table()
        layout.addWidget(self.transactions_table)

        # Sample data combining daily and monthly transactions
        all_data = [
            ("TR001", "2025-05-04", "13001", "jhon", "raymond", "67.00", "980", "2023-10-15", "COMPLETED"),
            ("TR002", "2025-05-04", "13001", "jhon", "raymond", "67.00", "890", "2023-10-15", "PENDING"),
            ("TR003", "2023-10-15", "13001", "jhon", "raymond", "67.00", "980", "2023-10-15", "FAILED"),
            ("TR004", "2023-10-15", "13001", "jhon", "raymond", "67.00", "980", "2025-05-04", "FAILED"),
            ("TR005", "2023-10-15", "13001", "jhon", "raymond", "67.00", "890", "2025-05-04", "PENDING"),
            ("TR006", "2023-10-15", "13001", "jhon", "raymond", "67.00", "890", "2025-05-04", "FAILED"),
            ("TR007", "2023-10-15", "13001", "jhon", "raymond", "67.00", "980", "2025-05-04", "PENDING"),
            ("TR008", "2023-10-15", "13001", "jhon", "raymond", "67.00", "980", "2023-10-15", "COMPLETED"),
        ]

        self.populate_table(self.transactions_table, all_data)

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
            "TRANSACTION ID", "PAYMENT DATE", "CLIENT NUMBER", "CLIENT NAME", "EMPLOYEE", "CONSUMPTION", "AMOUNT", "DUE DATE", "STATUS"
        ])
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        return table

    def populate_table(self, table, data):
        table.setRowCount(len(data))
        for row, row_data in enumerate(data):
            for col, text in enumerate(row_data):
                item = QtWidgets.QTableWidgetItem(text.strip() if isinstance(text, str) else text)
                table.setItem(row, col, item)
            status_item = QtWidgets.QTableWidgetItem(row_data[8])
            status_item.setForeground(
                QtGui.QColor("#4CAF50") if row_data[8] == "COMPLETED"
                else QtGui.QColor("#FFA726") if row_data[8] == "PENDING"
                else QtGui.QColor("#E57373")
            )
            table.setItem(row, 8, status_item)

    def switch_table(self, index):
        self.filter_table()

    def toggle_search_input(self, text):
        if text == "Date":
            self.search_input.hide()
            self.search_input_date.show()
        else:
            self.search_input.show()
            self.search_input_date.hide()

    def filter_table(self):
        table = self.transactions_table
        filter_by = self.filter_combo.currentText()

        # Get search text
        if filter_by == "Date":
            search_text = self.search_input_date.date().toString("yyyy-MM-dd").lower()
        else:
            search_text = self.search_input.text().lower()

        # Map filter criteria to column index
        column_indices = {
            "Transaction ID": 0,
            "Client Name": 4,
            "Employee": 5,
            "Date": 7
        }
        column_index = column_indices.get(filter_by, 0)

        today = QtCore.QDate.currentDate()
        trans_type_index = self.transaction_type_combo.currentIndex()

        for row in range(table.rowCount()):
            item = table.item(row, column_index)
            date_item = table.item(row, 7)
            match_search = False
            match_type = True

            # Apply search filter
            if item:
                item_text = item.text().lower()
                match_search = (search_text in item_text) if filter_by != "Date" else (search_text == item_text)
            else:
                match_search = False

            # Apply transaction type filter
            if date_item:
                row_date_str = date_item.text().strip()
                row_date = QtCore.QDate.fromString(row_date_str, "yyyy-MM-dd")
                if not row_date.isValid():
                    match_type = False
                elif trans_type_index == 0:  # All Transactions
                    match_type = True
                elif trans_type_index == 1:  # Daily Transaction
                    match_type = (row_date == today)
                elif trans_type_index == 2:  # Monthly Transaction
                    match_type = (row_date.month() == today.month() and row_date.year() == today.year())

            table.setRowHidden(row, not (match_search and match_type))


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransactionsPage()
    window.show()
    sys.exit(app.exec_())