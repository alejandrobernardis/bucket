#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 15/Nov/2013 00:23

import sys
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from common import FONT_VERDANA_10

try:
    import assets_rc
except:
    raise ImportError('Assets Not found.')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self._a_new_machine = None
        self._a_open_machine = None
        self._a_save_machine = None
        self._a_add_rails = None
        self._a_remove_rails = None
        self.file_dialog = QFileDialog(self)
        self.start_ui()
        self.setWindowTitle('Casino8 - F07010')
        self.setMinimumSize(QSize(1024, 768))
        self.show()

    # Message

    def open_message(self, e):
        QMessageBox.question(self, 'ERROR', "Error: %s" % e, QMessageBox.Ok)

    # Operations

    def _do_new_machine(self):
        pass

    def _do_open_machine(self):
        pass

    def _do_save_machine(self):
        pass

    def _do_add_rails(self):
        pass

    def _do_remove_rails(self):
        pass

    # Actions & Menu

    def create_actions(self):
        self._a_new_machine = \
            QAction(QIcon(':/assets/table_new.png'), '&New machine', self)
        self._a_new_machine.setShortcut(QKeySequence.New)
        self._a_new_machine.triggered.connect(self._do_new_machine)
        self._a_open_machine = \
            QAction(QIcon(':/assets/table_open.png'), '&Open machine', self)
        self._a_open_machine.setShortcut(QKeySequence.Open)
        self._a_open_machine.triggered.connect(self._do_open_machine)
        self._a_save_machine = \
            QAction(QIcon(':/assets/table_save.png'), '&Save machine', self)
        self._a_save_machine.setShortcut(QKeySequence.Save)
        self._a_save_machine.triggered.connect(self._do_save_machine)

        # Rails
        self._a_add_rails = \
            QAction(QIcon(':/assets/rails_add.png'), '&Add rails', self)
        self._a_add_rails.setShortcut('Ctrl+Shift+N')
        self._a_add_rails.triggered.connect(self._do_add_rails)
        self._a_remove_rails = \
            QAction(QIcon(':/assets/rails_remove.png'), '&Remove rails', self)
        self._a_remove_rails.setShortcut('Ctrl+Shift+R')
        self._a_remove_rails.triggered.connect(self._do_remove_rails)

    def create_menu(self):
        actions = \
            (self._a_new_machine, self._a_open_machine, self._a_save_machine,)
        menu_file = self.menuBar().addMenu("&File")
        menu_file.addActions(actions)

        # Rails
        actions = (self._a_add_rails, self._a_remove_rails,)
        menu_file = self.menuBar().addMenu("&Rails")
        menu_file.addActions(actions)

    def create_toolbar(self):
        actions = \
            (self._a_new_machine, self._a_open_machine, self._a_save_machine,)
        toolbar = self.addToolBar('Main')
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.addActions(actions)
        toolbar.addSeparator()
        actions = (self._a_add_rails, self._a_remove_rails,)
        toolbar.addActions(actions)

    def create_statusbar(self):
        statusbar = self.statusBar()
        statusbar.setFont(FONT_VERDANA_10)
        statusbar.showMessage('Initializing...')

    def create_docks(self):
        pass

    # GUI

    def start_ui(self):
        self.create_statusbar()
        self.create_actions()
        self.create_menu()
        self.create_toolbar()
        self.create_docks()
        self.statusBar().showMessage('Ready')


class MainApplication(QApplication):
    def __init__(self, sys_args):
        super(MainApplication, self).__init__(sys_args)
        self.main_window = MainWindow()
        self.exec_()


if __name__ == '__main__':
    try:
        app = MainApplication(sys.argv)
    except Exception as error:
        print 'EXIT *** (e): %s' % error
