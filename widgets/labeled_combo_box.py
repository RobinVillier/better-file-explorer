from PySide2 import QtWidgets, QtCore


class LabeledComboBox(QtWidgets.QWidget):
    def __init__(self, label_text: str, parent=None) -> QtWidgets.QComboBox:
        super().__init__(parent)
        layout = QtWidgets.QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.label = QtWidgets.QLabel(label_text)
        self.label.setAlignment(QtCore.Qt.AlignRight | QtCore.Qt.AlignVCenter)

        self.combobox = QtWidgets.QComboBox()
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        self.combobox.setSizePolicy(size_policy)

        layout.addWidget(self.label, 1)
        layout.addWidget(self.combobox, 4)
