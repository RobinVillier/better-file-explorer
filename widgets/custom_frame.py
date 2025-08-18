from PySide2 import QtWidgets, QtCore


class Frame(QtWidgets.QFrame):

    def __init__(self,
                 name: str = "",
                 parent=None,
                 fixed_height=None):
        super(Frame, self).__init__(parent)
        self.setObjectName(name)
        if fixed_height is not None:
            self.setFixedHeight(fixed_height)

        self._layout = QtWidgets.QVBoxLayout()
        self._layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(self._layout)

    def content_layout(self):
        return self._layout
