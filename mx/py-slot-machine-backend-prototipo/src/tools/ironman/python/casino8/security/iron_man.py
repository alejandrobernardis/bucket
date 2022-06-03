#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2013 Asumi Kamikaze Inc.
# Copyright (c) 2013 The Octopus Apps Inc.
# Licensed under the Apache License, Version 2.0 (the "License")
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: 31/07/2013 18:05

import re

SEPARATOR = '|'
VALIDATE_HASH = re.compile(r'^I(\d)+$')
VALIDATE_KEY = re.compile(r'^I(\d)+\|[a-zA-Z0-9-]+$')
VALIDATE_TOKEN = re.compile(r'^\^[\d]{4,}\/[\d]{2,}\/[\d]{2,}\|'
                            r'[\d]{2,}:[\d]{2,}:[\d]{2,}\.[\d]{1,4}\|'
                            r'latinocasino\.net\|'
                            r'[a-zA-Z0-9]{6,}\$$')

VALIDATE_INDEX = re.compile(r'\d')
VALIDATE_LETTERS = re.compile(r'[a-z]', re.I)
LETTERS_MIN = 'abcdefghijklmnopqrstuvwxyz'
LETTERS_MAY = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
LETTERS = LETTERS_MIN+LETTERS_MAY
LETTERS_LEN = len(LETTERS)-1

SECRET_HASH = 'Y2HePDUxJqtbjMt6CbRBtgHvBSKSpAVaZ/CLAlvGvwuUO7gQZo644mkDJUR2p' \
              '0Wd1RqSmgMtL12u1@J3nldwXLR8#GL05G7OQWpbXx5tSJZ2xU9xqZJ5fsX+JL' \
              'mbfiTKW2UM8FHj8ky7lnFy!hHALRiQ7++B3Rn4=='

# ------------------------------------------------------------------------------

KEYS = 'VCn6,NOD5,lDX4,sXS8,NHc8,NhD8,csl9,Ega2,hFm3,VIa6,rRG7,cQA1,XHC4,' \
       'fsx1,VSp4,LFk2,zbt9,LFR7,ciF5,FEp3,irw4,uHd2,GNd4,CMd6,fPS3,cxz6,' \
       'KRI9,zrm2,sfU5,qct7,SNW7,oix9,hCC6,Pms4,jNp4,GAC2,jmY9,ebi1,lWp3,' \
       'KwU8,NqY6,euB8,usS2,qqy9,OHj2,BmC8,FRf7,xKe3,wnH8,LVr1,hBv2,aJE8,' \
       'Mue6,CaY4,FdX1,SqK1,GOI7,XJN9,Teg9,FqS9,CAx9,NQb2,nVr7,Azj8,hrc5,' \
       'SYA4,JQA8,UiV3,cIK3,sPh2,hcx8,doJ8,bJU1,RlF1,Byw5,zVo3,yzo2,gla7,' \
       'fQj5,loB3,UAC7,UiY1,oQA8,SFS2,mJk4,ggG7,LEC5,pWl9,rBi3,ywJ6,ySF7,' \
       'Ocm2,GQk5,fLy7,DhL1,uwO8,RLu6,OQj5,azr8,NnJ2'

# ------------------------------------------------------------------------------


class IronMan(object):
    @staticmethod
    def doit(literal, key):
        result = u''
        key_index = 0
        for i in literal:
            number = ord(i) ^ ord(key[key_index])
            xored = str(number)
            if number < 10:
                xored = '00' + xored
            elif number < 100:
                xored = '0' + xored
            result += xored
            if key_index == len(key)-1:
                key_index = 0
            else:
                key_index += 1
        return result

    @staticmethod
    def rdoit(literal, key):
        result = u''
        key_index = 0
        key_coef = 3
        for i in xrange(0, len(literal)/key_coef):
            pos = i * key_coef
            xored = int(literal[pos:pos+key_coef])
            result += chr(xored ^ ord(key[key_index]))
            if key_index == len(key)-1:
                key_index = 0
            else:
                key_index += 1
        return result

    @staticmethod
    def defense(value):
        if not VALIDATE_HASH.match(value):
            raise ValueError(u'El formato del request no es correcto.')
        value = IronMan.rdoit(value, SECRET_HASH)
        if not VALIDATE_KEY.match(value):
            raise ValueError(u'El formato de la clave no es correcto.')
        value = value.split(SEPARATOR)
        result = IronMan.rdoit(value[0][1:], value[1])
        if not VALIDATE_TOKEN.match(result):
            raise ValueError(u'El formato del literal no es correcto.')
        result = result[1:-1].split(SEPARATOR)
        if len(result) is not 4:
            raise ValueError(u'La cantidad de bloques no es correcta.')
        super_key = result[3]
        index = int(VALIDATE_INDEX.findall(super_key)[0])
        letters = VALIDATE_LETTERS.findall(super_key)
        result = u''
        for i in letters:
            new_index = LETTERS.index(i)+index
            if new_index <= LETTERS_LEN:
                result += LETTERS[new_index]
            else:
                result += LETTERS[(new_index-LETTERS_LEN)-1]
        result += str(index)
        return result in KEYS
