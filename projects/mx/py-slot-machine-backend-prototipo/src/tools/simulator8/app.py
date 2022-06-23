#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 15/Nov/2013 00:23

import os
import sys
import json
import datetime
import settings
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from bot import OptionsHelper, run as simulator
from common import FONT_VERDANA_10, set_points_by_level
from config import DEFAULT_PAYTABLE
from components import EditorWidget, ReportWidget

try:
    import assets_rc
except:
    raise ImportError('Assets Not found.')


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(None)
        self._a_new_table = None
        self._a_open_table = None
        self._a_save_table = None
        self._a_run_simulation = None
        self._w_dock = None
        self._w_report = None
        self.file_dialog = QFileDialog(self)
        self.start_ui()
        self.setWindowTitle('Casino8 - B07010')
        self.setMinimumSize(QSize(1024, 768))
        self.show()

    # Properties

    @property
    def w_dock(self):
        return self._w_dock

    @property
    def w_report(self):
        return self._w_report

    # Message

    def open_message(self, e):
        QMessageBox.question(self, 'ERROR', "Error: %s" % e, QMessageBox.Ok)

    # Operations

    def _do_new_table(self):
        self._w_dock.table.reset_grid()

    def _do_open_table(self):
        try:
            self._w_dock.table.open(self.file_dialog.getOpenFileName())
        except Exception as e:
            self.open_message(e)

    def _do_save_table(self):
        try:
            self._w_dock.table.save(self.file_dialog.getSaveFileName())
        except Exception as e:
            self.open_message(e)

    def _do_run_simulation(self):
        self.statusBar().showMessage('Start simulation...')
        try:

            report_datetime = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')

            report_table = os.path.join(
                settings.DATA_PATH,
                'csv/report.table.%s.csv' % report_datetime
            )

            self._w_dock.table.verify_grid()
            self._w_dock.table.save(report_table)
            form = self._w_dock.form

            try:
                index = form.combobox_paytable.currentIndex()
                machine = DEFAULT_PAYTABLE[index][0]
                paytable = DEFAULT_PAYTABLE[index][1]
                max_lines = DEFAULT_PAYTABLE[index][2]

            except Exception:
                machine = DEFAULT_PAYTABLE[0][0]
                paytable = DEFAULT_PAYTABLE[0][1]
                max_lines = DEFAULT_PAYTABLE[0][2]

            options = OptionsHelper()
            options.filename = report_table
            options.verbose = form.checkbox_verbose.isChecked()
            options.balance = float(form.input_balance.text())
            options.bet = float(form.combobox_bet.currentText())
            options.lines = int(form.combobox_lines.currentText())
            options.max_lines = max_lines
            options.iterations = int(form.input_iterations.text())
            options.level = int(form.combobox_level.currentText())
            options.points = set_points_by_level(options.level)

            report_config = os.path.join(
                settings.DATA_PATH,
                'csv/report.config.%s.json' % report_datetime
            )

            with open(report_config, 'wb') as file_output:
                json.dump({
                    'iterations': options.iterations,
                    'balance': options.balance,
                    'bet': options.bet,
                    'lines': options.lines,
                    'level': options.level,
                    'paytable': machine,
                }, file_output, indent=4)

            data = simulator(options, paytable, report_datetime, False)
            self._w_report.update_grid(data)
            self.statusBar().showMessage('Complete simulation')

        except Exception as e:
            self.statusBar().showMessage('Simulation failed')
            self.open_message(e)

    # Actions & Menu

    def create_actions(self):
        self._a_new_table = \
            QAction(QIcon(':/assets/table_new.png'), '&New table', self)
        self._a_new_table.setShortcut(QKeySequence.New)
        self._a_new_table.triggered.connect(self._do_new_table)
        self._a_open_table = \
            QAction(QIcon(':/assets/table_open.png'), '&Open table', self)
        self._a_open_table.setShortcut(QKeySequence.Open)
        self._a_open_table.triggered.connect(self._do_open_table)
        self._a_save_table = \
            QAction(QIcon(':/assets/table_save.png'), '&Save table', self)
        self._a_save_table.setShortcut(QKeySequence.Save)
        self._a_save_table.triggered.connect(self._do_save_table)
        self._a_run_simulation = \
            QAction(QIcon(':/assets/run.png'), '&Run simulation', self)
        self._a_run_simulation.setShortcut('Ctrl+R')
        self._a_run_simulation.triggered.connect(self._do_run_simulation)

    def create_menu(self):
        actions = (self._a_new_table, self._a_open_table, self._a_save_table,)
        menu_file = self.menuBar().addMenu("&File")
        menu_file.addActions(actions)
        menu_run = self.menuBar().addMenu("&Run")
        menu_run.addActions((self._a_run_simulation,))

    def create_toolbar(self):
        actions = (self._a_new_table, self._a_open_table, self._a_save_table,)
        toolbar = self.addToolBar('Main')
        toolbar.setIconSize(QSize(16, 16))
        toolbar.setMovable(False)
        toolbar.addActions(actions)
        toolbar.addSeparator()
        toolbar.addAction(self._a_run_simulation)

    def create_statusbar(self):
        statusbar = self.statusBar()
        statusbar.setFont(FONT_VERDANA_10)
        statusbar.showMessage('Initializing...')

    def create_docks(self):
        self._w_dock = EditorWidget('Configuration', self)
        self._w_dock.button_run.clicked.connect(self._do_run_simulation)
        self.addDockWidget(Qt.LeftDockWidgetArea, self._w_dock)
        self._w_report = ReportWidget(50, 6)
        self.setCentralWidget(self._w_report)

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
