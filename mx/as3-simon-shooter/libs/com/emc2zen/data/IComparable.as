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
	* Define la API para la implementacion de un comparador.
	* @author	PollyJex
	*/
	public interface IComparable {
		
		/**
		* Compara dos objetos. 
		* <p>- Si source es menor a value retorna -1.<br/> 
		* - Si source es igual a value retorna 0.<br/> 
		* - Si source es mayor a value retorna 1.</p>
		* @param	value		Valor a comparar.
		* @return	int
		*/
		function compareTo( value:* ):int
		
	}
	
}
