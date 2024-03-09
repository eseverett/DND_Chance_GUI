from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QProgressBar, QLabel, QHBoxLayout, QCheckBox
from PyQt6.QtCore import QTimer
import sys
import pandas as pd
from functools import partial
from PyQt6 import QtCore

class MainWindow(QWidget):
    def __init__(self, configFile):
        super().__init__()
        self.configFile = configFile
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout()
        
        self.setGeometry(300, 300, 2000, 1000)
        self.setWindowTitle('Mana Pool')

        self.progressBar = QProgressBar(self)
        self.progressBar.setMinimumSize(1850, 30)  
        self.progressBar.setMaximum(100)
        self.progressBar.setValue(100)

        self.maxValueLabel = QLabel(f'Max Mana: {self.progressBar.maximum()}', self)
        self.currentValueLabel = QLabel(f'Current Mana: {self.progressBar.value()}', self)

        labelLayout = QHBoxLayout()
        labelLayout.addWidget(self.maxValueLabel)
        labelLayout.addWidget(self.currentValueLabel)
        labelLayout.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)

        self.layout.addLayout(labelLayout)

        self.loadSpellsFromConfig()

        self.manaRegenCheckbox = QCheckBox("Mana Regeneration", self)
        self.manaRegenCheckbox.stateChanged.connect(self.toggleManaRegeneration)
        self.layout.addWidget(self.manaRegenCheckbox)

        self.regenTimer = QTimer(self)
        self.regenTimer.timeout.connect(self.regenMana)
        self.regenTimer.setInterval(1000)  # Regenerate mana every 1000 milliseconds (1 second)

        self.setLayout(self.layout)

    def toggleManaRegeneration(self, _):
        if self.manaRegenCheckbox.isChecked():
            print("Mana regeneration started")
            self.regenTimer.start()
        else:
            print("Mana regeneration stopped")
            self.regenTimer.stop()


    def regenMana(self):
        currentValue = self.progressBar.value()
        maxValue = self.progressBar.maximum()
        newValue = min(maxValue, currentValue + 1)
        print(f"Regenerating mana: {newValue}")  # Debugging print
        self.progressBar.setValue(newValue)
        self.currentValueLabel.setText(f'Current Mana: {newValue}')

    def loadSpellsFromConfig(self):
        try:
            spells_df = pd.read_csv(self.configFile, delimiter=',')
            
            for index, row in spells_df.iterrows():
                buttonLabel = f"{row['Category']} {row['Level']}: {row['Name']}"
                descriptionLabel = QLabel(f"{row['Description']} Cost: {row['Cost']}", self)
                spellButton = QPushButton(buttonLabel, self)
                spellCost = int(row['Cost'])
                spellButton.clicked.connect(partial(self.castSpell, spellCost))
                
                self.layout.addWidget(spellButton)
                self.layout.addWidget(descriptionLabel)
        except Exception as e:
            print(f"Failed to load config file: {e}")

    def castSpell(self, manaCost):
        currentValue = self.progressBar.value()
        newValue = max(0, currentValue - manaCost)
        self.progressBar.setValue(newValue)
        self.currentValueLabel.setText(f'Current Value: {newValue}')

def main():
    configFile = 'DND_Chance_GUI/conf.csv' 
    app = QApplication(sys.argv)
    mainWin = MainWindow(configFile)
    mainWin.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
