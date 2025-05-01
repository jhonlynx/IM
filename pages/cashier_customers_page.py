import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.employeeBack import CustomerPageBack

class CustomersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.showMaximized()
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and add button
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("CUSTOMERS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()
        
        # Search and add button container
        search_add_layout = QtWidgets.QHBoxLayout()
        search_add_layout.setSpacing(10)
        
        # Search bar
        search_input = QtWidgets.QLineEdit()
        search_input.setPlaceholderText("Search customers by Id...")
        search_input.setStyleSheet("""
            QLineEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """)
        search_add_layout.addWidget(search_input)
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD CUSTOMER", icon=QtGui.QIcon("images/add.png"))
        add_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        add_btn.clicked.connect(self.show_add_customer_page)  # Changed from setup_add_customer_page
        search_add_layout.addWidget(add_btn)
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)

        # Customers Table
        self.customers_table = QtWidgets.QTableWidget()
        self.customers_table.setStyleSheet("""
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
        self.customers_table.setColumnCount(10)
        self.customers_table.setHorizontalHeaderLabels([
            "FIRST NAME", "MIDDLE NAME", "LAST NAME", "CONTACT",
            "CATEGORY", "ADDRESS", "LOCATION", "METER CODE", "FIRST READING", "STATUS"
        ])
        
        customer_back = CustomerPageBack()
        data = customer_back.fetch_customers('Employee')
        
        self.populate_table(data)
        
        # Adjust table properties
        self.customers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.customers_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.customers_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.customers_table.verticalHeader().setVisible(False)
        self.customers_table.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)  # <--- Add this line

        layout.addWidget(self.customers_table)

    def populate_table(self, data):
        self.customers_table.setRowCount(len(data))
        for row, (first_name, middle_name, last_name, contact, category, address, location, meter_code, first_reading, status) in enumerate(data):
            self.customers_table.setItem(row, 0, QtWidgets.QTableWidgetItem(first_name))
            self.customers_table.setItem(row, 1, QtWidgets.QTableWidgetItem(middle_name))
            self.customers_table.setItem(row, 2, QtWidgets.QTableWidgetItem(last_name))
            self.customers_table.setItem(row, 3, QtWidgets.QTableWidgetItem(contact))
            self.customers_table.setItem(row, 4, QtWidgets.QTableWidgetItem(category))
            self.customers_table.setItem(row, 5, QtWidgets.QTableWidgetItem(address))
            self.customers_table.setItem(row, 6, QtWidgets.QTableWidgetItem(location))
            self.customers_table.setItem(row, 7, QtWidgets.QTableWidgetItem(meter_code))
            self.customers_table.setItem(row, 8, QtWidgets.QTableWidgetItem(first_reading))
            self.customers_table.setItem(row, 8, QtWidgets.QTableWidgetItem(status))
            
            # # Action buttons
            # actions_widget = QtWidgets.QWidget()
            # actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            # actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # edit_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/edit.png"))
            # delete_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/delete.png"))
            
            # for btn in [edit_btn, delete_btn]:
            #     btn.setIconSize(QtCore.QSize(24, 24))
            #     btn.setStyleSheet("""
            #         QPushButton {
            #             padding: 5px 10px;
            #             border: none;
            #             border-radius: 4px;
            #         }
            #         QPushButton:hover {
            #             background-color: #f0f0f0;
            #         }
            #     """)
            #     actions_layout.addWidget(btn)
            
            # self.customers_table.setCellWidget(row, 9, actions_widget)

    def show_add_customer_page(self):
        # Create dialog instead of widget
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("Add New Customer")
        add_dialog.setModal(True)
        add_dialog.setMinimumWidth(500)
        add_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(add_dialog)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header
        title = QtWidgets.QLabel("ADD NEW CUSTOMER")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        layout.addWidget(title)

        # Form layout
        form_layout = QtWidgets.QFormLayout()
        form_layout.setSpacing(15)

        # Input fields
        fields = [
            ("First Name", QtWidgets.QLineEdit()),
            ("Middle Name", QtWidgets.QLineEdit()),
            ("Last Name", QtWidgets.QLineEdit()),
            ("Contact Number", QtWidgets.QLineEdit()),
            ("Category", QtWidgets.QComboBox()),
            ("Address", QtWidgets.QLineEdit()),
            ("Location", QtWidgets.QComboBox()),
            ("Meter Code", QtWidgets.QLineEdit()),
            ("First Reading", QtWidgets.QLineEdit()),
        ]

        # Set up combo boxes
        category_combo = fields[4][1]
        category_combo.addItems(["Residential", "Commercial", "Industrial"]) 
        location_combo = fields[6][1]
        location_combo.addItems(["Conseulo", "Santiago", "Hemensulan"])
        

        # Style inputs
        input_style = """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 300px;
            }
        """
        
        # Add fields to form and apply styles
        for label, widget in fields:
            widget.setStyleSheet(input_style)
            form_layout.addRow(f"{label}:", widget)

        layout.addLayout(form_layout)
        layout.addStretch()

        # Buttons container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        # Cancel button
        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #ccc;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #999;
            }
        """)
        cancel_btn.clicked.connect(add_dialog.reject)

        # Save button
        save_btn = QtWidgets.QPushButton("Save Customer")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: rgb(229, 115, 115);
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: rgb(200, 100, 100);
            }
        """)
        save_btn.clicked.connect(add_dialog.accept)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        # Show dialog
        add_dialog.exec_()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = CustomersPage()
    window.show()
    sys.exit(app.exec_())