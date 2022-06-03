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
	* Capa de dato del modelo de implementacion de ENVIRONMENT para el proceso de DEBUGGIN.
	* @author	PollyJex
	*/
	public class LogEnvironment extends Constant {
		
		/**
		* Entorno LOCAL, ejecuta el proceso de debugin dentro del SWF en la consola.
		*/
		public static const LOCAL:LogEnvironment = new LogEnvironment( "LOCAL", 1 );
		
		/**
		* Entorno REMOTE, ejecuta el proceso de debugin fuera del SWF en la consola.
		*/
		public static const REMOTE:LogEnvironment = new LogEnvironment( "REMOTE", 2 );
		
		/**
		* Entorno OUTPUT, ejecuta el proceso de debugin dentro del SWF en la consola de salida de flash.
		*/
		public static const OUTPUT:LogEnvironment = new LogEnvironment( "OUTPUT", 0 );
		
		
		
		/**
		* Verifica si es un ENVIRONMENT registrado, si no existe retorna LogEnvironment.OUTPUT.
		* @param	value		Instancia de la clase.
		* @return	LogEnvironment
		*/
		public static function verifyEnvironment( value:LogEnvironment ):LogEnvironment {
			
			return LogEnvironment[ resolveEnvironmentAsName( value.id ) ];
			
		}
		
		
		
		/**
		* Resuelve el NOMBRE del ENVIRONMENT por el numero de ID.
		* @param	value	Identificador numerico.
		* @return	String
		*/
		public static function resolveEnvironmentAsName( value:int ):String {
			
			switch( value ) {
				
				case 1:
					return LOCAL.name;
					break;
				case 2:
					return REMOTE.name;
					break;
				case 0:
				default:
					return OUTPUT.name;
					break;
				
			}
			
		}
		
		
		
		/**
		* Constructor.
		* @param	name	Identificador literal
		* @param	id		Identificador numerico
		* @return	LogEnvironment
		*/
		public function LogEnvironment( name:String, id:int ) {
			
			super( name, id, "LogEnvironment" );
			
		}
		
	}
	
}
