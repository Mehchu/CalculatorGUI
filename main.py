from PyQt6.QtGui import QPalette, QFontMetrics
from PyQt6.QtWidgets import (QWidget, QPushButton, QApplication,
                             QGridLayout, QButtonGroup, QLabel, QSizePolicy)
from PyQt6.QtCore import Qt
import sys

displayString = ''
prevAns = ''
buttonGroup = QButtonGroup()
buttonList = ['7', '8', '9', ' * ', ' ** ',
              '4', '5', '6', ' / ', ' // ',
              '1', '2', '3', ' + ', 'del',
              ' = ', '0', '.', ' - ', 'ans']

op = {'+': lambda x, y: x + y,
      '-': lambda x, y: x - y,
      '*': lambda x, y: x * y,
      '/': lambda x, y: x / y,
      '**': lambda x, y: x ** y,
      '//': lambda x, y: x // y,
      }


def calculate(string):
    global prevAns
    string = string.split()
    if len(string) % 2 == 0:
        return "Syntax Error"
    while len(string) >= 3:
        try:
            answer = op[string[1]](float(string[0]), float(string[2]))
        except ZeroDivisionError:
            return "Undefined"
        string.pop(0)
        string.pop(0)
        string[0] = str(answer)
    prevAns = string[0]
    return string[0]


def textEntered(called):
    global displayString
    character = buttonList[buttonGroup.id(called)]
    if character == ' = ':
        window.display.setText(calculate(displayString))
        displayString = ''
        return
    elif character == 'ans':
        character = prevAns
    elif character == 'del':
        character = ''
        displayString = displayString[:-1]
    displayString += character
    window.display.setText(displayString)


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.display = QLabel(self)
        self.display.setStyleSheet("background-color: lightgray;border: 1px solid black")
        self.fontD = self.font()
        self.fontD.setPointSize(20)
        self.display.setFont(self.fontD)
        self.populate()

    def populate(self):

        grid = QGridLayout()

        grid.addWidget(self.display, 0, 0, 1, 5)

        x = 0
        y = 1
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        for index, character in enumerate(buttonList):
            button = QPushButton(character, self)
            button.setSizePolicy(sizePolicy)
            buttonGroup.addButton(button, index)
            grid.addWidget(button, y, x)

            x += 1
            if x >= 5:
                x = 0
                y += 1

        buttonGroup.buttonClicked.connect(textEntered)
        grid.setRowStretch(0, 3)
        for row in range(grid.rowCount() - 1):
            row += 1
            grid.setRowStretch(row, 2)
        grid.setSpacing(5)
        self.setLayout(grid)

        self.setGeometry(300, 300, 200, 200)
        self.setWindowTitle('Calculator')

        self.show()


def main():
    global window
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec())


if __name__ == '__main__':
    main()