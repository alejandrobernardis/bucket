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

package com.emc2zen.util {

	/**
	* @import
	*/
	
	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.util.ArgumentsUtil;
	import com.emc2zen.util.NumberUtil;
	
	/**
	* Utilidades para las intancias del objeto Array.
	* @author	PollyJex
	*/
	public class ArrayUtil extends CoreStatic {
		
		/**
		* Retorna un nuevo Array discriminando del Array original los valor que no concuerden con el tipo.
		* @param	value		Array original.
		* @param	type		Valor a discriminar.
		* @return	Array
		*/
		public static function DiscriminateForType( value:Array, type:* = undefined ):Array {
			
			return ArgumentsUtil.DiscriminateForType( value, type );
			
		}
		
		/**
		* Retorna un unico valor o una lista con los valores del array pero desordenados.
		* @param	value 		Array original.
		* @param	noList	 	Define el modo de retorno. LIST:TRUE | UNIQUE:FALSE.
		* @return	Array
		*/
		public static function random( value:Array, noList:Boolean = false ):Array {
			
			var arrTmp:Array = new Array();
			var ranTmp:Array = NumberUtil.uniqueRandom( 0, value.length - 1 );
			
			while( ranTmp.length > 0 ){			
				
				arrTmp.push( value[ ranTmp.pop() ] );		
				
				if( noList ){
					break;
				}
				
			}		
			
			return arrTmp;
			
		}
		
	}
	
}
