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

package com.emc2zen.data.type {
	
	/**
	* @import
	*/

	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.IChar;

	/**
	* Representacion de un caracter.
	* @author	PollyJex
	*/
	public class Char extends CoreObject implements IChar {
		
		/**
		* Caracter.
		*/
		private var _char:String;
		
		/**
		* Constructor.
		* @param	value	Caracter.
		* @return	Char
		*/
		public function Char( value:String = "" ) {
			
			if( value.length > 1 ){
				value = value.substring( 0, 1 );
			}
			
			_char = value;
			
		}
		
		/**
		* Retorna el codigo del caracter.
		* @param	void
		* @return	Number
		*/
		public function code():Number {
			
			return _char.charCodeAt( 0 );
			
		}
		
		/**
		* Retorna una cadena con el valor de la clase.
		* @param	void
		* @return	String
		*/
		override public function toString():String {
			
			return _char;
			
		}
		
		/**
		* Retorna el valoe del caracter.
		* @param	void
		* @return	String
		*/
		public function value():String {
			
			return _char;
			
		}
		
	}
	
}
