import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.adminBack import adminCustomerPageBack

class AdminWorkersPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("WORKERS LIST")
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
        self.search_criteria.addItems(["ID", "Name", "Username"])
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
        self.search_input.setPlaceholderText("Search workers...")
        
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
        
        self.search_input.textChanged.connect(self.filter_table)
        
        # Add widgets to container
        search_container.addWidget(self.search_input)
        
        # Connect search criteria change
        self.search_criteria.currentTextChanged.connect(self.toggle_search_input)
        
        search_add_layout.addLayout(search_container)
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD WORKERS", icon=QtGui.QIcon("images/add.png"))
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
        add_btn.clicked.connect(self.show_add_workers_page)
        search_add_layout.addWidget(add_btn)
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)  



        # Table setup
        self.workers_table = QtWidgets.QTableWidget()
        self.workers_table.verticalHeader().setVisible(False)
        self.workers_table.setStyleSheet("""
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
        
        # Set up columns (10 columns)
        self.workers_table.setColumnCount(5)
        self.workers_table.setHorizontalHeaderLabels([
            "ID", "NAME", "USERNAME", "PASSWORD", "ROLE",
        ])
        
        customer_back = adminCustomerPageBack()
        data = customer_back.fetch_customers('user')
        
        self.populate_table(data)
        
        # Adjust table properties
        self.workers_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.workers_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.workers_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.workers_table)


    def populate_table(self, data):
        self.workers_table.setRowCount(len(data))
        
        for row, workers in enumerate(data):
            # Unpack all values (now expecting 11 values in the customer tuple)
            user_id, name, username, password  = workers

            # Add customer data to the table
            self.customers_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(user_id)))
            self.customers_table.setItem(row, 1, QtWidgets.QTableWidgetItem(name))
            self.customers_table.setItem(row, 2, QtWidgets.QTableWidgetItem(username))
            self.customers_table.setItem(row, 3, QtWidgets.QTableWidgetItem(password))


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

    def show_add_workers_page(self):
        # Create dialog instead of widget
        add_dialog = QtWidgets.QDialog(self)
        add_dialog.setWindowTitle("Add New Workers")
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
            ("NAME", QtWidgets.QLineEdit()),
            ("USERNAME", QtWidgets.QLineEdit()),
            ("PASSWORD", QtWidgets.QLineEdit()),
        ]
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
    window = AdminWorkersPage()
    window.show()
    sys.exit(app.exec_())
