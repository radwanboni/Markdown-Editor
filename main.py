from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

import os
import sys
import webbrowser

def show_help_menu():
    help_menu = QDialog()
    layout = QVBoxLayout()
    help_menu.setLayout(layout)
    help_menu.setMinimumSize(QSize(300, 150))
    help_menu.setWindowTitle('MdEditor Help')

    # Markdown Tutorial
    mk_layout = QVBoxLayout()
    mk_tut = QPushButton(QIcon('icon/Markdown_doc.png'), "MarkDown Tutorial \nOpen official Github Markdown", help_menu)
    mk_tut.clicked.connect(lambda: webbrowser.open('https://www.markdownguide.org'))
    mk_tut.setObjectName('mk')
    layout.addWidget(mk_tut)

    # Credit Section
    credit_label = QLabel("MdEditor\nMd Boni Amin (202080090129) using Python (PyQt5)")
    credit_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(credit_label)

    help_menu.exec_()

def create_main_window():
    main_window = QMainWindow()
    main_window.path = ''
    main_window.setMinimumSize(QSize(800, 600))
    container = QWidget()
    layout = QVBoxLayout()
    container.setLayout(layout)
    main_window.setCentralWidget(container)

    # Toolbar
    app_toolbar = QToolBar()
    main_window.addToolBar(app_toolbar)
    app_toolbar.setMovable(False)

    main_window.spacer = QWidget()
    main_window.spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    main_window.spacer.setObjectName('spacer')

    main_window.spacer2 = QWidget()
    main_window.spacer2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    main_window.spacer2.setObjectName('spacer')

    # Preview Button
    main_window.preview = QAction(QIcon("icon/Preview_Close.png"), "Show Preview", main_window)
    main_window.preview.triggered.connect(preview_panel)
    app_toolbar.addAction(main_window.preview)
    main_window.preview_hidden = False

    app_toolbar.addWidget(main_window.spacer)

    # Filename
    main_window.filename = QLabel('Untitled.md')
    main_window.filename.setObjectName('doc')
    app_toolbar.addWidget(main_window.filename)

    app_toolbar.addWidget(main_window.spacer2)

    # Save Button
    main_window.save = QAction(QIcon("icon/save.png"), "Save", main_window)
    main_window.save.triggered.connect(file_save)
    app_toolbar.addAction(main_window.save)
    main_window.save.setObjectName('right')

    # Open Button
    main_window.open = QAction(QIcon("icon/openfile.png"), "Open", main_window)
    main_window.open.triggered.connect(open_file)
    app_toolbar.addAction(main_window.open)

    # New Button
    main_window.new = QAction(QIcon("icon/add-file.png"), "New", main_window)
    main_window.new.triggered.connect(new_file)
    app_toolbar.addAction(main_window.new)

    # Help
    main_window.help = QAction(QIcon("icon/Help.png"), "Help", main_window)
    main_window.help.triggered.connect(show_help_menu)
    app_toolbar.addAction(main_window.help)

    # Editor
    mainlayout = QHBoxLayout()
    layout.addLayout(mainlayout)

    # Input Editor
    main_window.input_editor = QTextEdit(main_window,
                    placeholderText="Type something here...",
                    lineWrapColumnOrWidth=100,
                    readOnly=False,
                    acceptRichText=False)
    main_window.input_editor.setContextMenuPolicy(Qt.NoContextMenu)
    mainlayout.addWidget(main_window.input_editor)

    # Output Editor
    main_window.output_editor = QTextEdit(main_window,
                    lineWrapColumnOrWidth=100,
                    readOnly=True,
                    acceptRichText=False
    )
    main_window.output_editor.setContextMenuPolicy(Qt.NoContextMenu)
    mainlayout.addWidget(main_window.output_editor)
    main_window.output_editor.setObjectName('Output')

    # Live Preview
    main_window.input_editor.textChanged.connect(on_input_change)

    return main_window

def open_file():
    file_path, _ = QFileDialog.getOpenFileName(main_window, "Open Markdown File", "", "Markdown Documents (*.md);;Text Documents (*.txt)")
    if file_path:
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                main_window.input_editor.setPlainText(content)
                main_window.path = file_path
                update_doc_title()
        except Exception as error:
            error_dialog(str(error))

def new_file():
    main_window.path = ''
    main_window.input_editor.clear()
    update_doc_title()

def on_input_change():
    main_window.output_editor.setMarkdown(main_window.input_editor.toPlainText())

def file_save():
    if not main_window.path:
        file_path, _ = QFileDialog.getSaveFileName(main_window, "Save File", "", filter="Markdown Documents (*.md);;Text Documents (*.txt)")
        if not file_path:
            return
        main_window.path = file_path
        update_doc_title()

    text = main_window.input_editor.toPlainText()
    try:
        with open(main_window.path, 'w') as file:
            file.write(text)
    except Exception as error:
        error_dialog(str(error))

def preview_panel():
    if not main_window.preview_hidden:
        main_window.output_editor.hide()
        main_window.preview_hidden = True
        main_window.preview.setToolTip("Show Preview")
        main_window.preview.setIcon(QIcon('icon/Preview_Open.png'))
    else:
        main_window.output_editor.show()
        main_window.preview_hidden = False
        main_window.preview.setToolTip("Close Preview")
        main_window.preview.setIcon(QIcon('icon/Preview_Close.png'))

def update_doc_title():
    main_window.setWindowTitle("%s MdEditor" %(os.path.basename(main_window.path) if main_window.path != '' else "Untitled.md"))
    main_window.filename.setText("%s" %(os.path.basename(main_window.path) if main_window.path != '' else "Untitled.md"))

def error_dialog(error):
    dialog = QMessageBox(main_window)
    if error == 'string index out of range':
        dialog.setText("You didn't save (")
    else:
        dialog.setText(error)
    dialog.setIcon(QMessageBox.Critical)
    dialog.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("MdEditor")
    icon_path = os.path.abspath("icon/logo.ico")
    app_icon = QIcon(icon_path)
    app.setWindowIcon(app_icon)

    main_window = create_main_window()

    main_window.show()
    app.exec_()