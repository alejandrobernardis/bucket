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

	import com.emc2zen.core.Constant;
	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.data.iterator.StringIterator;

	/**
	* Utilidades para la verificacion de tipos de objetos.
	* @author	PollyJex
	*/
	public final class TypeUtil extends CoreStatic {
		
		/**
		* Constante EMPTY.
		*/
		public static const EMPTY:Constant = new Constant( "EMPTY", 0 );
		
		/**
		* Verifica si value corresponde a la clase type, si value es null, si value es undefined o si un objete esta vacio.
		* @param	value		Valor a evaluar.
		* @param	type		Tipo de valor a evaluar.
		* @return	Boolean
		*/
		public static function thisIs( value:*, type:* ):Boolean {
			
			if( isNull( type ) ) {
				return isNull( value );
			}else if( isUndefined( type ) ){ 
				return isUndefined( value );
			}else if( type === EMPTY || ( type is String && type.toUpperCase() == EMPTY.name ) ){ 
				return isEmpty( value );
			}else{
				return new Boolean( value is type );
			}			
			
		}
		
		/**
		* Is Array
		* @param	value	*
		* @return	Boolean
		*/
		public static function isArray( value:* ):Boolean {
			return thisIs( value, Array );
		}
		
		/**
		* Is Object
		* @param	value	*
		* @return	Boolean
		*/
		public static function isBoolean( value:* ):Boolean {
			
			if( isString( value ) ){
				value = value.toLowerCase();
			}
			
			switch( value ){
				
				case 1:
				case "1":
				case true:
				case "true":
				case "ok":
				case "yes":
				case "si":
				case "on":
					return true;
				
				case 0:
				case "0":
				case false:
				case "false":
				case undefined:
				case "undefined":
				case null:
				case "null":
				case "error":
				case "no":
				case "off":
				default:
					return false;				
				
			}
			
		}
		
		/**
		* Is Email
		* @param	value
		* @return	Boolean
		*/
		public static function isEmail( value:String ):Boolean {
			
			var charDisallowed:String = new String( "()<>,;:\\\"[] `~!#$%^&*+={}|/?'" );
			var charIterator:StringIterator = new StringIterator( value );
			
			while( charIterator.hasNext() ){
				if( charDisallowed.indexOf( charIterator.next() ) != -1 ){
					return false;
				}				
			}
			
			var expTmp:RegExp = new RegExp( "^([a-zA-Z0-9]+)([a-zA-Z0-9-_\.]*)@([a-zA-Z0-9-]+)[\.]([a-zA-Z]{2,4}[\.a-zA-Z]{0,4})$" );
			return new Boolean( ! isNull( expTmp.exec( value ) ) );
			
		}
		
		/**
		* Is Empty, verifica si un Array, String u Object esta vacio.
		* @param	value	*
		* @return	Boolean
		*/
		public static function isEmpty( value:* ):Boolean {
			
			if( ! isSet( value ) ){
				
				return true;
				
			}else if( isArray( value ) || isString( value ) ){
				
				if( isString( value ) ){
					value = StringUtil.remove( value, " " );
				}
				
				if( value.length > 0 ){
					return false;
				}
				
			}else if( isObject( value ) ){
				
				for( var obj:String in value ){
					return false;
				}
				
			}
			
			return true;			
			
		}
		
		/**
		* Is Function
		* @param	value	*
		* @return	Boolean
		*/
		public static function isFunction( value:* ):Boolean {
			return thisIs( value, Function );
		}
		
		/**
		* Is Int
		* @param	value	*
		* @return	Boolean
		*/
		public static function isInt( value:* ):Boolean {
			var tmpType:Boolean = thisIs( value, int );
			if( ( !tmpType ) 
					|| ( tmpType && ( value < -2147483648 || value > 2147483647 || isNaN ( value ) ) ) ){
				return false;
			}
			return true;
		}
		
		/**
		* Is Null
		* @param	value	*
		* @return	Boolean
		*/
		public static function isNull( value:* ):Boolean {
			return new Boolean( value === null );
		}
		
		/**
		* Is Number
		* @param	value	*
		* @return	Boolean
		*/
		public static function isNumber( value:* ):Boolean {
			var tmpType:Boolean = thisIs( value, Number );
			if( ( !tmpType ) 
					|| ( tmpType && ( value < 4.9406564584124654e-324 || value > 1.79769313486231e+308 || isNaN ( value ) ) ) ){
				return false;
			}
			return true;
		}
		
		/**
		* Is Object
		* @param	value	*
		* @return	Boolean
		*/
		public static function isObject( value:* ):Boolean {
			return thisIs( value, Object );
		}
		
		/**
		* Is Primitive ( Boolean | Number | String ).
		* @param	value	*
		* @return	Boolean
		*/
		public static function isPrimitive( value:* ):Boolean {
			return new Boolean( isBoolean( value ) || isNumber( value ) || isString( value ) )
		}
		
		/**
		 * Is Set
		 * @param	value
		 * @return	Boolean
		 */
		public static function isSet( value:* ):Boolean {
			
			if( ! isUndefined( value ) && ! isNull( value ) ){
				return true;
			}
			
			return false;
			
		}
		
		/**
		* Is String
		* @param	value	*
		* @return	Boolean
		*/
		public static function isString( value:* ):Boolean {
			return thisIs( value, String );
		}
		
		/**
		* Is Uint
		* @param	value	*
		* @return	Boolean
		*/
		public static function isUint( value:* ):Boolean {
			var tmpType:Boolean = thisIs( value, uint );
			if( ( !tmpType ) 
					|| ( tmpType && ( value < 0 || value > 4294967295 || isNaN ( value ) ) ) ){
				return false;
			}
			return true;
		}
		
		/**
		* Is Undefined
		* @param	value	*
		* @return	Boolean
		*/
		public static function isUndefined( value:* ):Boolean {
			return new Boolean( value === undefined );
		}	
		
		/**
		* Is XML
		* @param	value	*
		* @return	Boolean
		*/
		public static function isXML( value:* ):Boolean {
			return thisIs( value, XML );
		}
		
	}
	
}
