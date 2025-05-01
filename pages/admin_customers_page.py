import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.adminBack import adminPageBack

class AdminCustomersPage(QtWidgets.QWidget):
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
        self.customers_table.verticalHeader().setVisible(False)
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
                    item = self.customers_table.item(row, 2)
                elif search_by == "Last Name":
                    item = self.customers_table.item(row, 4)
                elif search_by == "Location":
                    item = self.customers_table.item(row, 8)
                elif search_by == "Category":
                    item = self.customers_table.item(row, 6)

                
                if item and search_text in item.text().lower():
                    match = True
            else:
                match = True
                
            self.customers_table.setRowHidden(row, not match)

    def show_add_customer_page(self):
        # Create dialog instead of widget
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("New Customer")
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
            ("Location", QtWidgets.QLineEdit()),
            ("Address", QtWidgets.QComboBox()),
            ("Serial Number", QtWidgets.QLineEdit()),
            ("First Reading", QtWidgets.QLineEdit()),
        ]

        # Instantiate backend
        IadminPageBack = adminPageBack()

        # Fetch and populate categories
        categories = IadminPageBack.fetch_categories()
        category_combo = next(widget for label, widget in fields if label == "Category")
        for category in categories:
            category_id, category_name = category  # Adjust depending on actual tuple structure
            category_combo.addItem(category_name, category_id)

        # Fetch and populate addresses
        addresses = IadminPageBack.fetch_address()
        address_combo = next(widget for label, widget in fields if label == "Address")
        for address in addresses:
            address_id, address_name = address  # Adjust depending on actual tuple structure
            address_combo.addItem(address_name, address_id)

        


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
        def save_customer():
            categ_id = category_combo.currentData()
            address_id = address_combo.currentData()

            input_values = {}
            for label, widget in fields:
                if isinstance(widget, QtWidgets.QLineEdit):
                    input_values[label] = widget.text().strip()
                elif isinstance(widget, QtWidgets.QComboBox):
                    input_values[label] = widget.currentText().strip()

            # Validate required fields
            missing_fields = []
            for label, widget in fields:
                if label == "Middle Name":
                    continue  # skip optional field

                if isinstance(widget, QtWidgets.QLineEdit) and not widget.text().strip():
                    missing_fields.append(label)
                elif isinstance(widget, QtWidgets.QComboBox) and widget.currentText().strip() == "":
                    missing_fields.append(label)

            if missing_fields:
                QtWidgets.QMessageBox.warning(self, "Missing Fields", "Please fill in all the required fields.")
                return
            
            # Validate that name fields contain only letters
            name_fields = ["First Name", "Middle Name", "Last Name"]
            invalid_name_fields = []

            for label in name_fields:
                widget = dict(fields)[label]
                widget.setStyleSheet(input_style)  # Reset style before validating
                widget.setToolTip("")              # Clear previous tooltips
                name_text = widget.text().strip()
                
                if name_text and not name_text.replace(" ", "").isalpha():
                    invalid_name_fields.append(label)
                    widget.setStyleSheet(f"{input_style} border: 2px solid red;")
                    widget.setToolTip(f"{label} must contain letters only")

            if invalid_name_fields:
                QtWidgets.QMessageBox.warning(
                    self,
                    "Error",
                    f"This fields must contain letters only: {', '.join(invalid_name_fields)}"
                )
                return


            contact_str = input_values["Contact Number"]
            try:
                contact = float(contact_str) if contact_str else None
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "Contact Number must be a valid number.")
                return
            
            # Handle meter reading conversion
            reading_str = input_values["First Reading"]
            try:
                meter_reading = float(reading_str) if reading_str else None
            except ValueError:
                QtWidgets.QMessageBox.warning(self, "Error", "First Reading must be a number.")
                return

            # Add meter
            IadminPageBack = adminPageBack()
            meter_id = IadminPageBack.add_meter(meter_reading, input_values["Serial Number"])

            # Add customer
            new_client_id = IadminPageBack.add_client(
                client_name=input_values["First Name"],
                client_lname=input_values["Last Name"],
                client_contact_num=input_values["Contact Number"],
                client_location=input_values["Location"],
                meter_id=meter_id,
                address_id= address_id,
                categ_id= category_id,
                client_mname=input_values["Middle Name"],
                status="Active"
            )

            QtWidgets.QMessageBox.information(self, "Success", "Customer added successfully.")
            add_dialog.accept()

            # Refresh the customer list
            updated_data = IadminPageBack.fetch_clients()
            self.populate_table(updated_data)

        save_btn.clicked.connect(save_customer)

        


        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        # Show dialog
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
    window = AdminCustomersPage()
    window.show()
    sys.exit(app.exec_())
