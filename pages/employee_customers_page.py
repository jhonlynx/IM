import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.adminBack import adminPageBack

class EmployeeCustomersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("CUSTOMERS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        # Search and Add button container
        search_add_layout = QtWidgets.QHBoxLayout() 
        
        # Search container
        search_container = QtWidgets.QHBoxLayout()
        
        # Search criteria dropdown
        self.search_criteria = QtWidgets.QComboBox()
        self.search_criteria.addItems(["ID", "First Name", "Last Name", "Location", "Category"])
        self.search_criteria.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 120px;
                background-color: white;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(images/dropdown.png);
                width: 12px;
                height: 12px;
            }
        """)
        search_container.addWidget(self.search_criteria)
        
        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search customers...")
        self.search_input_combo = QtWidgets.QComboBox()
        self.search_input_combo.addItems(["Residential", "Commercial", "Industrial"])
        self.search_input_combo.hide()  # Initially hidden
        
        # Apply same styling to both widgets
        input_style = """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input_combo.setStyleSheet(input_style)
        
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input_combo.currentTextChanged.connect(self.filter_table)
        
        # Add widgets to container
        search_container.addWidget(self.search_input)
        search_container.addWidget(self.search_input_combo)
        
        # Connect search criteria change
        self.search_criteria.currentTextChanged.connect(self.toggle_search_input)
        
        search_add_layout.addLayout(search_container)
        
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
        add_btn.clicked.connect(self.show_add_customer_page)
        search_add_layout.addWidget(add_btn)
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)  



        # Table setup
        self.customers_table = QtWidgets.QTableWidget()
        self.customers_table.setAlternatingRowColors(True)
        self.customers_table.setStyleSheet("""
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
        
        # Set up columns (10 columns)
        self.customers_table.setColumnCount(10)
        self.customers_table.setHorizontalHeaderLabels([
            "CLIENT ID", "CLIENT NUMBER", "FIRST NAME", "MIDDLE NAME", "LAST NAME", "CONTACT",
            "CATEGORY", "ADDRESS", "LOCATION", "STATUS"
        ])
        
        customer_back = adminPageBack()
        data = customer_back.fetch_clients()
        
        self.populate_table(data)
        
        # Adjust table properties
        self.customers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.customers_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.customers_table.verticalHeader().setVisible(False)
        self.customers_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.customers_table)


    def populate_table(self, data):
        self.customers_table.setRowCount(0)  # Clear previous rows
        self.customers_table.setRowCount(len(data))
        
        for row, customer in enumerate(data):
            # Unpack all values (now expecting 11 values in the customer tuple)
            client_id, client_number, fname, middle_name, lname, contact, categ_name, address_id, location, status = customer

            # Add customer data to the table
            self.customers_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(client_id)))
            self.customers_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(client_number)))
            self.customers_table.setItem(row, 2, QtWidgets.QTableWidgetItem(fname))
            self.customers_table.setItem(row, 3, QtWidgets.QTableWidgetItem(middle_name))
            self.customers_table.setItem(row, 4, QtWidgets.QTableWidgetItem(lname))
            self.customers_table.setItem(row, 5, QtWidgets.QTableWidgetItem(contact))
            self.customers_table.setItem(row, 6, QtWidgets.QTableWidgetItem(categ_name))
            self.customers_table.setItem(row, 7, QtWidgets.QTableWidgetItem(address_id))
            self.customers_table.setItem(row, 8, QtWidgets.QTableWidgetItem(location))
            self.customers_table.setItem(row, 9, QtWidgets.QTableWidgetItem(status))

            # Status with color coding
            status_item = QtWidgets.QTableWidgetItem(status)
            status_item.setForeground(
                QtGui.QColor("#64B5F6") if status == "Active" else QtGui.QColor("#E57373")
            )
            self.customers_table.setItem(row, 9, status_item)

            # # Action buttons
            # actions_widget = QtWidgets.QWidget()
            # actions_layout = QtWidgets.QHBoxLayout(actions_widget)
            # actions_layout.setContentsMargins(4, 4, 4, 4)
            
            # edit_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/edit.png"))
            # delete_btn = QtWidgets.QPushButton(icon=QtGui.QIcon("images/delete.png"))
            
            # edit_btn.setIconSize(QtCore.QSize(24, 24))
            # delete_btn.setIconSize(QtCore.QSize(24, 24))
            
            # for btn in [edit_btn, delete_btn]:
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
            
            # self.customers_table.setCellWidget(row, 11, actions_widget)  # Place action buttons in the 11th column

    def filter_table(self):
        search_by = self.search_criteria.currentText()
        
        if search_by == "Category":
            search_text = self.search_input_combo.currentText().lower()
        else:
            search_text = self.search_input.text().lower()
        
        for row in range(self.customers_table.rowCount()):
            match = False
            if search_text:
                if search_by == "ID":
                    item = self.customers_table.item(row, 0)
                elif search_by == "First Name":
                    item = self.customers_table.item(row, 1)
                elif search_by == "Last Name":
                    item = self.customers_table.item(row, 3)
                elif search_by == "Location":
                    item = self.customers_table.item(row, 7)
                elif search_by == "Category":
                    item = self.customers_table.item(row, 5)
                
                if item and search_text in item.text().lower():
                    match = True
            else:
                match = True
                
            self.customers_table.setRowHidden(row, not match)

    def show_add_customer_page(self):
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("New Customer")
        add_dialog.setModal(True)
        add_dialog.setFixedSize(1000, 700)
        add_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(add_dialog)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.setSpacing(10)

        # Section Title
        title = QtWidgets.QLabel("ADD NEW CUSTOMER")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(40)
        form_layout.setVerticalSpacing(20)

        input_style = """
            QLineEdit, QComboBox {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        def create_labeled_widget(label_text, widget):
            container = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            container.addWidget(label)
            container.addWidget(widget)
            return container

        fields = {
            "First Name": QtWidgets.QLineEdit(),
            "Middle Name": QtWidgets.QLineEdit(),
            "Last Name": QtWidgets.QLineEdit(),
            "Contact Number": QtWidgets.QLineEdit(),
            "Category": QtWidgets.QComboBox(),
            "Location": QtWidgets.QLineEdit(),
            "Address": QtWidgets.QComboBox(),
            "Serial Number": QtWidgets.QLineEdit(),
            "First Reading": QtWidgets.QLineEdit(),
        }

        for widget in fields.values():
            widget.setStyleSheet(input_style)

        # Fetch backend data
        IadminPageBack = adminPageBack()
        for category_id, category_name in IadminPageBack.fetch_categories():
            fields["Category"].addItem(category_name, category_id)
        for address_id, address_name in IadminPageBack.fetch_address():
            fields["Address"].addItem(address_name, address_id)

        # Layout inputs in 2 columns
        left_fields = ["First Name", "Middle Name", "Last Name", "Contact Number", "Category"]
        right_fields = ["Location", "Address", "Serial Number", "First Reading"]

        for i, key in enumerate(left_fields):
            form_layout.addLayout(create_labeled_widget(f"{key}:", fields[key]), i, 0)

        for i, key in enumerate(right_fields):
            form_layout.addLayout(create_labeled_widget(f"{key}:", fields[key]), i, 1)

        layout.addLayout(form_layout)

        # Buttons
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        cancel_btn = QtWidgets.QPushButton("Cancel")
        cancel_btn.setStyleSheet("""
            QPushButton {
                background-color: #95a5a6;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #7f8c8d;
            }
        """)
        cancel_btn.clicked.connect(add_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save Customer")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #c0392b;
            }
        """)

        def save_customer():
            category_combo = fields["Category"]
            address_combo = fields["Address"]
            category_id = category_combo.currentData()
            address_id = address_combo.currentData()

            input_values = {label: widget.text().strip() if isinstance(widget, QtWidgets.QLineEdit) else widget.currentText().strip() for label, widget in fields.items()}

            missing_fields = [label for label in fields if label != "Middle Name" and not input_values[label]]
            if missing_fields:
                QtWidgets.QMessageBox.warning(self, "Missing Fields", "Please fill in all the required fields.")
                return

            name_fields = ["First Name", "Middle Name", "Last Name"]
            invalid_name_fields = [label for label in name_fields if input_values[label] and not input_values[label].replace(" ", "").isalpha()]
            if invalid_name_fields:
                QtWidgets.QMessageBox.warning(self, "Error", f"These fields must contain letters only: {', '.join(invalid_name_fields)}")
                return

            try:
                float(input_values["Contact Number"])
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "Contact Number must be a valid number.")
                return

            try:
                meter_reading = float(input_values["First Reading"])
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "First Reading must be a number.")
                return

            meter_id = IadminPageBack.add_meter(meter_reading, input_values["Serial Number"])
            new_client_id = IadminPageBack.add_client(
                client_name=input_values["First Name"],
                client_lname=input_values["Last Name"],
                client_contact_num=input_values["Contact Number"],
                client_location=input_values["Location"],
                meter_id=meter_id,
                address_id=address_id,
                categ_id=category_id,
                client_mname=input_values["Middle Name"],
                status="Active"
            )

            QtWidgets.QMessageBox.information(self, "Success", "Customer added successfully.")
            add_dialog.accept()
            updated_data = IadminPageBack.fetch_clients()
            self.populate_table(updated_data)

        save_btn.clicked.connect(save_customer)
        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        add_dialog.exec_()
 

    def toggle_search_input(self, text):
            if text == "Category":
                self.search_input.hide()
                self.search_input_combo.show()
            else:
                self.search_input.show()
                self.search_input_combo.hide()           


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EmployeeCustomersPage()
    window.show()
    sys.exit(app.exec_())
