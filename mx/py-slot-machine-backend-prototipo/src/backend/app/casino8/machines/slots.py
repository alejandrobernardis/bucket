#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 23/06/2013 02:51

from array import array
from casino8.machines.base import AbstractMachine


class Slot100(AbstractMachine):
    mid = 100
    name = "BA"
    full_name = "Banda Ancha"
    max_lines = 10

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 20, 80),
        'B': (0, 0, 5, 25, 90),
        'C': (0, 0, 8, 35, 95),
        'D': (0, 0, 13, 45, 100),
        'E': (0, 0, 18, 70, 150),
        'F': (0, 0, 24, 95, 180),
        'G': (0, 2, 30, 130, 250),
        'H': (0, 3, 35, 200, 450),
        'I': (0, 4, 45, 240, 900),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 50, 500, 2000),
    }


class Slot101(AbstractMachine):
    mid = 101
    name = "FA"
    full_name = "Fiesta Animal"
    max_lines = 15

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 6, 7, 0),
        (-1, 1, 2, 3, 4, 5, 6, 7, 0),
        (-1, 1, 2, 3, 4, 5, 6, 7, 0),
        (-1, 1, 2, 3, 4, 5, 6, 7, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 3, 20, 50),
        'B': (0, 0, 5, 20, 60),
        'C': (0, 0, 9, 30, 100),
        'D': (0, 0, 11, 45, 120),
        'E': (0, 0, 13, 80, 160),
        'F': (0, 0, 18, 95, 210),
        'G': (0, 3, 25, 135, 280),
        'H': (0, 3, 30, 200, 350),
        'I': (0, 4, 50, 200, 700),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 50, 500, 2000),
    }


class Slot102(AbstractMachine):
    mid = 102
    name = "LTDM"
    full_name = "La Taberna del Monstruo"
    max_lines = 20

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 20, 60),
        'B': (0, 0, 5, 25, 90),
        'C': (0, 0, 8, 20, 100),
        'D': (0, 0, 12, 50, 140),
        'E': (0, 0, 13, 70, 180),
        'F': (0, 2, 18, 100, 250),
        'G': (0, 2, 20, 160, 280),
        'H': (0, 3, 35, 200, 320),
        'I': (0, 4, 50, 250, 850),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 6, 60, 600, 3000),
    }


class Slot103(AbstractMachine):
    mid = 103
    name = "RO"
    full_name = "Rockeros"
    max_lines = 20

    mini_game = (
        (-1, 1, 2, 3, 0),
        (-1, 1, 2, 3, 0),
        (-1, 1, 2, 3, 0),
        (-1, 1, 2, 3, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 15, 70),
        'B': (0, 0, 5, 20, 90),
        'C': (0, 0, 8, 30, 110),
        'D': (0, 0, 10, 55, 180),
        'E': (0, 0, 12, 65, 250),
        'F': (0, 2, 15, 85, 340),
        'G': (0, 2, 18, 100, 500),
        'H': (0, 5, 25, 115, 700),
        'I': (0, 6, 50, 145, 1300),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 60, 600, 3000),
    }


class Slot104(AbstractMachine):
    mid = 104
    name = "AA"
    full_name = u"Ataque Alienígena"
    max_lines = 25

    mini_game = (
        (-1, 1, 2, 3, 0),
        (-1, 1, 2, 3, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 30, 90),
        'B': (0, 0, 5, 30, 100),
        'C': (0, 0, 8, 40, 150),
        'D': (0, 0, 10, 50, 220),
        'E': (0, 0, 13, 60, 280),
        'F': (0, 2, 18, 85, 350),
        'G': (0, 2, 25, 95, 500),
        'H': (0, 3, 30, 140, 700),
        'I': (0, 5, 40, 200, 1000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 60, 600, 3000),
    }


class Slot105(AbstractMachine):
    mid = 105
    name = "LM"
    full_name = "Lucha Machine"
    max_lines = 25

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 15, 75),
        'B': (0, 0, 4, 25, 120),
        'C': (0, 0, 9, 30, 170),
        'D': (0, 0, 11, 40, 200),
        'E': (0, 0, 15, 45, 280),
        'F': (0, 2, 18, 70, 320),
        'G': (0, 2, 25, 90, 380),
        'H': (0, 3, 30, 130, 550),
        'I': (0, 4, 50, 300, 1500),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 50, 300, 3000),
    }


class Slot106(AbstractMachine):
    mid = 106
    name = "VI"
    full_name = "Vikingos"
    max_lines = 30

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 15, 70),
        'B': (0, 0, 5, 40, 80),
        'C': (0, 0, 8, 25, 110),
        'D': (0, 0, 10, 40, 165),
        'E': (0, 0, 13, 70, 190),
        'F': (0, 0, 17, 100, 230),
        'G': (0, 2, 25, 140, 310),
        'H': (0, 3, 32, 200, 500),
        'I': (0, 4, 45, 350, 1000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 50, 1000, 3500),
    }


class Slot107(AbstractMachine):
    mid = 107
    name = "SA"
    full_name = "Sr. Ardilla"
    max_lines = 30

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 3, 20, 80),
        'B': (0, 0, 4, 25, 90),
        'C': (0, 0, 7, 30, 150),
        'D': (0, 0, 11, 50, 190),
        'E': (0, 0, 12, 60, 240),
        'F': (0, 2, 15, 70, 350),
        'G': (0, 2, 20, 90, 500),
        'H': (0, 4, 30, 130, 600),
        'I': (0, 6, 40, 300, 3000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 80, 800, 4000),
    }


class Slot108(AbstractMachine):
    mid = 108
    name = "NP"
    full_name = "Navi Punk"
    max_lines = 30

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 3, 20, 80),
        'B': (0, 0, 4, 25, 90),
        'C': (0, 0, 7, 30, 150),
        'D': (0, 0, 11, 50, 190),
        'E': (0, 0, 12, 60, 240),
        'F': (0, 2, 15, 70, 350),
        'G': (0, 2, 20, 90, 500),
        'H': (0, 4, 30, 130, 600),
        'I': (0, 6, 40, 300, 3000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 80, 800, 4000),
    }


class Slot109(AbstractMachine):
    mid = 109
    name = "ZO"
    full_name = "Zombies"
    max_lines = 25

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 3, 20, 80),
        'B': (0, 0, 4, 25, 90),
        'C': (0, 0, 7, 30, 150),
        'D': (0, 0, 11, 50, 190),
        'E': (0, 0, 12, 60, 240),
        'F': (0, 2, 15, 70, 350),
        'G': (0, 2, 20, 90, 500),
        'H': (0, 4, 30, 130, 600),
        'I': (0, 6, 40, 300, 3000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 5, 80, 800, 4000),
    }


class Slot110(AbstractMachine):
    mid = 110
    name = "MS"
    full_name = "Mariachis"
    max_lines = 30

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 15, 75),
        'B': (0, 0, 6, 30, 130),
        'C': (0, 0, 9, 40, 170),
        'D': (0, 0, 11, 45, 220),
        'E': (0, 0, 15, 50, 290),
        'F': (0, 2, 18, 70, 320),
        'G': (0, 3, 25, 90, 380),
        'H': (0, 3, 30, 130, 500),
        'I': (0, 4, 50, 300, 2000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 7, 70, 600, 3500),
    }


class Slot111(AbstractMachine):
    mid = 111
    name = "MM"
    full_name = u"Mundo Mágico"
    max_lines = 25

    mini_game = (
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0),
        (-1, 1, 2, 3, 4, 5, 0)
    )

    rails = (
        array('c', 'AAAABBCCDDDEEEFFFGGGHHIIJJJJJKLL'),
        array('c', 'AAAABBBCCCCDDDEEEEFFFGHHIIJJJJKL'),
        array('c', 'AAABBBBCCCCDDDDEEFFFGGHHIJJJJJKL'),
        array('c', 'AAABBBCCCDDDEEEFFFFGGGGHHIIIJKLL'),
        array('c', 'AABBCCCDDDEEEEFFFFGGGHHHHHIIJKKL'),
    )

    paytable_chars = {
        'A': (0, 0, 4, 15, 75),
        'B': (0, 0, 6, 30, 130),
        'C': (0, 0, 9, 40, 170),
        'D': (0, 0, 11, 45, 220),
        'E': (0, 0, 15, 50, 290),
        'F': (0, 2, 18, 70, 320),
        'G': (0, 3, 25, 90, 380),
        'H': (0, 3, 30, 130, 500),
        'I': (0, 4, 50, 300, 2000),
        'J': (0, 0, 1, 2, 3),
        'K': (0, 0, 5, 10, 15),
        'L': (0, 7, 70, 600, 3500),
    }

