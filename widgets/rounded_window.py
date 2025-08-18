from PySide2.QtWidgets import QApplication, QWidget
from PySide2.QtCore import Qt, QPoint
from PySide2.QtGui import QPainter, QBrush, QColor, QRegion


class RoundedWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(400, 400)

        # Définir une forme ronde
        radius = 200
        region = QRegion(self.rect(), QRegion.Ellipse)
        self.setMask(region)

    def paintEvent(self, event):
        # Peindre le fond rond
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QBrush(QColor(100, 150, 255)))
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(self.rect())

    # Permet de déplacer la fenêtre manuellement
    def mousePressEvent(self, event):
        self.old_pos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = event.globalPos() - self.old_pos
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.old_pos = event.globalPos()


if __name__ == "__main__":
    app = QApplication([])
    window = RoundedWindow()
    window.show()
    app.exec_()
