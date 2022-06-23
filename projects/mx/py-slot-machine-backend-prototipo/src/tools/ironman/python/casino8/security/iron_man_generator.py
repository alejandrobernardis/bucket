#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 31/07/2013 23:34

from array import array
from random import randrange, shuffle
from casino8.security.iron_man import *


class IronManKeyGenerator(object):
    def get_chars(self):
        result = []
        for i in xrange(0, 3):
            result.append(randrange(0, LETTERS_LEN))
        return result

    def verify(self, value, compare):
        index = int(VALIDATE_INDEX.findall(value)[0])
        letters = VALIDATE_LETTERS.findall(value)
        result = ''
        for i in letters:
            new_index = LETTERS.index(i)+index
            if new_index <= LETTERS_LEN:
                result += LETTERS[new_index]
            else:
                result += LETTERS[(new_index-LETTERS_LEN)-1]
        result += str(index)
        return result in compare

    def simple_verify(self, index, letters, compare):
        result = ''
        for i in letters:
            new_index = LETTERS.index(i)+index
            if new_index <= LETTERS_LEN:
                result += LETTERS[new_index]
            else:
                result += LETTERS[(new_index-LETTERS_LEN)-1]
        return result in compare

    def create(self, quantity=100):
        server = []
        client = []

        for i in xrange(0, quantity):
            literal_value = ''
            literal_token = ''
            char_index = randrange(1, 10)
            char_indexes = self.get_chars()

            for j in char_indexes:
                letter = LETTERS[j]
                literal_value += letter
                new_index = j - char_index
                if new_index >= 0:
                    literal_token += LETTERS[new_index]
                else:
                    literal_token += LETTERS[(new_index+LETTERS_LEN)+1]

            if not self.simple_verify(char_index, literal_token, literal_value):
                continue

            extra_numbers = randrange(100, 1000)
            token = array('c', literal_token+str(extra_numbers))
            shuffle(token)

            index = VALIDATE_INDEX.findall(token)[0].tostring()
            hash_client = token.tostring().replace(index, str(char_index))

            hash_server = ''
            index = int(VALIDATE_INDEX.findall(hash_client)[0])
            letters = VALIDATE_LETTERS.findall(hash_client)

            for k in letters:
                new_index = LETTERS.index(k)+index
                if new_index <= LETTERS_LEN:
                    hash_server += LETTERS[new_index]
                else:
                    hash_server += LETTERS[(new_index-LETTERS_LEN)-1]
            hash_server += str(index)

            if not self.verify(hash_client, hash_server):
                continue

            server.append(hash_server)
            client.append(hash_client)

        print '*' * 80
        print 'Iron Man Key Gnerator'
        print '*' * 80

        print '\nPython (server):\n'
        print '\'%s\'' % ','.join(server)
        print '*' * 80

        print '\nActionScript 3 (client):\n'
        print client
        print '*' * 80

ikg = IronManKeyGenerator()
ikg.create(100)