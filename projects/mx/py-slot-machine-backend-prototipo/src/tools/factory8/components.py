#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 15/Nov/2013 11:09


from PyQt5.QtWidgets import *


class BaseTableWidget(QTableWidget):
    pass


class RailsTableWidget(BaseTableWidget):
    pass


class PayTableWidget(BaseTableWidget):
    pass


class MachineFormWidget(QWidget):
    def __init__(self, parent=None, flags=None):
        super(MachineFormWidget, self).__init__(parent, flags)
        self._input_id = None
        self._input_name = None
        self._input_full_name = None
        self._input_max_lines = None
        self.start_ui()

    def start_ui(self):
        grid = QGridLayout()
        self._input_id = QLineEdit()
        grid.addWidget(QLabel('ID#:'), 0, 0)
        grid.addWidget(self._input_iterations, 0, 1, 1, 2)
        self._input_name = QLineEdit()
        grid.addWidget(QLabel('Name:'), 1, 0)
        grid.addWidget(self._input_name, 1, 1, 1, 2)
        self._input_full_name = QLineEdit()
        grid.addWidget(QLabel('Full Name:'), 2, 0)
        grid.addWidget(self._input_full_name, 2, 1, 1, 2)
        self._input_max_lines = QLineEdit()
        grid.addWidget(QLabel('Max Lines:'), 3, 0)
        grid.addWidget(self._input_max_lines, 3, 1, 1, 2)
        self.setLayout(grid)

    def reset_form(self):
        self._input_id.clear()
        self._input_name.clear()
        self._input_full_name.clear()
        self._input_max_lines.clear()