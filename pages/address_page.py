import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMessageBox

from backend.adminBack import adminPageBack

class AddressPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Header with title and search
        header_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("ADDRESS LIST")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        header_layout.addWidget(title)
        header_layout.addStretch()

        search_add_layout = QtWidgets.QHBoxLayout()
        
        # Search container
        search_container = QtWidgets.QHBoxLayout()
        
        # Search input
        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search address by name...")
        
        # Apply same styling to both widgets
        input_style = """
            QLineEdit {
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
        
        header_layout.addLayout(search_add_layout)
        layout.addLayout(header_layout)


        # Table setup
        self.address_table = QtWidgets.QTableWidget()
        self.address_table.setAlternatingRowColors(True)
        self.address_table.setStyleSheet("""
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
        self.address_table.setColumnCount(3)
        self.address_table.verticalHeader().setVisible(False)
        self.address_table.setHorizontalHeaderLabels([
            "NAME", "DATE", "STATUS"
        ])
        
        address_back = adminPageBack()
        data = address_back.fetch_address()
        
        self.populate_table(data)
        
        # Adjust table properties
        self.address_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.address_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.address_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        
        layout.addWidget(self.address_table)


    def populate_table(self, data):
        self.address_table.setRowCount(0)
        self.address_table.setRowCount(len(data))

        for row, address in enumerate(data):
            address_id, address_name, address_status, address_date = address

            self.address_table.setItem(row, 0, QtWidgets.QTableWidgetItem(address_name))
            self.address_table.setItem(row, 1, QtWidgets.QTableWidgetItem(str(address_date)))

             # Create status layout with label + toggle button
            status_layout = QtWidgets.QHBoxLayout()
            status_layout.setContentsMargins(5, 0, 5, 0)

            # Status label
            status_label = QtWidgets.QLabel(address_status)
            status_label.setStyleSheet(f"color: {'#4CAF50' if address_status == 'Active' else '#E57373'}; font-weight: bold;")

            # Toggle button for status
            toggle_button = QtWidgets.QPushButton()
            toggle_button.setCheckable(True)
            toggle_button.setChecked(address_status == "Active")
            toggle_button.setFixedSize(40, 20)
            toggle_button.setStyleSheet("""
                QPushButton {
                    background-color: red;
                    border: 1px solid #aaa;
                    border-radius: 10px;
                }
                QPushButton:checked {
                    background-color: green;
                }
            """)
            toggle_button.pressed.connect(lambda r=row, lbl=status_label: self.toggle_status(r, lbl))

            # Add label and button to layout
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            status_layout.addWidget(toggle_button)

            # Set the layout into a QWidget
            status_container = QtWidgets.QWidget()
            status_container.setLayout(status_layout)
            self.address_table.setCellWidget(row, 2, status_container)

 
    def show_add_address_page(self):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("New Address")
        dialog.setFixedSize(600, 300)
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
        title = QtWidgets.QLabel("ADDRESS INFORMATION FORM")
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
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        def create_labeled_widget(label_text, widget):
            v_layout = QtWidgets.QVBoxLayout()
            label = QtWidgets.QLabel(label_text)
            label.setFont(QtGui.QFont("Arial", 10))
            v_layout.addWidget(label)
            v_layout.addWidget(widget)
            return v_layout

        address_name = QtWidgets.QLineEdit()
        address_name.setStyleSheet(input_style)

        form_layout.addLayout(create_labeled_widget("ADDRESS NAME:", address_name), 0, 0)

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
        cancel_btn.clicked.connect(dialog.reject)

        # Save Button
        save_btn = QtWidgets.QPushButton("Save")
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



    def show_edit_address_page(self, row):
        address_id = self.address_table.item(row, 0).text()
        current_name = self.address_table.item(row, 1).text()

        edit_dialog = QtWidgets.QDialog(self)
        edit_dialog.setWindowTitle("Edit Address")
        edit_dialog.setModal(True)
        edit_dialog.setFixedSize(500, 250)
        edit_dialog.setStyleSheet("""
            QDialog {
                background-color: #C9EBCB;
            }
            QLabel {
                font-family: 'Arial', sans-serif;
                font-weight: bold;
            }
        """)

        layout = QtWidgets.QVBoxLayout(edit_dialog)
        layout.setContentsMargins(30, 20, 30, 20)
        layout.setSpacing(10)

        title = QtWidgets.QLabel("EDIT ADDRESS")
        title.setStyleSheet("""
            font-size: 20px;
            padding: 10px;
        """)
        title.setAlignment(QtCore.Qt.AlignCenter)
        layout.addWidget(title)

        form_layout = QtWidgets.QVBoxLayout()
        form_layout.setSpacing(20)

        input_style = """
            QLineEdit {
                font-family: 'Arial';
                font-size: 14px;
                padding: 8px;
                border: 1px solid #bdc3c7;
                border-radius: 4px;
                background-color: #ffffff;
            }
        """

        label = QtWidgets.QLabel("ADDRESS NAME:")
        label.setFont(QtGui.QFont("Arial", 10))

        name_input = QtWidgets.QLineEdit(current_name)
        name_input.setStyleSheet(input_style)

        input_container = QtWidgets.QVBoxLayout()
        input_container.addWidget(label)
        input_container.addWidget(name_input)

        form_layout.addLayout(input_container)
        layout.addLayout(form_layout)
        layout.addStretch()

        # Buttons container
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
        cancel_btn.clicked.connect(edit_dialog.reject)

        save_btn = QtWidgets.QPushButton("Save")
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

        edit_dialog.exec_()



    def deactivate_address(self, row):
        address_id = self.address_table.item(row, 0).text()
        # Show confirmation
        reply = QtWidgets.QMessageBox.question(self, 'Deactivate Address', 
                f"Are you sure you want to deactivate address ID {address_id}?",
                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)


    def toggle_search_input(self, text):
            if text == "Category":
                self.search_input.hide()
                self.search_input_combo.show()
            else:
                self.search_input.show()
                self.search_input_combo.hide() 

    def filter_table(self, text):
        # Filter rows based on the search text
        for row in range(self.address_table.rowCount()):
            item = self.address_table.item(row, 0)  # Look at the 'NAME' column (index 1)
            if item:
                address_name = item.text().lower()
                if text.lower() in address_name:
                    self.address_table.setRowHidden(row, False)  # Show row if name matches
                else:
                    self.address_table.setRowHidden(row, True)  # Hide row if name doesn't match
                

    def toggle_status(self, row, label):
        table = self.address_table
        container = table.cellWidget(row, 2)
        if container:
            toggle_button = container.findChild(QtWidgets.QPushButton)
            if toggle_button:
                # Store the current status before the button toggles
                current_status = toggle_button.isChecked()
                next_status = not current_status
                next_status_label = "Active" if next_status else "Inactive"

                # Block the toggle signal to prevent automatic state change
                toggle_button.blockSignals(True)

                # Ask for confirmation
                reply = QMessageBox.question(
                    self,
                    "Confirm Status Change",
                    f"Are you sure you want to change the status to {next_status_label}?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    # Change the status and apply label styles
                    toggle_button.setChecked(next_status)
                    if next_status:
                        label.setText("Active")
                        label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                    else:
                        label.setText("Inactive")
                        label.setStyleSheet("color: #E57373; font-weight: bold;")
                else:
                    # Revert the button's checked state to the original state
                    toggle_button.setChecked(current_status)

                # Re-enable the signal after handling
                toggle_button.blockSignals(False)                 


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddressPage()
    window.show()
    sys.exit(app.exec_())
