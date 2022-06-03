#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 15/Nov/2013 11:09


import os
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from unicodecsv import UnicodeWriter, UnicodeReader
from common import FONT_VERDANA_TABLE, FONT_VERDANA_TABLE_ROW, COLOR_OK, \
    COLOR_ERROR, COLOR_WARNING, COLOR_INFO, set_bets_by_level, \
    FONT_VERDANA_REPORT, FONT_VERDANA_REPORT_ROW
from config import HEADER_TABLE, DEFAULT_TABLE, DEFAULT_PAYTABLE
from settings import DATA_PATH


class TableEditorWidget(QTableWidget):
    def __init__(self, *__args):
        super(TableEditorWidget, self).__init__(13, 6, *__args)
        self.start_ui()

    def start_ui(self):
        for col, (label, width) in enumerate(HEADER_TABLE):
            self.setHorizontalHeaderItem(col, QTableWidgetItem(label))
            self.setColumnWidth(col, width)
        self.setSelectionMode(QAbstractItemView.NoSelection)
        self.setStyleSheet("QTableWidget {border: none}")
        self.setFont(FONT_VERDANA_TABLE_ROW)
        self.setAlternatingRowColors(True)
        self.reset_grid()
        hheader = self.horizontalHeader()
        hheader.setSectionResizeMode(0, QHeaderView.Stretch)
        hheader.hide()
        vheader = self.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.hide()

    def keyReleaseEvent(self, event):
        if event.key() in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Tab,):
            self.recalculate_grid()

    def reset_grid(self, data=None):
        for row, (char, p1, p2, p3, p4, p5,) \
                in enumerate(data or DEFAULT_TABLE):
            flags = ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
            if row < 12:
                char_item = QTableWidgetItem(char)
                char_item.setFont(FONT_VERDANA_TABLE)
                char_item.setBackground(COLOR_INFO)
                char_item.setFlags(char_item.flags() & flags)
                self.setItem(row, 0, char_item)
                for pos, (element) in enumerate((p1, p2, p3, p4, p5,)):
                    item = QTableWidgetItem(str(element))
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row, pos+1, item)
            else:
                for pos in xrange(0, 6):
                    item = QTableWidgetItem()
                    item.setFont(FONT_VERDANA_TABLE)
                    item.setBackground(COLOR_WARNING)
                    item.setFlags(item.flags() & flags)
                    item.setTextAlignment(Qt.AlignCenter)
                    self.setItem(row, pos, item)
        self.recalculate_grid()
        data and self.verify_grid()

    def recalculate_grid(self):
        for col in xrange(1, 6):
            result = 0
            for row in xrange(0, 12):
                try:
                    value = int(self.item(row, col).text())
                    if value < 0:
                        raise ValueError()
                except Exception:
                    self.item(row, col).setText('0')
                    value = 0
                result += value
            item = self.item(12, col)
            item.setText(str(result))
            if result == 32:
                color = COLOR_OK
            elif result > 32:
                color = COLOR_ERROR
            else:
                color = COLOR_WARNING
            item.setBackground(color)

    def verify_grid(self):
        result = 0
        for col in xrange(1, 6):
            try:
                result += int(self.item(12, col).text())
            except Exception:
                return False
        if not (result == 32*5):
            raise ValueError('Complete the table on your left or open a file')

    def resolve_file_name(self, file_name=None):
        return file_name or os.path.join(DATA_PATH, 'table.tmp.csv')

    def save(self, file_name=None):
        self.verify_grid()
        try:
            if isinstance(file_name, (list, tuple,)):
                file_name = file_name[0]
            with open(self.resolve_file_name(file_name), 'wb') as file_output:
                writer = UnicodeWriter(file_output)
                writer.writerow(('X', '1', '2', '3', '4', '5'))
                for row in xrange(0, 13):
                    row_value = []
                    for col in xrange(0, 6):
                        row_value.append(self.item(row, col).text())
                    if row < 12:
                        row_value[0] = str(row_value[0][0:1]).upper()
                    else:
                        row_value[0] = 'EOF'
                    writer.writerow(row_value)
        except Exception:
            raise IOError('Can\'t save the file: %s' % file_name)

    def open(self, file_name=None):
        try:
            if isinstance(file_name, (list, tuple,)):
                file_name = file_name[0]
            with open(self.resolve_file_name(file_name), 'rb') as file_input:
                result = []
                data = UnicodeReader(file_input)
                for row in data:
                    if str(row[0]).lower() not in ('x', 'eof',):
                        char = str(row[0]).upper()
                        if char == "J":
                            row[0] = "J (Game)"
                        elif char == "K":
                            row[0] = "K (Free Spins)"
                        elif char == "L":
                            row[0] = "L (Wildcard)"
                        result.append(row)
                self.reset_grid(result)
        except Exception:
            raise IOError('Can\'t open the file: %s' % file_name)


class FormEditorWidget(QWidget):
    def __init__(self, *__args):
        super(FormEditorWidget, self).__init__(*__args)
        self.input_iterations = None
        self.input_balance = None
        self.combobox_paytable = None
        self.combobox_level = None
        self.combobox_bet = None
        self.combobox_lines = None
        self.checkbox_verbose = None
        self.start_ui()

    def start_ui(self):
        grid = QGridLayout()
        grid.setSpacing(4)
        self.input_iterations = QLineEdit('400')
        grid.addWidget(QLabel('Iterations:'), 0, 0)
        grid.addWidget(self.input_iterations, 0, 1, 1, 2)
        self.input_balance = QLineEdit('200')
        grid.addWidget(QLabel('Balance:'), 1, 0)
        grid.addWidget(self.input_balance, 1, 1, 1, 2)
        self.combobox_paytable = QComboBox()
        self.combobox_paytable.currentIndexChanged.connect(self.reset_paytable)
        grid.addWidget(QLabel('Paytable:'), 2, 0)
        grid.addWidget(self.combobox_paytable, 2, 1, 1, 2)
        self.combobox_level = QComboBox()
        self.combobox_level.currentIndexChanged.connect(self.reset_level)
        grid.addWidget(QLabel('Level:'), 3, 0)
        grid.addWidget(self.combobox_level, 3, 1, 1, 2)
        self.combobox_bet = QComboBox()
        grid.addWidget(QLabel('Bet:'), 4, 0)
        grid.addWidget(self.combobox_bet, 4, 1, 1, 2)
        self.combobox_lines = QComboBox()
        grid.addWidget(QLabel('Lines:'), 5, 0)
        grid.addWidget(self.combobox_lines, 5, 1, 1, 2)
        self.checkbox_verbose = QCheckBox()
        grid.addWidget(QLabel('Verbose:'), 6, 0)
        grid.addWidget(self.checkbox_verbose, 6, 1, 1, 2)
        self.start_paytable()
        self.start_level()
        self.setLayout(grid)

    def reset_form(self):
        self.input_iterations.setText('400')
        self.input_balance.setText('200')
        self.combobox_paytable.setCurrentIndex(0)
        self.combobox_level.setCurrentIndex(0)

    def start_paytable(self):
        self.combobox_paytable.clear()
        for name, table, max_lines in DEFAULT_PAYTABLE:
            self.combobox_paytable.addItem(name)

    def start_level(self):
        self.combobox_level.clear()
        for number in xrange(1, 140):
            self.combobox_level.addItem(str(number))

    def reset_level(self, level=None):
        if not level:
            level = int(self.combobox_level.currentText())
        else:
            level += 1
        self.combobox_bet.clear()
        for number in set_bets_by_level(level):
            self.combobox_bet.addItem(str(number))

    def reset_paytable(self):
        value = int(self.combobox_paytable.currentIndex())
        self.combobox_lines.clear()
        for number in xrange(1, DEFAULT_PAYTABLE[value][2]+1):
            self.combobox_lines.addItem(str(number))


class EditorWidget(QDockWidget):
    def __init__(self, *__args):
        super(EditorWidget, self).__init__(*__args)
        self.table = None
        self.form = None
        self.button_run = None
        self.start_ui()

    def start_ui(self):
        vbox = QVBoxLayout()
        self.table = TableEditorWidget()
        vbox.addWidget(self.table)
        self.form = FormEditorWidget()
        vbox.addWidget(self.form)
        self.button_run = \
            QPushButton(QIcon(':/assets/run.png'), u'Run Simulation')
        vbox.addWidget(self.button_run)
        widget = QWidget()
        widget.setLayout(vbox)
        self.setWidget(widget)
        self.setFixedWidth(300)
        self.setFixedHeight(550)
        self.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.setTitleBarWidget(None)


class ReportWidget(QTableWidget):
    def __init__(self, *__args):
        super(ReportWidget, self).__init__(*__args)
        self.start_ui()

    def start_ui(self):
        self.setFont(FONT_VERDANA_TABLE_ROW)
        self.setAlternatingRowColors(True)
        hheader = self.horizontalHeader()
        hheader.setSectionResizeMode(0, QHeaderView.Stretch)
        hheader.hide()
        vheader = self.verticalHeader()
        vheader.setSectionResizeMode(QHeaderView.Stretch)
        vheader.hide()

    def update_grid(self, data):
        flags = ~Qt.ItemIsEditable & ~Qt.ItemIsSelectable
        for row, row_data in enumerate(data):
            for col, col_data in enumerate(row_data):
                item = QTableWidgetItem()
                if isinstance(col_data, unicode):
                    item.setText(col_data)
                else:
                    item.setText(str(col_data))
                if col < 1 or row_data[0] == 'Combos':
                    item.setFont(FONT_VERDANA_REPORT)
                else:
                    item.setFont(FONT_VERDANA_REPORT_ROW)
                    item.setTextAlignment(Qt.AlignCenter)
                item.setFlags(item.flags() & flags)
                self.setItem(row, col, item)