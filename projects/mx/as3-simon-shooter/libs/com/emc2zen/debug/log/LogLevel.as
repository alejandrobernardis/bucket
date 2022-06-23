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

package com.emc2zen.debug.log {
	
	/**
	* @import
	*/

	import com.emc2zen.core.Constant;

	/**
	* Capa de dato del modelo de implementacion de LEVELS para el proceso de DEBUGGIN.
	* @author	PollyJex
	*/
	public class LogLevel extends Constant {
		
		/**
		* Level NONE.
		*/
		public static const NONE:LogLevel = new LogLevel( "NONE", 0, 0xCCCCCC );
		
		/**
		* Level INFO.
		*/
		public static const INFO:LogLevel = new LogLevel( "INFO", 1, 0x00CC33 );
		
		/**
		* Level DEBUG.
		*/
		public static const DEBUG:LogLevel = new LogLevel( "DEBUG", 2, 0x00CCCC );
		
		/**
		* Level WARN.
		*/
		public static const WARNING:LogLevel = new LogLevel( "WARNING", 3, 0xFFFF00 );
		
		/**
		* Level ERROR.
		*/
		public static const ERROR:LogLevel = new LogLevel( "ERROR", 4, 0xFF9900 );
		
		/**
		* Level CRITICAL.
		*/
		public static const CRITICAL:LogLevel = new LogLevel( "CRITICAL", 5, 0xFF4400 );
		
		/**
		* Level FATAL.
		*/
		public static const FATAL:LogLevel = new LogLevel( "FATAL", 6, 0xFF0000 );
		
		
		
		/**
		* Verifica si es un LEVEL registrado, si no existe retorna LEVEL.NONE.
		* @param	value		Instacia de la clase.
		* @return	LogLevel
		*/
		public static function verifyLevel( value:LogLevel ):LogLevel {
			
			return LogLevel[ resolveLevelAsName( value.id ) ];
			
		}
		
		/**
		* Resuelve el NOMBRE del LEVEL por el numero de ID.
		* @param	value		Identificador numerico.
		* @return	String
		*/
		public static function resolveLevelAsName( value:int ):String {
			
			return resolveLevelAsAux( value, true );
			
		}
		
		/**
		* Resuelve el COLOR del LEVEL por el numero de ID.
		* @param	value	Identificador numerico.
		* @return	uint
		*/
		public static function resolveLevelAsColor( value:int ):uint {
			
			return resolveLevelAsAux( value );
			
		}
		
		
		
		/**
		* Resuelve el NOMBRE y COLOR del LEVEL por el numero de ID.
		* @param	value	Identificador numerico.
		* @param	name	Define el tipo de retorno TRUE:NAME | FALSE:COLOR.
		* @return	*
		*/
		private static function resolveLevelAsAux( value:int, name:Boolean=false ):* {
			
			var objTmp:LogLevel;
			
			switch( value ) {
				
				case 1:
					objTmp = INFO;
					break;
				case 2:
					objTmp = DEBUG;
					break;
				case 3:
					objTmp = WARNING;
					break;
				case 4:
					objTmp = ERROR;
					break;
				case 5:
					objTmp = CRITICAL;
					break;
				case 6:
					objTmp = FATAL;	
					break;
				case 0:
				default:
					objTmp = NONE;
					break;
				
			}
			
			return ( ! name ) ? objTmp.color : objTmp.name;
			
		}
		
		
		
		/**
		* Identificador del color del LEVEL (uint).
		*/
		private var _color:uint;
		
		/**
		* Constructor
		* @param	name		Identificador literal.
		* @param	id			Identificador numerico.
		* @param	color		Color.
		* @return	LogLevel
		*/
		public function LogLevel( name:String, id:int, color:uint ) {
			
			super( name, id, "LogLevel" );
			
			this._color = color;
			
		}
		
		/**
		* Retona el COLOR del LEVEL.
		* @param	Void
		* @return	uint
		*/
		public function get color():uint {
			
			return _color;
			
		}
		
	}
	
}
