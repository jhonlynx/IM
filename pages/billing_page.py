import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets

from backend.adminBack import adminPageBack

class EmployeeBillingPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("BILLING LIST")
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
        self.search_criteria.addItems(["BILLING CODE", "CLIENT NAME", "CLIENT LOCATION"])
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
        self.search_input.setPlaceholderText("Search billings...")
        
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
        
        
        search_add_layout.addLayout(search_container)
        
        # Add button with icon
        add_btn = QtWidgets.QPushButton("ADD BILLING", icon=QtGui.QIcon("images/add.png"))
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
        # add_btn.clicked.connect(self.show_add_billing)
        add_btn.clicked.connect(self.show_add_billing)
        search_add_layout.addWidget(add_btn)
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)  



        # Billing Table
        self.billing_table = QtWidgets.QTableWidget()
        self.billing_table.setAlternatingRowColors(True)
        self.billing_table.setStyleSheet("""
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
        
        # Set up table columns
        self.billing_table.setColumnCount(8)
        self.billing_table.setHorizontalHeaderLabels([
            "BILLING CODE", "ISSUED DATE", "BILLING DUE", "CLIENT ID", "CLIENT NAME", "CLIENT LOCATION", "BILLING TOTAL", "STATUS"
        ])

        billing_back = adminPageBack()
        data = billing_back.fetch_billing()
        
        self.populate_table(data)

        
        # Adjust table properties
        self.billing_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.billing_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.billing_table.verticalHeader().setVisible(False)
        self.billing_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.billing_table)


    def populate_table(self, data):
        self.billing_table.setRowCount(len(data))
        
        for row, billings  in enumerate(data):
            # Unpack all values (now expecting 11 values in the customer tuple)
            billing_code, issued_date, billing_due, client_id, client_name, client_location, billing_total, status = billings

            # Add customer data to the table
            self.billing_table.setItem(row, 0, QtWidgets.QTableWidgetItem(str(billing_code))),
            self.billing_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(issued_date))),
            self.billing_table.setItem(row, 2, QtWidgets.QTableWidgetItem(str(billing_due))),
            self.billing_table.setItem(row, 3, QtWidgets.QTableWidgetItem(str(client_id))),
            self.billing_table.setItem(row, 4, QtWidgets.QTableWidgetItem(client_name)),
            self.billing_table.setItem(row, 5, QtWidgets.QTableWidgetItem(client_location)),
            self.billing_table.setItem(row, 6, QtWidgets.QTableWidgetItem(str(billing_total)))
            self.billing_table.setItem(row, 7, QtWidgets.QTableWidgetItem(status))

            # Status with color coding
            status_item = QtWidgets.QTableWidgetItem(status)
            status_item.setForeground(
                QtGui.QColor("#64B5F6") if status == "PAID" else QtGui.QColor("#E57373")
            )
            self.billing_table.setItem(row, 7, status_item)



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
        search_text = self.search_input.text().lower()

        for row in range(self.billing_table.rowCount()):
            match = False
            if search_text:
                if search_by == "BILLING ID":
                    item = self.billing_table.item(row, 0)
                elif search_by == "CLIENT ID":
                    item = self.billing_table.item(row, 3)
                elif search_by == "CLIENT NAME":
                    item = self.billing_table.item(row, 4)
                elif search_by == "CLIENT LOCATION":
                    item = self.billing_table.item(row, 5)    

                if item and search_text in item.text().lower():
                    match = True
            else:
                match = True

            self.billing_table.setRowHidden(row, not match)


    def show_add_billing(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("Add New Bill")
        dialog.setFixedSize(1000, 700)
        dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)
        
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.setContentsMargins(30, 5, 30, 5)
        layout.setSpacing(10)

        # Section Title
        title = QtWidgets.QLabel("BILLING INFORMATION FORM")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        # Form Layout
        form_layout = QtWidgets.QGridLayout()
        form_layout.setHorizontalSpacing(40)
        form_layout.setVerticalSpacing(20)

        input_style = """
            QLineEdit, QDateEdit, QComboBox {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        readonly_style = """
        QLineEdit {
            font-family: 'Arial';
            font-size: 14px;
            padding: 8px;
            border: 1px solid #bdc3c7;
            border-radius: 4px;
            background-color: #e0e0e0;
            color: #555555;
        }
    """


        # --- LEFT COLUMN ---

        def create_labeled_widget(label_text, widget):
            layout = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            layout.addWidget(label)
            layout.addWidget(widget)
            return layout

        
        client = QtWidgets.QComboBox()
        client.setStyleSheet(input_style)

        reading_date = QtWidgets.QDateEdit()
        reading_date.setCalendarPopup(True)
        reading_date.setStyleSheet(input_style)

        previous_reading = QtWidgets.QLineEdit()
        previous_reading.setStyleSheet(input_style)
        previous_reading.setReadOnly(True)
        previous_reading.setStyleSheet(readonly_style)

        present_reading = QtWidgets.QLineEdit()
        present_reading.setStyleSheet(input_style)

        cubic_meter_consumed = QtWidgets.QLineEdit()
        cubic_meter_consumed.setStyleSheet(input_style)
        cubic_meter_consumed.setReadOnly(True)
        cubic_meter_consumed.setStyleSheet(readonly_style)

        amount = QtWidgets.QLineEdit()
        amount.setStyleSheet(input_style)
        amount.setReadOnly(True)
        amount.setStyleSheet(readonly_style)

        due_date = QtWidgets.QDateEdit()
        due_date.setCalendarPopup(True)
        due_date.setStyleSheet(input_style)
        


        form_layout.addLayout(create_labeled_widget("CLIENT:", client), 0, 0)
        form_layout.addLayout(create_labeled_widget("READING DATE:", reading_date), 1, 0)
        form_layout.addLayout(create_labeled_widget("PREVIOUS READING:", previous_reading), 2, 0)
        form_layout.addLayout(create_labeled_widget("PRESENT READING:", present_reading), 3, 0)
        form_layout.addLayout(create_labeled_widget("CUBIC METER CONSUMED:", cubic_meter_consumed), 4, 0)
        form_layout.addLayout(create_labeled_widget("AMOUNT:", amount), 5, 0)
        form_layout.addLayout(create_labeled_widget("DUE DATE:", due_date), 6, 0)

                
        IadminPageBack = adminPageBack()

        client.setEditable(True)
        client.setInsertPolicy(QtWidgets.QComboBox.NoInsert)
        client.setStyleSheet(input_style)
        client.lineEdit().setReadOnly(False)

        client_entries = []
        client_data_map = {}

        clients = IadminPageBack.fetch_clients()
        client.clear()

        # Populate client ComboBox
        for client_data in clients:
            client_id = client_data[0]
            client_number = client_data[1]
            first_name = client_data[2]
            last_name = client_data[4]
            display_text = f"{client_number} - {first_name} {last_name}"
            client.addItem(display_text, client_id)
            client_entries.append(display_text)
            client_data_map[display_text] = client_id

        # ✅ Just use QCompleter
        completer = QtWidgets.QCompleter(client_entries)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        client.setCompleter(completer)



        # Bold centered section header
        additional_charge_label = QtWidgets.QLabel("ADDITIONAL CHARGE")
        font = QtGui.QFont()
        font.setBold(True)
        font.setPointSize(11)
        additional_charge_label.setFont(font)
        additional_charge_label.setAlignment(QtCore.Qt.AlignCenter)
        form_layout.addWidget(additional_charge_label, 0, 1)

        subscribe_capital = QtWidgets.QLineEdit()
        subscribe_capital.setStyleSheet(input_style)

        late_payment = QtWidgets.QLineEdit()
        late_payment.setStyleSheet(input_style)

        penalty = QtWidgets.QLineEdit()
        penalty.setStyleSheet(input_style)

        total_charge = QtWidgets.QLineEdit()
        total_charge.setStyleSheet(input_style)
        total_charge.setReadOnly(True)
        total_charge.setStyleSheet(readonly_style)

        total_bill = QtWidgets.QLineEdit()
        total_bill.setStyleSheet(input_style)
        total_bill.setReadOnly(True)
        total_bill.setStyleSheet(readonly_style)

        form_layout.addLayout(create_labeled_widget("SUBSCRIBE CAPITAL:", subscribe_capital), 1, 1)
        form_layout.addLayout(create_labeled_widget("LATE PAYMENT:", late_payment), 2, 1)
        form_layout.addLayout(create_labeled_widget("PENALTY:", penalty), 3, 1)
        form_layout.addLayout(create_labeled_widget("TOTAL CHARGE:", total_charge), 4, 1)
        form_layout.addLayout(create_labeled_widget("TOTAL BILL:", total_bill), 6, 1)

        # Add form_layout to main layout
        layout.addLayout(form_layout)


        # Button Container
        button_container = QtWidgets.QWidget()
        button_layout = QtWidgets.QHBoxLayout(button_container)
        button_layout.setAlignment(QtCore.Qt.AlignRight)

        # Cancel Button
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

        # Save Button
        save_btn = QtWidgets.QPushButton("Save Bill")
        save_btn.setStyleSheet("""
            QPushButton {
                background-color: #27ae60;
                color: white;
                padding: 8px 15px;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 100px;
            }
            QPushButton:hover {
                background-color: #219a52;
            }
        """)

        button_layout.addWidget(cancel_btn)
        button_layout.addWidget(save_btn)
        layout.addWidget(button_container)

        dialog.exec_() 

          


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EmployeeBillingPage()
    window.show()
    sys.exit(app.exec_())
