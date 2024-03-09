import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        
        self.setGeometry(300, 300, 2000, 1000)
        self.setWindowTitle('Mana Pool')

        self.progressBar = QProgressBar(self)
        self.progressBar.setMaximum(500)
        self.progressBar.setValue(500)

        self.maxValueLabel = QLabel(f'Max Value: {self.progressBar.maximum()}', self)
        self.currentValueLabel = QLabel(f'Current Value: {self.progressBar.value()}', self)
        
        self.button1 = QPushButton('spell1', self)
        self.button1.clicked.connect(self.spell1)
        
        self.button2 = QPushButton('spell2', self)
        self.button2.clicked.connect(self.spell2)

        layout.addWidget(self.progressBar)
        layout.addWidget(self.maxValueLabel)
        layout.addWidget(self.currentValueLabel)
        layout.addWidget(self.button1)
        layout.addWidget(self.button2)

        self.setLayout(layout)

    def spell1(self):
        currentValue = self.progressBar.value()
        subtractAmount = 10
        newValue = max(0, currentValue - subtractAmount)
        self.progressBar.setValue(newValue)
        
        self.currentValueLabel.setText(f'Current Value: {newValue}')
        
    def spell2(self):
        currentValue = self.progressBar.value()
        subtractAmount = 50
        newValue = max(0, currentValue - subtractAmount)
        self.progressBar.setValue(newValue)
        
        self.currentValueLabel.setText(f'Current Value: {newValue}')

def main():
    app = QApplication(sys.argv)
    mainWin = MainWindow()
    mainWin.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
