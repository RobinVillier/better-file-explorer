from PySide2.QtWidgets import QProxyStyle, QApplication, QStyle
from PySide2.QtGui import QPainter, QColor, QBrush


class RoundedMenuStyle(QProxyStyle):  # TODO Rounded menu doesnt work, but doesn't return any error
    def __init__(self, base_style=None):
        super(RoundedMenuStyle, self).__init__(base_style or QApplication.style())

    def drawPrimitive(self, element, option, painter, widget=None):
        if element == QStyle.PE_PanelMenu:
            painter.save()
            painter.setRenderHint(QPainter.Antialiasing)
            rect = option.rect.adjusted(0, 0, -1, -1)
            color = QColor("#2d2d2d")
            painter.setBrush(QBrush(color))
            painter.setPen(QColor("#555"))
            painter.drawRoundedRect(rect, 8, 8)
            painter.restore()
        else:
            super(RoundedMenuStyle, self).drawPrimitive(element, option, painter, widget)
