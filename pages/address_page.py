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
        
        IadminPageBack = adminPageBack()

        
        self.populate_table(IadminPageBack.fetch_address()
)
        
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
            toggle_button.setProperty("address_id", address_id)
            toggle_button.pressed.connect(lambda r=row, lbl=status_label: self.toggle_status(r, lbl))

            # Add label and button to layout
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            status_layout.addWidget(toggle_button)

            # Set the layout into a QWidget
            status_container = QtWidgets.QWidget()
            status_container.setLayout(status_layout)
            self.address_table.setCellWidget(row, 2, status_container)
            
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
                address_id = toggle_button.property("address_id")
                IadminPageBack = adminPageBack()
                address_info = IadminPageBack.get_address_by_id(address_id)
                current_status = address_info[2]  # 'Active' or 'Inactive'
                next_status = 'Inactive' if current_status == 'Active' else 'Active'

                # Block signals
                toggle_button.blockSignals(True)

                # Confirm toggle
                reply = QMessageBox.question(
                    self,
                    "Confirm Status Change",
                    f"Are you sure you want to change the status to {next_status}?",
                    QMessageBox.Yes | QMessageBox.No
                )

                if reply == QMessageBox.Yes:
                    # Update DB
                    IadminPageBack.toggle_address_status(address_id, next_status)

                    # Update label and toggle state
                    label.setText(next_status)
                    label.setStyleSheet(f"color: {'#4CAF50' if next_status == 'Active' else '#E57373'}; font-weight: bold;")
                    toggle_button.setChecked(next_status == "Active")
                else:
                    # Keep original state
                    toggle_button.setChecked(current_status == "Active")

                toggle_button.blockSignals(False)
               


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = AddressPage()
    window.show()
    sys.exit(app.exec_())
