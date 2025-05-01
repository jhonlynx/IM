from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtChart import QChart, QChartView, QPieSeries, QPieSlice

class AdminDashboardPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.parent = parent
        self.sample_data = [
            ("TR001", "Alice Brown", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
            ("TR002", "Charlie Davis", "₱50", "John Doe", "2023-10-15", "PENDING"),
            ("TR003", "Eve Franklin", "₱50", "John Doe", "2023-10-15", "FAILED"),
            ("TR004", "George Harris", "₱50", "John Doe", "2023-10-15", "COMPLETED"),
        ]
        self.setup_ui()

    def setup_ui(self):
        layout = QtWidgets.QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        
        content_widget = QtWidgets.QWidget()
        content_layout = QtWidgets.QVBoxLayout(content_widget)
        content_layout.setSpacing(40)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Stats Grid
        stats_grid = QtWidgets.QGridLayout()
        stats_grid.setSpacing(20)
        
        # Add stat cards
        workers_card = self.create_stat_card("Total Workers", "25", "images/list.png")
        stats_grid.addWidget(workers_card, 0, 0)
        
        customers_card = self.create_stat_card("Total Customers", "150", "images/clients.png")
        stats_grid.addWidget(customers_card, 0, 1)
        
        active_card = self.create_stat_card("Active", "120", "images/active.png")
        stats_grid.addWidget(active_card, 0, 2)
        
        inactive_card = self.create_stat_card("Inactive", "30", "images/not-active.png")
        stats_grid.addWidget(inactive_card, 0, 3)
        
        total_billed = sum(float(TRANS_AMOUNT.replace('₱', '')) 
                          for _, _, TRANS_AMOUNT, _, _, _ in self.sample_data)
        billed_card = self.create_stat_card("Total Billed Amount", f"₱{total_billed:,.2f}", "images/bill.png")
        stats_grid.addWidget(billed_card, 0, 4)
        
        content_layout.addLayout(stats_grid)
        
        # Charts Grid
        charts_container = QtWidgets.QWidget()
        charts_layout = QtWidgets.QHBoxLayout(charts_container)
        charts_layout.setSpacing(20)
        
        daily_chart = self.create_revenue_chart("Daily Revenue")
        monthly_chart = self.create_revenue_chart("Monthly Revenue")
        
        charts_layout.addWidget(daily_chart, 1)
        charts_layout.addWidget(monthly_chart, 1)
        
        content_layout.addWidget(charts_container)
        layout.addWidget(content_widget)

    def create_stat_card(self, title, value, icon):
        # [Keep existing create_stat_card method]
        pass

    def create_revenue_chart(self, title):
        # [Keep existing create_revenue_chart method]
        pass