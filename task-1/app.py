import hashlib
import inspect
import os
import sys

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QDesktopWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QLabel,
    QHBoxLayout,
    QFileDialog,
)


class App(QWidget):
    def __init__(self, hasher=None, instance_dir=None, hash_limit=80):
        super().__init__()

        self.hasher = hasher or hashlib.sha512()
        self.instance_dir = instance_dir or os.path.join(os.path.dirname(__file__), 'instance')
        if not os.path.exists(self.instance_dir):
            os.makedirs(self.instance_dir)
        self.hash_limit = hash_limit

        self.title = 'Hash'
        self.width = 640
        self.height = 480

        self.file_name = None
        self.hash = None

        self.file_name_label = QLabel('')
        self.hash_label = QLabel('')

        self.text_edit = QTextEdit()

        self.open_button = QPushButton('Open')
        self.hash_button = QPushButton(self.hasher.name)
        self.export_button = QPushButton('Export')

        self.init_ui()

    def init_layout(self):
        self.text_edit.setEnabled(False)
        self.hash_button.setEnabled(False)

        self.hash_label.setVisible(False)
        self.file_name_label.setVisible(False)
        self.export_button.setVisible(False)

        self.open_button.clicked.connect(self.open_file)
        self.hash_button.clicked.connect(self.obtain_hash)
        self.export_button.clicked.connect(self.export_hash)

        v_box_layout = QVBoxLayout()
        h_box_layout = QHBoxLayout()
        hash_v_box_layout = QVBoxLayout()

        h_box_layout.addWidget(self.open_button)
        h_box_layout.addWidget(self.hash_button)

        v_box_layout.addWidget(self.file_name_label)
        v_box_layout.addWidget(self.text_edit)
        v_box_layout.addLayout(h_box_layout)
        hash_v_box_layout.addWidget(self.hash_label)
        hash_v_box_layout.addWidget(self.export_button)
        v_box_layout.addLayout(hash_v_box_layout)

        self.setLayout(v_box_layout)

    def init_ui(self):
        self.init_layout()

        self.setWindowTitle(self.title)
        self.setGeometry(0, 0, self.width, self.height)
        self.move_to_center()

        self.show()

    def move_to_center(self):
        rect = self.frameGeometry()
        center = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(center)
        self.move(rect.topLeft())

    def open_file(self):
        files = QFileDialog.getOpenFileName(self, 'Open File', self.instance_dir)

        try:
            if not files:
                return
            path = files[0]
            with open(path, 'r') as f:
                file_text = f.read()
                self.file_name = path
                self.file_name_label.setText(os.path.basename(path))
                self.file_name_label.setVisible(True)
                self.text_edit.setText(file_text)
                self.text_edit.setEnabled(True)
                self.hash_button.setEnabled(True)
        except FileNotFoundError:
            pass

    def obtain_hash(self):
        hasher = self.hasher.copy()
        text = self.text_edit.toPlainText().encode('utf-8')
        hasher.update(text)
        self.hash = hasher.hexdigest()
        self.hash_label.setText(self.truncate_label_text(self.hash))
        if not self.hash_label.isVisible():
            self.hash_label.setVisible(True)
            self.export_button.setVisible(True)

    def export_hash(self):
        file_name = QFileDialog.getSaveFileName(self, 'Export Hash', self.instance_dir)
        print(file_name)
        if not file_name:
            return
        try:
            path = file_name[0]
            with open(path, 'w') as f:
                f.write(self.hash)
        except FileNotFoundError:
            pass

    def truncate_label_text(self, text):
        if len(text) > self.hash_limit:
            return text[:self.hash_limit - 3] + '...'
        return text


def main():
    app = QApplication(sys.argv)
    ex = App(hashlib.md5())
    sys.exit(app.exec())


if __name__ == '__main__':
    main()
