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

	/**
	* Utilidades para las intancias del objeto String.
	* @author	PollyJex
	*/
	public final class StringUtil extends CoreStatic {
		
		/**
		* Agrega una cantidad x de caracteres del lado izquierdo de la cadena.
		*/
		public static const PAD_LEFT:Constant = new Constant( "LEFT", 1 );
		
		/**
		* Agrega una cantidad x de caracteres del lado derecho y del izquierdo de la cadena.
		*/
		public static const PAD_BOTH:Constant = new Constant( "BOTH", 2 );
		
		/**
		* Agrega una cantidad x de caracteres en el medio de la cadena.
		*/
		public static const PAD_RILE:Constant = new Constant( "RILE", 3 );
		
		/**
		* Agrega una cantidad x de caracteres del lado derecha de la cadena.
		*/
		public static const PAD_RIGTH:Constant = new Constant( "RIGTH", 4 );
		
		
		
		/**
		* Retorna una cadena con el primer caracter de cada palabra en mayuscula.
		* @param	source	Valor a modifica.
		* @return	String
		*/
		public static function capitalize( source:String ):String {
			
			return ResolveCapitalize( source );
			
		}
		
		/**
		* Evalua el cuerpo de cadena, retorna => 1:MAYUSCULA | 0:MINUSCULA.
		* @param	value 	Valor a comparar.
		* @return	Number
		*/
		public static function casevalue( value:String ):Number {
			
			if( value.toUpperCase() == value ){
				return 1;
			}else{
				return 0;
			}
			
		}
		
		/**
		* Verifica si la cadena source es igual a compare, retorna un boolean.
		* @param	source			Valor a comparar.
		* @param	compare			Valor de comparacion.
		* @param	caseSensitive	Determina si la comparacion es sensible a mayusculas.
		* @return	Boolean
		*/
		public static function equal( source:String, compare:String, caseSensitive:Boolean = false ):Boolean {
			
			if( TypeUtil.isNull( source ) || TypeUtil.isNull( compare ) ){
				return false;
			}
			
			if( ! caseSensitive ){
				return new Boolean( source.toUpperCase() == compare.toUpperCase() );
			}else{
				return new Boolean( source == compare );
			}
			
		}
		
		/**
		* Verifica si value equivale a un espacio en blanco.
		* @param	value	Valor original.
		* @return	Boolean
		*/
		public static function isWhiteSpace( value:String ):Boolean {
			
			if( value.charCodeAt( 0 ) == 32 ){
				return true;
			}
			
			switch( value ){
				
				case "\n":
				case "\r":
				case "\t":
				case "\f":
					return true;
					
				default:
					return false;
				
			}
			
		}
		
		/**
		* Retorna una cadena con el primer caracter en minuscula.
		* @param	source	Valor a modificar.	
		* @return	String
		*/
		public static function lcFirstChar( source:String ):String {
			
			return new String( source.substr( 0, 1 ).toLowerCase() + source.substr( 1 ) );
			
		}
		
		/**
		* Remueve los espacios en blanco a la inzquierda de la cadena.
		* @param	source	Valor a limpiar.
		* @return	String
		*/
		public static function ltrim( source:String ):String {
			
			var intTmp:int = 0;
			
			while( isWhiteSpace( source.charAt( intTmp++ ) ) ){
				source = source.substr( intTmp, source.length );
			}
			
			return source;
			
		}
		
		/**
		* Remueve de la cadena source el valor definido en value, retorna una nueva cadena.
		* @param	source	Valor original.
		* @param	value	Valor a eliminar.
		* @return	String
		*/
		public static function remove( source:String, value:String ):String {
			
			return replace( source, value, "" );
			
		}
		
		/**
		* Repite la cadena source la cantidad de veces de quantity, retorna una nueva cadena.
		* @param	source		Valor a repetir.
		* @param	quantity	Cantidad de repeticiones.
		* @return	String
		*/
		public static function repeat( source:String, quantity:int ):String {
			
			var strTmp:String = new String();
			
			while( quantity > 0 ){
				strTmp += source;
				quantity --;
			}
			
			return strTmp;
			
		}		
		
		/**
		* Reemplaza en la cadena source el valor de value por el valor de changed, posee la capacidad de reemplazar una o 
		* todas las apariciones en la cadena source. Retona una nueva cadena.
		* @param	source		Valor original.
		* @param	value		Valor a reemplazar.
		* @param	changed		Valor de reemplazo.
		* @param	stopLoop	Indica si reempleza el valor de value en toda la cadena.
		* @return	
		*/
		public static function replace( source:String, value:String, changed:String, stopLoop:Boolean=false ):String {
			
			var regTmp:RegExp = new RegExp( value );
			
			while( regTmp.exec( source ) != null ){
				source = source.replace( regTmp, changed );
				if( stopLoop ){
					break;
				}
			}
			
			return source;
			
		}	
		
		/**
		* Invierte el sentido de la cadena.
		* @param	source	Cadena a invertir.
		* @return	String
		*/
		public static function reverse( source:String ):String {
			
			return new String( source.split( "" ).reverse().join( "" ) );
			
		}
		
		/**
		* Remueve los espacios en blanco a la derecha de la cadena.
		* @param	source	Valor a limpiar.
		* @return	String
		*/
		public static function rtrim( source:String ):String {
			
			while( isWhiteSpace( source.charAt( source.length - 1 ) ) ){
				source = source.substr( 0, source.length - 1 );
			}
			
			return source;
			
		}
		
		/**
		* Sustituye en value la secuencia de paramatros que conforman a rest, para el orden de 
		* reemplazo utilizar <code>{x}</code>, donde x es un numero de 1-X.
		* @param	value	Valor original.
		* @param	rest	Secuencia de reemplazos. 1, 2, n -> {1}, {2}, {n}.
		* @return	
		*/
		public static function substitute( value:String, ...rest ):String {
			
			var argDat:Array = ArgumentsUtil.Verify( rest );
			var argLen:int = argDat.length;
			var strRep:String = new String();
			
			for( var a:int = 0; a < argLen; a++ ){
				
				strRep = "\\{" + ( a + 1 ) + "\\}";
				value = replace( value, strRep, argDat[ a ], true );
				
			}
			
			return value;
			
		}
		
		/**
		* Rellena la cadena source con la cadena changed la diferencia entre ( length - source ), dependiendo del tipo y retorna una nueva cadena.
		* @param	source		Valor original.
		* @param	length		Largo de la cadena.
		* @param	changed		Valor de agregado.
		* @param	type		Tipo de orperacion ( PAD_BOTH | PAD_LEFT | PAD_RIGTH (d) | PAD_RILE ).
		* @return	String
		*/
		public static function toPad( source:String, length:int, changed:String = " ", type:Constant = null ):String {
			
			var strLen:int = new int( length - source.length );
			
			if( !TypeUtil.isEmpty( source ) || strLen > 0 ){
				
				if( TypeUtil.isNull( type ) ){
					type = PAD_RIGTH;
				}
				
				var strAdd:String = repeat( changed, strLen ).substr( 0, strLen );
				
				if( type == PAD_BOTH || type == PAD_RILE ){
					var middle:int;
				}
				
				switch( type ){
					
					case PAD_BOTH:
						middle = new int( Math.floor( strAdd.length / 2 ) );
						source = strAdd.substr( 0, middle ) + source + strAdd.substr( middle );
						break;
						
					case PAD_LEFT:
						source = strAdd + source;
						break;
						
					case PAD_RIGTH:
					default:
						source = source + strAdd;
						break;
						
					case PAD_RILE:
						middle = new int( Math.floor( source.length / 2 ) );
						source = source.substr( 0, middle ) + strAdd + source.substr( middle );
						break;
					
				}
				
			}
			
			return source;
			
		}
		
		/**
		* Remueve los espacios en blanco a la derecha y a la inzquierda de la cadena.
		* @param	source	Valor a limpiar.
		* @return	String
		*/
		public static function trim( source:String ):String {
			
			return rtrim( ltrim( source ) );
			
		}
		
		/**
		* Retorna una cadena con el primer caracter en mayuscula.
		* @param	source	Valor a modificar.	
		* @return	String
		*/
		public static function ucFirstChar( source:String ):String {
			
			return new String( source.substr( 0, 1 ).toUpperCase() + source.substr( 1 ) );
			
		}
		
		/**
		* Retorna una cadena con el primer caracter de cada palabra en minuscula.
		* @param	source	Valor a modifica.
		* @return	String
		*/
		public static function unCapitalize( source:String ):String {
			
			return ResolveCapitalize( source, true );
			
		}
		
		
		
		/**
		* Resuelve la capitalizacion o descapitalizacon de un cadena.
		* @param	soruce	Valor a modifcar.
		* @param	value	Modo. TRUE:UNCAPITALIZE | FALSE:CAPITALIZE.
		* @return	
		*/
		private static function ResolveCapitalize( source:String, value:Boolean = false ):String {
			
			var strTmp:String = new String();
			var arrTmp:Array = source.split( " " );
			
			while( arrTmp.length > 0 ){		
				
				if( ! value ){
					strTmp += ucFirstChar( arrTmp.shift() );	
				}else{
					strTmp += lcFirstChar( arrTmp.shift() );	
				}
				
			}
			
			return strTmp;
			
		}
		
	}
	
}
