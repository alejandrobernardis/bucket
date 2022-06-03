#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Copyright (c) 2012 Young and Rubicam Digital Mexico.
# Licensed under the Apache License, Version 2.0 (the "License")
#
# Author: Alejandro M. Bernardis
# Email: alejandro.bernardis at gmail.com
# Created: Feb 17, 2012 11:16:18 AM
#
#: -----------------------------------------------------------------------------
import csv, re, json
#: -----------------------------------------------------------------------------
def unicode_csv_reader(utf8_data, dialect=csv.excel, **kwargs):
	csv_reader = csv.reader(utf8_data, dialect=dialect, **kwargs)
	for row in csv_reader:
		yield [unicode(cell, 'utf-8') for cell in row]
#: -----------------------------------------------------------------------------
def  create_json(file_name=None, file_open=None):
	
	vmap = dict()
	
	def recursive_map(_map, _name, _value, _id):
		_vl = len(_value)
		if _vl > 0:
			_vx = str("i"+_value.pop(0))
			if not _vx in _map:
				_map[_vx] = dict(vid=_id if _vl == 1 else "", 
								 nombre=_name if _vl == 1 else "", 
								 segundoIni="", segundoEnd="", 
								 x="", y="30", w="140", h="100")
			elif _vx in _map and _vl == 1:
				_map[_vx]["vid"] = _id
				_map[_vx]["nombre"] = _name
			_map[_vx] = recursive_map(_map[_vx], _name, _value, _id)
		return _map
	
	with open(file_open, "rb") as f:
		csv_line = unicode_csv_reader(f)
		vmap["E"] = dict(vid=0, nombre="Entrada", segundoIni="", segundoEnd="")
		vmap["A"] = dict(vid=0, nombre="Con Salsita", segundoIni="", 
						 segundoEnd="", x="", y="100", w="250", h="100")
		vmap["B"] = dict(vid=0, nombre="Sin Salsita", segundoIni="", 
						 segundoEnd="", x="", y="100", w="250", h="100")
		
		for row in csv_line:
			if len(row) >= 7:
				_m = vmap[row[3]]
				_n = re.sub(r"\.mp4", "", row[2])
				_n = re.sub(r"^(A|B)_([0-9]_){3}", "", _n)
				_l = []
				for a in row[4:]:
					if a == "0": break
					_l.append(a)
				_i = row[1]
				vmap[row[3]] = recursive_map(_m, _n, _l, _i)
			else:
				vmap[row[3]]["vid"] = row[1]
				
		vmap["E"]["A"] = vmap["A"]
		del vmap["A"]
		vmap["E"]["B"] = vmap["B"]
		del vmap["B"]
		f.close()
		
	with open(file_name, "wb") as f:
		file_content = json.dumps(vmap)
		f.write(file_content)
		f.close()	
#: -----------------------------------------------------------------------------
if __name__ == '__main__':
	create_json(file_name="db/database.json", file_open="db/database.csv")
#: -----------------------------------------------------------------------------