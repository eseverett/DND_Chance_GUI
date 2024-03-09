import sys
import random
import scipy.stats as stats
import matplotlib.pyplot as plt
from PyQt6.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget
from PyQt6.QtCore import QTimer
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

class GaussianRandomNumberGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.timer = QTimer()
        self.timer.timeout.connect(self.generateNumber)
        self.generated_numbers = []
        self.color_latched = False
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 2000, 1000)
        self.setWindowTitle('Gaussian Random Luck')

        layout = QVBoxLayout()
        self.startButton = QPushButton('Start', self)
        self.stopButton = QPushButton('Stop', self)
        self.resetButton = QPushButton('Reset', self)
        self.clearButton = QPushButton('Clear', self)
        self.plotCanvas = FigureCanvas(plt.Figure())

        layout.addWidget(self.startButton)
        layout.addWidget(self.stopButton)
        layout.addWidget(self.resetButton)
        layout.addWidget(self.clearButton)
        layout.addWidget(self.plotCanvas)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.startButton.clicked.connect(self.startRandomGeneration)
        self.stopButton.clicked.connect(self.stopRandomGeneration)
        self.resetButton.clicked.connect(self.resetColor)
        self.clearButton.clicked.connect(self.clearData)

        self.show()

    def startRandomGeneration(self):
        print("Starting random number generation")  # Debug print
        if not self.timer.isActive():
            self.timer.start(60000)  # 60 seconds

    def stopRandomGeneration(self):
        self.timer.stop()

    def resetColor(self):
        self.setStyleSheet("background-color: white;")
        self.color_latched = False
        self.startRandomGeneration()

    def clearData(self):
        self.generated_numbers = []
        self.updatePlot()

    def generateNumber(self):
        try:
            if self.color_latched:
                return

            number = random.gauss(0, 1)
            self.generated_numbers.append(number)

            if number < -2:
                self.setStyleSheet("background-color: red;")
                self.color_latched = True
            elif number > 2:
                self.setStyleSheet("background-color: green;")
                self.color_latched = True

            self.updatePlot()
        except Exception as e:
            print(f"Error in generateNumber: {e}")  # Error handling

    def updatePlot(self):
        self.plotCanvas.figure.clear()
        ax = self.plotCanvas.figure.add_subplot(111)
        stats.probplot(self.generated_numbers, dist="norm", plot=ax)
        ax.set_title("Q-Q Plot")
        self.plotCanvas.draw()

def main():
    app = QApplication(sys.argv)
    ex = GaussianRandomNumberGUI()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()

