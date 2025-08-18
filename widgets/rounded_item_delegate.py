from PySide2 import QtWidgets, QtGui


class RoundedItemDelegate(QtWidgets.QStyledItemDelegate):
    def paint(self, painter, option, index):
        if index.column() == 0:
            rect = option.rect
            view = option.widget

            total_width = sum([view.columnWidth(i) for i in range(view.columnCount())])
            rect.setWidth(total_width)

            # Déterminer l'état visuel
            if option.state & QtWidgets.QStyle.State_Selected:
                bg_color = QtGui.QColor("#444444")  # Selected
            elif option.state & QtWidgets.QStyle.State_MouseOver:
                bg_color = QtGui.QColor("#444444")  # Hover
            else:
                bg_color = QtGui.QColor("#2e2e2e")  # Default

            painter.save()
            painter.setRenderHint(QtGui.QPainter.Antialiasing)
            path = QtGui.QPainterPath()
            radius = 5
            path.addRoundedRect(rect.adjusted(1, 1, -1, -1), radius, radius)
            painter.fillPath(path, bg_color)
            painter.restore()

        # Dessiner le texte normalement
        super().paint(painter, option, index)
