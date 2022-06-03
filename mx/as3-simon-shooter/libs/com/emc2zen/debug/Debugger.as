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

package com.emc2zen.debug {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.debug.Logger;
	import com.emc2zen.debug.log.LogEnvironment;
	import com.emc2zen.debug.log.LogEvent;
	import com.emc2zen.debug.log.LogLevel;

	/**
	* API de implementacion para el proceso de DEBUGGIN.
	* @author	PollyJex
	*/
	public class Debugger extends CoreStatic {
		
		/**
		* Debug NONE, Default debug.
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function NONE( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.NONE, context ).concat( rest ) );
			}
		}
		
		/**
		* Debug INFO.
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function INFO( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.INFO, context ).concat( rest ) );
			}
		}
		
		/**
		* Debug DEBUG.
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function DEBUG( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.DEBUG, context ).concat( rest ) );
			}
		}
		
		/**
		* Debug WARNING
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function WARNING( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.WARNING, context ).concat( rest ) );
			}
		}
		
		/**
		* Debug ERROR.
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function ERROR( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.ERROR, context ).concat( rest ) );
			}
		}
		
		/**
		* Debug CRITICAL.
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function CRITICAL( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.CRITICAL, context ).concat( rest ) );
			}
		}
		
		/**
		* Debug FATAL.
		* @param	context		Objeto a debuguear.
		* @param	rest		...
		* @return	void
		*/
		public static function FATAL( context:*, ...rest:Array ):void {
			if( active() ) {
				Logger.LOG.apply( Logger, new Array( LogLevel.FATAL, context ).concat( rest ) );
			}
		}
		
		
		
		/**
		* Activa y desactiva el proceso de DEBUGGIN, en caso de no pasarse un parametro retorna el estado actual.
		* @param	value	NULL | TRUE | FALSE.
		* @return	Boolean
		*/
		public static function active( value:* = null ):Boolean {
			
			return Logger.active( value );
			
		}
		
		/**
		* Setea el modo de traceo en el proceso de DEBUGGIN, en caso de no pasarse un parametro retorna el estado actual.
		* @param	value	NULL | LOCAL | REMOTE | OUTPUT.
		* @return	LogEnvironment
		*/
		public static function environment( value:LogEnvironment = null ):LogEnvironment {
			
			return Logger.environment( value );
			
		}
		
	}
	
}