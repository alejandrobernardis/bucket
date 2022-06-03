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
	
	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.data.type.Char;
	import com.emc2zen.util.StringUtil;
	import com.emc2zen.util.TypeUtil;

	/**
	* Resuelve el uso de caracteres en unicode.
	* @author	PollyJex
	*/
	public class Unicode extends CoreStatic {
		
		/**
		* Retona el caracter de reemplazo del valor unicode: "0xD1", 0xD1 -> (&Ntilde;)
		* @param	value	Valor unicode.
		* @return	Char
		*/
		public static function char( value:* ):Char {
			
			return new Char( charString( value ) );
			
		}
		
		/**
		* Retona el caracter de reemplazo del valor unicode:  "0xD1", 0xD1 -> (&Ntilde;)
		* @param	value	Valor unicode.
		* @return	String
		*/
		public static function charString( value:* ):String {
			
			if( TypeUtil.isNumber( value ) ){
				value = ucode( value );
			}
			
			value = StringUtil.replace( value, "^u", "0x" );
			
			return String.fromCharCode( parseInt( value, 16 ) );
			
		}
		
		/**
		* Retona el codigo del carcater en valor hexadecimal, en caso de no ser Char o String retorna -1.
		* @param	value 	Char | String
		* @return	Number
		*/
		public static function code( value:* ):Number {
			
			var numTmp:Number = -1;
			
			if( TypeUtil.isString( value ) ){
				
				numTmp = value.charCodeAt( 0 );
				
			}else if( TypeUtil.thisIs( value, Char ) ){
				
				numTmp = value.code();
				
			}
			
			return numTmp;
			
		}
		
		/**
		* Resuelve una cadena o una lista de caracteres a su valores de unicode.
		* @param	value	Lista de valores.
		* @return	Array
		*/
		public static function resolveUnicodeString( value:* ):Array {
			
			if( value.length < 2 ){
				return null;
			}
			
			var arrTmp:Array = new Array();
			
			if( ! TypeUtil.isArray( value ) ){
				
				arrTmp = value.split( " " );
				
			}else{
				
				arrTmp = value;
			}
			
			for( var a:int = 0; a < arrTmp.length; a++ ){
				
				arrTmp[ a ] = charString( arrTmp[ a ] );
				
			}
			
			return arrTmp;
			
		}
		
		/**
		* Retorna el valor unicode en hexadecimal como una cadena: (HEX) 0xD1 -> "0x00D1", (DEC) 209 -> "0x00D1"
		* @param	value	Valor decimal del caracter.
		* @return	String
		*/
		public static function ucode( value:Number ):String {
			
			return "0x" + StringUtil.toPad( value.toString( 16 ), 4, "0", StringUtil.PAD_LEFT ).toUpperCase();
			
		}
		
	}
	
}
