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
	import com.emc2zen.data.type.AbstractType;
	import com.emc2zen.util.TypeUtil;
	
	/**
	* Utilidades para la manipulacion de los argumentos pasados en las funciones.
	* @author	PollyJex
	*/
	public class ArgumentsUtil extends CoreStatic {
		
		/**
		* Verifica la forma en la que se pasa los argumentos y retorna un nuevo array con la lista corregida.
		* @param	value	Lista de valores.
		* @return	Array
		*/
		public static function Verify( value:Array ):Array {
			
			if( TypeUtil.isArray( value[ 0 ] ) && value.length == 1 ){
				return value[ 0 ];
			}else{
				return value;
			}
			
		}	
		
		/**
		* Retorna un nuevo Array discriminando del Array original los valor que no concuerden con el tipo.
		* @param	value		Array original.
		* @param	type		Valor a discriminar.
		* @return	Array
		*/
		public static function DiscriminateForType( value:Array, type:* = undefined ):Array {
			
			if( ! TypeUtil.isUndefined( type ) ){
				
				var arrRet:Array = new Array();				
				var arrTmp:Array = Verify( value );
				
				for( var a:int = 0; a < arrTmp.length; a++ ){
					
					if( TypeUtil.thisIs( arrTmp[ a ], type ) ){
						arrRet.push( arrTmp[ a ] );
					}
					
				}
				
				if( ! TypeUtil.isEmpty( arrRet ) ){
					return arrRet;
				}
				
			}
			
			return null;
			
		}
		
	}
	
}
