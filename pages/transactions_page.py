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

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("TRANSACTIONS")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Search bar
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText("Search transactions...")
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """)
        header_layout.addWidget(search_input)
        layout.addLayout(header_layout)

        # Transactions Table
        self.transactions_table = QtWidgets.QTableWidget()
        self.transactions_table.setStyleSheet("""
            QTableWidget {
                border: 1px solid #ccc;
                border-radius: 4px;
                background-color: #C9EBCB;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
            }
        """)
        
        # Set up table columns
        self.transactions_table.setColumnCount(6)
        self.transactions_table.setHorizontalHeaderLabels([
            "TRANSACTION ID", "CLIENT NAME", "AMOUNT", "CASHIER", "DATE", "STATUS"
        ])
        
        # Sample data
        sample_data = [
            ("TR001", "Alice Brown", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
            ("TR002", "Charlie Davis", "₱50", "John Doe", "2023-10-15", "PENDING"),
            ("TR003", "Eve Franklin", "₱50", "John Doe", "2023-10-15", "FAILED"),
            ("TR004", "George Harris", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
        ]
        
        # Populate table
        self.transactions_table.setRowCount(len(sample_data))
        for row, (trans_id, name, amount, cashier, date, status) in enumerate(sample_data):
            self.transactions_table.setItem(row, 0, QtWidgets.QTableWidgetItem(trans_id))
            self.transactions_table.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.transactions_table.setItem(row, 2, QtWidgets.QTableWidgetItem(amount))
            self.transactions_table.setItem(row, 3, QtWidgets.QTableWidgetItem(cashier))
            self.transactions_table.setItem(row, 4, QtWidgets.QTableWidgetItem(date))
            
            # Status with color coding
            status_item = QtWidgets.QTableWidgetItem(status)
            status_item.setForeground(
                QtGui.QColor("#4CAF50") if status == "COMPLETED" 
                else QtGui.QColor("#FFA726") if status == "PENDING"
                else QtGui.QColor("#E57373")
            )
            self.transactions_table.setItem(row, 5, status_item)

        # Adjust table properties
        self.transactions_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.transactions_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.transactions_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.transactions_table.verticalHeader().setVisible(False)
        
        layout.addWidget(self.transactions_table)

        # Add export button
        export_btn = QtWidgets.QPushButton("Export to Excel")
        export_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                max-width: 150px;
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        export_btn.clicked.connect(self.export_to_excel)
        
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)
        button_layout.addWidget(export_btn)
        layout.addWidget(button_container)

    def export_to_excel(self):
        # This method will be implemented when you're ready to add Excel export functionality
        pass

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransactionsPage()
    window.show()
    sys.exit(app.exec_())    