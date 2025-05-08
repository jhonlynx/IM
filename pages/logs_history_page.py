import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

class TextEllipsisDelegate(QtWidgets.QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super().initStyleOption(option, index)
        option.textElideMode = QtCore.Qt.ElideRight

class LogsAndHistoryPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        header_layout = QtWidgets.QHBoxLayout()

        title = QtWidgets.QLabel("Logs and History")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        self.view_selector = QtWidgets.QComboBox()
        self.view_selector.addItems(["Transaction History", "System Logs"])
        self.view_selector.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        self.view_selector.currentIndexChanged.connect(self.switch_view)
        header_layout.addWidget(self.view_selector)

        layout.addLayout(header_layout)

        self.table_stack = QtWidgets.QStackedWidget()

        self.transaction_history_table = self.create_transaction_history_table()
        self.system_logs_table = self.create_system_logs_table()

        self.table_stack.addWidget(self.transaction_history_table)
        self.table_stack.addWidget(self.system_logs_table)

        layout.addWidget(self.table_stack)
        self.table_stack.setCurrentIndex(0)

    def create_transaction_history_table(self):
        table = QtWidgets.QTableWidget()
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        table.setColumnCount(7)
        table.setHorizontalHeaderLabels([
            "Log ID", "Transaction ID", "Action", "Timestamp", "User", "Old Status", "New Status"
        ])
        table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        table.setWordWrap(False)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setItemDelegate(TextEllipsisDelegate(table))

        sample_data = [
            (1, "TR001", "Status Update", "2023-10-15 14:30:00", "John Doe", "PENDING", "COMPLETED"),
            (2, "TR002", "Status Update", "2023-10-15 15:00:00", "Jane Smith", "COMPLETED", "PENDING"),
            (3, "TR003", "Updated", "2023-10-15 16:00:00", "John Doe", "FAILED", "COMPLETED"),
        ]

        table.setRowCount(len(sample_data))
        for row, data_row in enumerate(sample_data):
            for col, value in enumerate(data_row):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

        return table

    def create_system_logs_table(self):
        table = QtWidgets.QTableWidget()
        table.setAlternatingRowColors(True)
        table.setStyleSheet("""
            QTableWidget {
                border: none;
                background-color: #E8F5E9;
                alternate-background-color: #FFFFFF;
            }
            QHeaderView::section {
                background-color: #B2C8B2;
                padding: 8px;
                border: none;
                font-family: 'Roboto', sans-serif;
                font-weight: bold;
                font-size: 15px;
            }
        """)
        table.setColumnCount(4)
        table.setHorizontalHeaderLabels(["Log ID", "Log Message", "Timestamp", "User"])
        table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        table.setWordWrap(False)
        table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        table.verticalHeader().setVisible(False)
        table.setItemDelegate(TextEllipsisDelegate(table))

        logs_data = [
            (1, "User John Doe logged in", "2023-10-15 14:00:00", "John Doe"),
            (2, "Transaction TR001 completed", "2023-10-15 14:30:00", "John Doe"),
            (3, "Error: Failed to load transaction", "2023-10-15 16:30:00", "System"),
        ]

        table.setRowCount(len(logs_data))
        for row, data_row in enumerate(logs_data):
            for col, value in enumerate(data_row):
                table.setItem(row, col, QtWidgets.QTableWidgetItem(str(value)))

        return table

    def switch_view(self, index):
        self.table_stack.setCurrentIndex(index)

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = LogsAndHistoryPage()
    window.showMaximized()
    sys.exit(app.exec_())
