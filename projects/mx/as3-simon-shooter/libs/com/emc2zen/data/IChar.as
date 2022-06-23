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



	/**
	* Define la API para la implementacion de una representacion de un caracter.
	* @author	PollyJex
	*/
	public interface IChar {
		
		/**
		* Retorna el codigo del caracter.
		* @param	void
		* @return	Number
		*/
		function code():Number;
		
		/**
		* Retorna una cadena con el valor de la clase.
		* @param	void
		* @return	String
		*/
		function toString():String;
		
		/**
		* Retorna el valoe del caracter.
		* @param	void
		* @return	String
		*/
		function value():String;
		
	}
	
}
