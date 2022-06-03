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
	import com.emc2zen.util.StringUtil;
	import com.emc2zen.util.TypeUtil;

	/**
	* Utilidades para las intancias del objeto Number.
	* @author	PollyJex
	*/
	public final class NumberUtil extends CoreStatic {
		
		/**
		* Valor minimo implementado en el metodo unique random.
		*/
		private static const UNIQUE_RANDOM_MIN:int = 1;
		
		/**
		* Valor maximo implementado en el metodo unique random.
		*/
		private static const UNIQUE_RANDOM_MAX:int = 32;
		
		
		
		/**
		* Agrega un cero a la izquierda del entero, solo para numeros del 1 al 9.
		* @param	source		Numero a modifica.
		* @return	String
		*/
		public static function addLeadingZero( value:int ):String {
			
			var numTmp:String = new String( value );
			
			if( value > -1 && value < 10 ){
				return StringUtil.toPad( numTmp, 2, "0", StringUtil.PAD_LEFT );
			}
			
			return numTmp;
			
		}
		
		/**
		* Verifica la igualdad entre dos numeros.
		* @param	value		Valor original.
		* @param	compare		Valor a comparar.
		* @return	Boolean
		*/
		public static function equals( value:Number = NaN, compare:Number = NaN ):Boolean {
			
			return new Boolean( value.valueOf() == compare.valueOf() );
			
		}
		
		/**
		* Verifica si value es modulo de module, retorna un Boolean.
		* @param	value		Valor a verificar.
		* @param	module		Valor del modulo.
		* @return	Boolean
		*/
		public static function isModule( value:Number, module:Number ):Boolean {
			
			return new Boolean( ( value % module ) == 0 );
			
		}
		
		/**
		* Retorna un Array el cual conforma una lista con la correlacion entre los numeros min y max.
		* @param	min		Valor minimo.
		* @param	maz		Valor maximo.
		* @return	Array
		*/
		public static function listed( min:Number = NaN, max:Number = NaN ):Array {
			
			var list:Array = new Array();
			
			if( isNaN( min ) ){
				min = UNIQUE_RANDOM_MIN;
				max = UNIQUE_RANDOM_MAX;
			}else if( isNaN( max ) ){
				max = ( min > UNIQUE_RANDOM_MIN ) ? min : UNIQUE_RANDOM_MAX;
				min = UNIQUE_RANDOM_MIN;
			}
			
			while( min <= max ){
				list.push( min ++ );
			}
			
			return list;
			
		}
		
		/**
		* Resuelve el valor de value dependiendo del modulo, retorna Number con el nuevo valor.
		* @param	value		Valor a resolver.
		* @param	module		Valor del modulo.
		* @return	Number
		*/
		public static function resolveModule ( value:Number, module:Number ):Number {
			
			if ( isModule( value, module ) ) { 
				return value; 
			}else if ( value < module ) { 
				return module; 
			}else { 
				return Math.round( ( value / module ) * module  ); 
			}
			
		}
		
		/**
		* Redondea los decimales de un numero dependiendo del valor de quantity, y retorna el resultado.
		* @param	value		Valor original.
		* @param	quantity	Cantidad de decimales.
		* @return	Number
		*/
		public static function toFixed( value:Number, quantity:Number ):Number {
			
			var numFlo:Number = Math.floor( value );
			var numPow:Number = Math.pow( 10, quantity );
			var numDec:String = new String( numPow + Math.round( ( value - numFlo ) * numPow ) );
			
			return new Number( numFlo + "." + numDec.substr( 1, quantity ) );
			
		}
		
		/**
		* Convierte el valor de value a HEXADECIMAL, con la opcion de modificar el prefijo a 0x o #, siendo "" el valor por default.
		* @param	value	Valor original
		* @param	prefix	Prefijo
		* @return	String
		*/
		public static function toHex( value:Number, prefix:String = "" ):String {
			
			var numTmp:String = value.toString( 16 );
			
			if( value < 16 ){
				numTmp = "0" + numTmp;
			}
			
			return ( prefix || "" ) + numTmp;
			
		}
		
		/**
		* Calcula el lime de un numero, y retona el resultado.
		* @param	value		Valor a evaluar.
		* @param	min			Valor minimo.
		* @param	max			Valor maximo.
		* @return	Number
		*/
		public static function toLimit ( value:Number, min:Number, max:Number ):Number {
			
			return new Number( Math.min( max, Math.max( min, value ) ) );
			
		}
		
		/**
		* Calcula el porcentage x de un numero, y retorna el resultado.
		* @param	source		Numero con el que se debe calcular.
		* @param	percentage	Porcentaje a calcular.
		* @return	Number
		*/
		public static function toPercentage( source:Number, percentage:Number ):Number {
			
			return new Number( ( percentage * source ) / 100 );
			
		}
		
		/**
		* Resuelve una lista de valores aleatorios de min a max.
		* @param	min		Valor minimo.
		* @param	max		Valor maximo.
		* @return	Array
		*/
		public static function uniqueRandom( min:Number = NaN, max:Number = NaN ):Array {
			
			var list:Array = listed( min, max );
			var result:Array = new Array();
			var listLeng:int = list.length;
			
			for ( var a:int = 0; a < listLeng; a++ ) {
				var rand:int = Math.floor( Math.random () * ( listLeng - a ) );
				result.push( list[ rand ] );
				list.splice( rand, 1 );
			}
			
			return result;
			
		}
		
	}
	
}
