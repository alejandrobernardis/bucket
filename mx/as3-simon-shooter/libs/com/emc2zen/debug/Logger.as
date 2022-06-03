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

	import com.emc2zen.core.CoreInterface;
	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.debug.log.LogEnvironment;
	import com.emc2zen.debug.log.LogEvent;
	import com.emc2zen.debug.log.LogLevel;
	import com.emc2zen.util.ClassUtil;
	import com.emc2zen.util.TypeUtil;
	import flash.events.Event;
	import flash.events.EventDispatcher;

	/**
	* API de implementacion para el proceso de comunicacion entre la API del DEBUGGER y la API de la CONSOLE.
	* @author	PollyJex
	*/
	public class Logger extends EventDispatcher implements CoreInterface {
		
		/**
		* Instacia singleton.
		*/
		private static var $singleton:Logger;
		
		/**
		* Last Level.
		*/
		private var _level:LogLevel;
		
		/**
		* Last Context.
		*/
		private var _context:*;
		
		/**
		* Last Optional Properties.
		*/
		private var _property:Array;
		
		/**
		* Estado del proceso de DEBUGGIN.
		* Default FALSE | TRUE.
		*/
		private var _enabled:Boolean = false;
		
		/**
		* Entorno del proceso de DEBUGGIN.
		* Default OUTPUT | LOCAL | REMOTE.
		*/
		private var _environment:LogEnvironment = LogEnvironment.OUTPUT;
		
		
		
		/**
		* Constructor.
		* @param	access	Acceso privado.
		* @return	Logger
		*/
		public function Logger( access:SingletonPrivate = null ) {
			
			if( ! TypeUtil.isNull( access ) ){
				
				super( this );
				
			}else{
				
				new CoreStatic( this );
				
			}
			
		}
		
		
		
		/**
		* Realiza la conexion con el enorno de DEBUGGIN (Console).
		* @param	level		Level del DEBUGGIN.
		* @param	context		Contexto del DEBUGGIN.
		* @param	rest		...
		* @return	void
		*/
		public static function LOG( level:LogLevel, context:* = null, ...rest:Array ):void {
			
			var ref:Logger = getInstance();
			
			ref._level = LogLevel.verifyLevel( level );
			ref._context = context;
			ref._property = rest;	
			
			trace( new Date(), "[" + ref._level + "]:", ClassUtil.fullName( ref._context ), ">>>", ref._property.join( " " ) );
			dispatchEvent( new LogEvent( LogEvent[ ref._level ], ref ) );
			
		}
		
		
		
		/**
		* Retorna el LEVEL.
		* @param	Void
		* @return	LogLevel
		*/
		public static function GET_LEVEL():LogLevel {
			
			return getInstance()._level;
			
		}
		
		/**
		* Retorna el CONTEXT.
		* @param	Void
		* @return	LogLevel
		*/
		public static function GET_CONTEXT():* {
			
			return getInstance()._context;
			
		}
		
		/**
		* Retorna las PROPERTY.
		* @param	Void
		* @return	LogLevel
		*/
		public static function GET_PROPERTY():Array {
			
			return getInstance()._property;
			
		}
		
		
		
		/**
		* Activa y desactiva el proceso de LOGGER, en caso de no pasarse un parametro retorna el estado actual.
		* @param	value	NULL | TRUE | FALSE.
		* @return	Boolean
		*/
		public static function active( value:* = null ):Boolean {
			
			if( !TypeUtil.isNull( value ) ){
				getInstance()._enabled = value;
			}
			
			return getInstance()._enabled;
			
		}
		
		/**
		* Setea el modo de traceo en el proceso de LOGGER, en caso de no pasarse un parametro retorna el estado actual.
		* @param	value	NULL | LOCAL | REMOTE | OUTPUT.
		* @return	LogEnvironment
		*/
		public static function environment( value:LogEnvironment = null ):LogEnvironment {
			
			if( !TypeUtil.isNull( value ) ){
				getInstance()._environment = value;
			}
			
			return getInstance()._environment;
			
		}
		
		
		
		/**
		* Retorna una instacia de la clase.
		* @param	void
		* @return	Logger
		*/
		private static function getInstance():Logger {
			
			if( TypeUtil.isNull( $singleton ) ) {
				$singleton = new Logger( new SingletonPrivate() );
			}
			
			return $singleton;
			
		}	
		
		
		
		/**
		* ADD EVENT.
		* @param	type
		* @param	listener
		* @param	useCapture
		* @param	priority
		* @param	useWeakReference
		* @return	void
		*/
		public static function addEventListener( type:String, listener:Function, useCapture:Boolean = false, priority:int = 0, useWeakReference:Boolean = false ):void {
			getInstance().addEventListener( type, listener, useCapture, priority, useWeakReference );
		}
		
		/**
		* DISPATCH EVENT.
		* @param	event
		* @return	Boolean
		*/
		public static function dispatchEvent( event:Event ):Boolean {
			return getInstance().dispatchEvent( event );
		}
		
		/**
		* HAS EVENT.
		* @param	type
		* @return	Boolean
		*/
		public static function hasEventListener( type:String ):Boolean {
			return getInstance().hasEventListener( type );
		}
		
		/**
		* REMOVE EVENT.
		* @param	type
		* @param	listener
		* @param	useCapture
		* @return	void
		*/
		public static function removeEventListener( type:String, listener:Function, useCapture:Boolean = false ):void  {
			getInstance().removeEventListener( type, listener, useCapture );
		}
		
		/**
		* WILL TRIGGER.
		* @param	type
		* @return	Boolean
		*/
		public static function willTrigger( type:String ):Boolean {
			return getInstance().willTrigger( type );
		}
		
	}
	
}

/**
* Implementacion que asegura que la clase sea utilizada bajo el patron singleton.
* @author	PollyJex
*/
final class SingletonPrivate {}
