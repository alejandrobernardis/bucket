/**
* @private
* @license	GNU GPLv2
*
* Copyright (C) 2007  Polly Jex.
* 
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
* MA  02110-1301, USA.
*
* @see	http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

package com.emc2zen.data {
	
	/**
	* @import
	*/

	import com.emc2zen.data.IIteratorBasic;

	/**
	* Define la API para la implementacion de un modelo basico de Iterator.
	* @author	PollyJex
	*/
	public interface IIterator extends IIteratorBasic {
		
		/**
		* Retorna la posicion actual del puntero.
		* @param	void
		* @return	int
		*/
		function index():int;
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		function peek():*;
		
		/**
		* Remueve del registro el ultimo elemento y retorna su valor.
		* @param	void
		* @return	*
		*/
		function remove():*;
		
		/**
		* Reseta el puntero de lectura.
		* @param	void
		* @return	void
		*/
		function reset():void;
		
		/**
		* Mueve el puntero de lectura al valor definido por value y retorna su valor.
		* @param	value	Posicion del puntero.
		* @return	*
		*/
		function seek( value:int ):*;
		
		/**
		* Retorna el tama&ntilde;o del registro.
		* @param	void
		* @return	int
		*/
		function size():int;
		
		/**
		* Retorna el valor asociado a la posicion actual del puntero.
		* @param	void
		* @return	*
		*/
		function value():*;
		
	}
	
}
