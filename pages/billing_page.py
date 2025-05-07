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

        # Define input style at the beginning
        input_style = """
            QLineEdit, QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
            }
        """

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
        """)
        search_container.addWidget(self.search_criteria)
        
        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search billings...")
        self.search_input.setStyleSheet(input_style)
        search_container.addWidget(self.search_input)
        
        # Add search container to search_add_layout
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
        add_btn.clicked.connect(self.show_add_billing)
        search_add_layout.addWidget(add_btn)
        
        # Add search_add_layout to header_layout
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)
        
        # Create billing table before accessing it
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
            "BILLING CODE", "ISSUED DATE", "BILLING DUE", "CLIENT ID", 
            "CLIENT NAME", "CLIENT LOCATION", "BILLING TOTAL", "STATUS"
        ])

        billing_back = adminPageBack()
        data = billing_back.fetch_billing()
        
        self.populate_table(data)

        # Now we can safely adjust table properties
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
                if search_by == "BILLING CODE":
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
        reading_date.setMaximumDate(QtCore.QDate.currentDate())
        reading_date.setDate(QtCore.QDate.currentDate())  # Set current date as default
         

        previous_reading = QtWidgets.QLineEdit()
        previous_reading.setReadOnly(True)
        previous_reading.setStyleSheet(readonly_style)

        present_reading = QtWidgets.QLineEdit()
        present_reading.setEnabled(False)
        present_reading.setStyleSheet(readonly_style)

        cubic_meter_consumed = QtWidgets.QLineEdit()
        cubic_meter_consumed.setReadOnly(True)
        cubic_meter_consumed.setStyleSheet(readonly_style)

        amount = QtWidgets.QLineEdit()
        amount.setReadOnly(True)
        amount.setStyleSheet(readonly_style)

        due_date = QtWidgets.QDateEdit()
        due_date.setCalendarPopup(True)
        due_date.setStyleSheet(input_style)
        due_date.setMinimumDate(QtCore.QDate.currentDate())

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

        #Completer for client ComboBox
        completer = QtWidgets.QCompleter(client_entries)
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        completer.setFilterMode(QtCore.Qt.MatchContains)
        client.setCompleter(completer)

        client.setCurrentText("Select Client")

        def update_total_bill():
            try:
                amt_text = amount.text().strip()
                charge_text = total_charge.text().strip()

                amt = float(amt_text) if amt_text else 0
                charge = float(charge_text) if charge_text else 0

                total = amt + charge
                total_bill.setText(f"{total:.2f}")
            except ValueError:
                total_bill.setText("0.00")


        #connect signal to handle selection changes
        def on_client_selected(index):
            selected_id = client.itemData(index)
            if selected_id is None:
                present_reading.setEnabled(False)
                present_reading.setStyleSheet(readonly_style)
                return
            IadminPageBack = adminPageBack()
            client_info = IadminPageBack.fetch_client_by_id(selected_id)[0] # get client info by id
            meter_id = client_info[5] # meter id
            client_categ_id = client_info[7] # category id
            previous_reading.setText(str(IadminPageBack.fetch_meter_by_id(meter_id)[0][1])) # get previous reading from meter id
            # Fetch rate blocks
            #self.rate_blocks = IadminPageBack.fetch_rate_blocks_by_categ(client_categ_id)
            self.rate_blocks = [
                    (123,True, 0, 10, None,111, 150.0),                # Minimum charge for 0–10 cu.m.
                    (123,False, 10, 20, 16.50,111, None),                   # 11–20 cu.m.
                    (123,False, 20, 30, 18.70,111, None),                   # 21–30 cu.m.
                    (123,False, 30, 40, 21.70,111, None),                   # 31–40 cu.m.
                    (123,False, 40, 50, 25.50,111, None),                   # 41–50 cu.m.
                    (123,False, 50, None, 30.00,111, None),                 # 51+ cu.m.
                ] # tanggala ning self.rate_blocks kung napagana na nimo ang kanang self.rate_blocks sa taas nga nigamit og IadminPageBack
                # naka set up nasad ko didto og function para ana mao sad na nga ngalan palihug lang sad ko pasa og import sa repo ani than
                # sa mga existing lang nga functions pag base dali raman to mura rag pasa pasa nmos repo og controller


            # Store categ_id for use in bill creation
            self.categ_id = client_categ_id
            present_reading.setEnabled(True)
            present_reading.setStyleSheet(input_style)
            

        client.currentIndexChanged.connect(on_client_selected)

        def on_present_reading_changed():
            try:
                prev = float(previous_reading.text())
                pres = float(present_reading.text())
                if pres < prev:
                    cubic_meter_consumed.setText("0")
                    amount.setText("0.00")
                    return

                consumed = pres - prev
                cubic_meter_consumed.setText(str(consumed))

                total_amount = 0
                has_applied_minimum = False

                for block in self.rate_blocks:
                    is_minimum = block[1]           # bool: True if it's the minimum block
                    min_c = block[2]                # min cubmic meter for this block (None if is_minimum)
                    max_c = block[3] if block[3] is not None else float('inf') # max cubic meter for this block (None if is_minimum)
                    rate = block[4]                 # rate per cu.m (None if is_nimum)
                    fixed_fee = block[6]            # fixed fee for is_minimum (None if not is_minimum)

                    if is_minimum and consumed > 0 and not has_applied_minimum:
                        total_amount += fixed_fee
                        has_applied_minimum = True

                    elif not is_minimum and consumed > min_c:
                        applied_volume = max(0, min(consumed, max_c) - min_c)
                        total_amount += applied_volume * rate

                amount.setText(f"{total_amount:.2f}")
                update_total_bill()

            except ValueError:
                cubic_meter_consumed.setText("0")
                amount.setText("0.00")

        present_reading.textChanged.connect(on_present_reading_changed)

        def update_total_charge():
            try:
                sub = float(subscribe_capital.text()) if subscribe_capital.text() else 0
                late = float(late_payment.text()) if late_payment.text() else 0
                pen = float(penalty.text()) if penalty.text() else 0
                total = sub + late + pen
                total_charge.setText(f"{total:.2f}")
                update_total_bill()
            except ValueError:
                total_charge.setText("0.00")
        
        subscribe_capital.textChanged.connect(update_total_charge)
        late_payment.textChanged.connect(update_total_charge)
        penalty.textChanged.connect(update_total_charge)

        def validate_billing_data():
                error_style = """
                    QLineEdit, QDateEdit, QComboBox {
                        padding: 8px;
                        border: 1px solid red;
                        border-radius: 4px;
                        font-family: 'Roboto', sans-serif;
                        min-width: 250px;
                    }
                """
                normal_style = input_style
                errors = []
                has_empty_fields = False
                
                # Reset all styles
                for widget in [client, reading_date, present_reading, due_date, 
                              subscribe_capital, late_payment, penalty]:
                    widget.setStyleSheet(normal_style)
                
                # Check for empty fields first
                if client.currentData() is None:
                    client.setStyleSheet(error_style)
                    has_empty_fields = True
                
                if not present_reading.text().strip():
                    present_reading.setStyleSheet(error_style)
                    has_empty_fields = True
                
                for field in [subscribe_capital, late_payment, penalty]:
                    if not field.text().strip():
                        field.setStyleSheet(error_style)
                        has_empty_fields = True
                
                if has_empty_fields:
                    msg = QtWidgets.QMessageBox(dialog)
                    msg.setWindowTitle("Validation Error")
                    msg.setText("All fields are needed to be filled")
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setStyleSheet("QMessageBox { background-color: white; }")
                    msg.exec_()
                    return False
                
                # Continue with other validations only if no empty fields
                try:
                    prev = float(previous_reading.text() or 0)
                    pres = float(present_reading.text() or 0)
                    if pres <= prev:
                        present_reading.setStyleSheet(error_style)
                        errors.append("\nPresent reading must be greater than previous reading\n")
                except ValueError:
                    present_reading.setStyleSheet(error_style)
                    errors.append("\nInvalid present reading value\n")
                
                if reading_date.date() > QtCore.QDate.currentDate():
                    reading_date.setStyleSheet(error_style)
                    errors.append("\nReading date cannot be in the future\n")
                
                if due_date.date() <= reading_date.date():
                    due_date.setStyleSheet(error_style)
                    errors.append("\nDue date must be after reading date\n")
                
                # Additional charges validation for non-empty fields
                for field, field_name in [(subscribe_capital, "Subscribe Capital"), 
                                        (late_payment, "Late Payment"), 
                                        (penalty, "Penalty")]:
                    try:
                        value = float(field.text())
                        if value < 0:
                            field.setStyleSheet(error_style)
                            errors.append(f"\n{field_name} cannot be negative\n")
                    except ValueError:
                        field.setStyleSheet(error_style)
                        errors.append(f"\nInvalid {field_name} amount\n")
                
                if errors:
                    msg = QtWidgets.QMessageBox(dialog)
                    msg.setWindowTitle("Validation Error")
                    msg.setText("\n\n".join(errors))
                    msg.setIcon(QtWidgets.QMessageBox.Warning)
                    msg.setStyleSheet("QMessageBox { background-color: white; }")
                    msg.exec_()
                    return False
                return True

        def save_bill():
                if not validate_billing_data():
                        return
                try:
                    
                    #backend style
                    #kung kani imo gamiton make sure lang sad nga dapat masave sila tulo dungan walay usa ma fail
                    # akong paabot sat ulo kay ang create reading, create billing, update meter sa iyang reading og last reading date
                    client_id = client.currentData()  # get selected client_id from comboBox
                    prev_read = float(previous_reading.text())
                    pres_read = float(present_reading.text())
                    read_date = reading_date.date().toPyDate()
                    meter_id = IadminPageBack.fetch_client_by_id(client_id)[0][5]  # get meter id from client id

                    reading_id = IadminPageBack.add_reading(read_date, prev_read, pres_read, meter_id) # uncomment ig ready, himog add reading nga function nya e return ang reading id, paki edit nlng pd sa adminback para matest nmo
                    IadminPageBack.update_meter_latest_reading(pres_read, read_date, meter_id) # uncomment sad ig ready, bali maupdate ang last reading sa meter og ang last reading date
                    billing_data = {
                        "billing_due": due_date.date().toPyDate(),
                        "billing_total": float(total_bill.text()) if total_bill.text() else 0,
                        "billing_consumption": float(cubic_meter_consumed.text()) if cubic_meter_consumed.text() else 0,
                        "reading_id": reading_id, # ilisi ang none og reading id kung successfully maka create na
                        "client_id": client_id,
                        "categ_id": self.categ_id,
                        "billing_date": read_date,
                        "billing_status": "TO BE PRINTED",
                        "billing_amount": float(amount.text()) if amount.text() else 0,
                        "billing_sub_capital": float(subscribe_capital.text()) if subscribe_capital.text() else 0,
                        "billing_late_payment": float(late_payment.text()) if late_payment.text() else 0,
                        "billing_penalty": float(penalty.text()) if penalty.text() else 0,
                        "billing_total_charge": float(total_charge.text()) if total_charge.text() else 0
                    }

                    print("READY TO SAVE:", billing_data) # testing rani para check if naget ba ang tanan
                    print(pres_read)
                    IadminPageBack.add_billing(billing_data['billing_due'],
                                            billing_data['billing_total'],
                                            billing_data['billing_consumption'],
                                            billing_data['reading_id'],
                                            billing_data['client_id'],
                                            billing_data['categ_id'],
                                            billing_data['billing_date'],
                                            billing_data['billing_status'],
                                            billing_data['billing_amount'],
                                            billing_data['billing_sub_capital'],
                                            billing_data['billing_late_payment'],
                                            billing_data['billing_penalty'],
                                            billing_data['billing_total_charge'],) # tanggala ang comment kung ready na ang billing repo


                    QtWidgets.QMessageBox.information(dialog, "Success", "Billing information saved successfully.")
                    dialog.accept()
                    updated_data = IadminPageBack.fetch_billing()
                    self.populate_table(updated_data)

                #maka update bisag error
                except Exception as e:
                    QtWidgets.QMessageBox.warning(dialog, "Error", f"Failed to save billing: {str(e)}")

        save_btn.clicked.connect(save_bill)

            
            


        dialog.exec_()
        

          


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = EmployeeBillingPage()
    window.show()
    sys.exit(app.exec_())
