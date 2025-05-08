import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PyQt5 import QtCore, QtGui, QtWidgets
from backend.adminBack import adminPageBack


class TransactionsPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.showMaximized()

    def create_scrollable_cell(self, row, column, text):
        scrollable_widget = ScrollableTextWidget(text)
        self.transaction_table.setCellWidget(row, column, scrollable_widget)
        
    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        # Create a header panel with some padding
        header_panel = QtWidgets.QWidget()
        header_panel.setStyleSheet("background-color: #f5f5f5; border-bottom: 1px solid #ddd;")
        header_layout = QtWidgets.QVBoxLayout(header_panel)
        header_layout.setContentsMargins(20, 15, 20, 15)
        
        # Header with title, search bar, and dropdown
        controls_layout = QtWidgets.QHBoxLayout()
        title = QtWidgets.QLabel("TRANSACTIONS")
        title.setStyleSheet("""
            font-family: 'Montserrat', sans-serif;
            font-size: 24px;
            font-weight: bold;
        """)
        controls_layout.addWidget(title)
        controls_layout.addStretch()

        # Search container
        search_container = QtWidgets.QHBoxLayout()

        self.filter_combo = QtWidgets.QComboBox()
        self.filter_combo.addItems(["Transaction Number", "Client Name", "Employee", "Date"])
        self.filter_combo.setStyleSheet("""
            QComboBox {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 150px;
                background-color: white;
            }
        """)
        search_container.addWidget(self.filter_combo)

        self.search_input = QtWidgets.QLineEdit()
        self.search_input.setPlaceholderText("Search transactions...")
        self.search_input_date = QtWidgets.QDateEdit()
        self.search_input_date.setCalendarPopup(True)
        self.search_input_date.hide()

        input_style = """
            QLineEdit, QDateEdit {
                padding: 8px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
                min-width: 250px;
                background-color: white;
            }
        """
        self.search_input.setStyleSheet(input_style)
        self.search_input_date.setStyleSheet(input_style)

        search_container.addWidget(self.search_input)
        search_container.addWidget(self.search_input_date)

        self.filter_combo.currentTextChanged.connect(self.toggle_search_input)
        self.search_input.textChanged.connect(self.filter_table)
        self.search_input_date.dateChanged.connect(self.filter_table)

        controls_layout.addLayout(search_container)

        # Transaction type dropdown
        self.transaction_type_combo = QtWidgets.QComboBox()
        self.transaction_type_combo.addItems(["All Transactions", "Daily Transaction", "Monthly Transaction"])
        self.transaction_type_combo.setStyleSheet("""
            QComboBox {
                padding: 6px;
                border: 1px solid #ccc;
                border-radius: 4px;
                font-family: 'Roboto', sans-serif;
            }
        """)
        self.transaction_type_combo.currentIndexChanged.connect(self.switch_table)
        controls_layout.addWidget(self.transaction_type_combo)
        
        header_layout.addLayout(controls_layout)
        layout.addWidget(header_panel)

        # Create table with horizontal scrollbar enabled - using all remaining space
        self.transaction_table = QtWidgets.QTableWidget()
        self.transaction_table.setAlternatingRowColors(True)
        self.transaction_table.setStyleSheet("""
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
            QTableWidget::item:selected {
                background-color: transparent;
                color: black;
            }
            QTableWidget::item:hover {
                background-color: transparent;
            }
        """)
        self.transaction_table.setColumnCount(9)
        self.transaction_table.setHorizontalHeaderLabels([
            "TRANSACTION NUMBER", "PAYMENT DATE", "CLIENT NUMBER", "CLIENT NAME", "EMPLOYEE", "CONSUMPTION", "AMOUNT", "DUE DATE", "STATUS"
        ])
        
        # Set the table to fill all available space
        self.transaction_table.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        self.transaction_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        
        # Enable horizontal scrollbar
        self.transaction_table.setHorizontalScrollMode(QtWidgets.QAbstractItemView.ScrollPerPixel)
        self.transaction_table.setWordWrap(False)
        

        IadminPageBack = adminPageBack()
        self.populate_table(IadminPageBack.fetch_transactions())
        
        self.transaction_table.setSelectionBehavior(QtWidgets.QTableWidget.SelectRows)
        self.transaction_table.setEditTriggers(QtWidgets.QTableWidget.NoEditTriggers)
        self.transaction_table.verticalHeader().setVisible(False)

        # Create a custom delegate for text elision with tooltip
        delegate = TextEllipsisDelegate(self.transaction_table)
        self.transaction_table.setItemDelegate(delegate)

        # Add table to the main layout with full expansion
        layout.addWidget(self.transaction_table)   

    def populate_table(self, data):   
        self.transaction_table.setRowCount(len(data))
        for row, transactions in enumerate(data):
            trans_code, trans_payment_date, client_number, client_name, user_name, billing_consumption, billing_total, billing_due, trans_status = transactions
            
            # For each cell that might have long text, create a custom widget with scrollable text
            self.create_scrollable_cell(row, 0, str(trans_code))
            self.create_scrollable_cell(row, 1, str(trans_payment_date))
            self.create_scrollable_cell(row, 2, str(client_number))
            self.create_scrollable_cell(row, 3, str(client_name))
            self.create_scrollable_cell(row, 4, str(user_name))
            self.create_scrollable_cell(row, 5, str(billing_consumption))
            self.create_scrollable_cell(row, 6, str(billing_total))
            self.create_scrollable_cell(row, 7, str(billing_due))

            # Create status layout with label + toggle button
            status_layout = QtWidgets.QHBoxLayout()
            status_layout.setContentsMargins(5, 0, 5, 0)

            # Status label
            status_label = QtWidgets.QLabel(trans_status)
            status_label.setStyleSheet(f"color: {'#4CAF50' if trans_status == 'PAID' else '#E57373'}; font-weight: bold;")
            
            # Toggle button
            toggle_button = QtWidgets.QPushButton()
            toggle_button.setCheckable(True)
            toggle_button.setChecked(trans_status == "PAID")
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
            toggle_button.clicked.connect(lambda checked, r=row, lbl=status_label: self.toggle_status(r, lbl))

            # Add label and button to layout
            status_layout.addWidget(status_label)
            status_layout.addStretch()
            status_layout.addWidget(toggle_button)

            # Set the layout into a QWidget
            status_container = QtWidgets.QWidget()
            status_container.setLayout(status_layout)
            self.transaction_table.setCellWidget(row, 8, status_container)

    def switch_table(self, index):
        self.filter_table()

    def toggle_search_input(self, text):
        if text == "Date":
            self.search_input.hide()
            self.search_input_date.show()
        else:
            self.search_input.show()
            self.search_input_date.hide()

    def filter_table(self):
        table = self.transaction_table
        filter_by = self.filter_combo.currentText()

        if filter_by == "Date":
            search_text = self.search_input_date.date().toString("yyyy-MM-dd").lower()
        else:
            search_text = self.search_input.text().lower()

        column_indices = {
            "Transaction Number": 0,
            "Client Name": 3,
            "Employee": 4,
            "Date": 1
        }
        column_index = column_indices.get(filter_by, 0)
        
        today = QtCore.QDate.currentDate()
        trans_type_index = self.transaction_type_combo.currentIndex()

        for row in range(table.rowCount()):
            match_search = False
            match_type = True

            # Handle both ScrollableTextWidget and regular items
            if column_index in [3, 4]:  # Client Name and Employee columns use ScrollableTextWidget
                cell_widget = table.cellWidget(row, column_index)
                if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                    item_text = cell_widget.text().lower()
                    match_search = search_text in item_text
            else:  # Other columns use regular QTableWidgetItem
                item = table.item(row, column_index)
                if item:
                    item_text = item.text().lower()
                    match_search = search_text in item_text if filter_by != "Date" else (search_text == item_text)

            # Apply transaction type filter
            date_item = table.item(row, 1)
            if date_item:
                row_date_str = date_item.text().strip()
                row_date = QtCore.QDate.fromString(row_date_str, "yyyy-MM-dd")
                if not row_date.isValid():
                    match_type = False
                elif trans_type_index == 1:  # Daily Transaction
                    match_type = (row_date == today)
                elif trans_type_index == 2:  # Monthly Transaction
                    match_type = (row_date.month() == today.month() and row_date.year() == today.year())

            table.setRowHidden(row, not (match_search and match_type))

    def toggle_status(self, row, label):
        table = self.transaction_table
        container = table.cellWidget(row, 8)
        if container:
            toggle_button = container.findChild(QtWidgets.QPushButton)
            if toggle_button:
                if toggle_button.isChecked():
                    label.setText("PAID")
                    label.setStyleSheet("color: #4CAF50; font-weight: bold;")
                else:
                    label.setText("PENDING")
                    label.setStyleSheet("color: #E57373; font-weight: bold;")


class ScrollableTextWidget(QtWidgets.QWidget):
    
    def __init__(self, text, parent=None):
        super(ScrollableTextWidget, self).__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create scrollable text area
        self.text_area = QtWidgets.QScrollArea()
        self.text_area.setWidgetResizable(True)
        self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)  
        self.text_area.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.text_area.setFrameShape(QtWidgets.QFrame.NoFrame)
        
        # Create a label with the text
        self.label = QtWidgets.QLabel(text)
        self.label.setTextFormat(QtCore.Qt.PlainText)
        self.label.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        
        # Add label to scroll area
        self.text_area.setWidget(self.label)
        
        # Add scroll area to layout
        layout.addWidget(self.text_area)
        
        # Set the widget's style
        self.setStyleSheet("""
            QScrollArea {
                background-color: transparent;
            }
            QLabel {
                background-color: transparent;
                padding-left: 4px;
                padding-right: 4px;
            }
            QScrollBar:horizontal {
                height: 10px;
                background: transparent;
                margin: 0px;
            }
            QScrollBar::handle:horizontal {
                background: #c0c0c0;
                min-width: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {
                width: 0px;
            }
        """)
        
        # Add tooltip for the full text
        self.setToolTip(text)

        # Install event filter to track mouse events
        self.installEventFilter(self)
        
    def text(self):
        return self.label.text()
    
    def eventFilter(self, obj, event):
        if obj is self:
            if event.type() == QtCore.QEvent.Enter:
                # Show scrollbar when mouse enters
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
                return True
            elif event.type() == QtCore.QEvent.Leave:
                # Hide scrollbar when mouse leaves
                self.text_area.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
                return True
        return super(ScrollableTextWidget, self).eventFilter(obj, event)


class TextEllipsisDelegate(QtWidgets.QStyledItemDelegate):
    
    def __init__(self, parent=None):
        super(TextEllipsisDelegate, self).__init__(parent)
        
    def paint(self, painter, option, index):
        # Use default painting
        super(TextEllipsisDelegate, self).paint(painter, option, index)
        
    def helpEvent(self, event, view, option, index):
        # Show tooltip when hovering if text is truncated
        if not event or not view:
            return False
            
        if event.type() == QtCore.QEvent.ToolTip:
            # Get the cell widget
            cell_widget = view.cellWidget(index.row(), index.column())
            
            if cell_widget and isinstance(cell_widget, ScrollableTextWidget):
                # Show tooltip for ScrollableTextWidget
                QtWidgets.QToolTip.showText(event.globalPos(), cell_widget.text(), view)
                return True
            else:
                # For standard items
                item = view.itemFromIndex(index)
                if item:
                    text = item.text()
                    width = option.rect.width()
                    metrics = QtGui.QFontMetrics(option.font)
                    elidedText = metrics.elidedText(text, QtCore.Qt.ElideRight, width)
                    
                    # If text is truncated, show tooltip
                    if elidedText != text:
                        QtWidgets.QToolTip.showText(event.globalPos(), text, view)
                    else:
                        QtWidgets.QToolTip.hideText()
                    
                    return True
                
        return super(TextEllipsisDelegate, self).helpEvent(event, view, option, index)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = TransactionsPage()
    window.show()
    sys.exit(app.exec_())