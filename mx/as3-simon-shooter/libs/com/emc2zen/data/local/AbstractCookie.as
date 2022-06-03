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

package com.emc2zen.data.local {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.ICookie;
	import com.emc2zen.data.iterator.HashMapIterator;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.util.ArgumentsUtil;
	import com.emc2zen.util.TypeUtil;
	import flash.events.NetStatusEvent;
	import flash.net.SharedObject;
	import flash.net.SharedObjectFlushStatus;

	/**
	* Modelo abstracto para la implementacion de datos temporales. SharedObject.
	* @author	PollyJex
	*/
	public class AbstractCookie extends CoreObject implements ICookie {
		
		/**
		* Tama&ntilde;o por default de los objetos compartidos.
		*/
		public static const DEFAULT_SIZE:int = 5120;
		
		
		
		/**
		* Const COOKIE_CREATE
		*/
		private static const COOKIE_CREATE:String = "CREATE SUCCESS";
		
		/**
		* Const COOKIE_CAPTURE
		*/
		private static const COOKIE_CAPTURE:String = "CAPTURE SUCCESS";
		
		/**
		* Const COOKIE_CAPTURE_ALL
		*/
		private static const COOKIE_CAPTURE_ALL:String = "CAPTURE ALL SUCCESS";
		
		/**
		* Const COOKIE_CAPTURE_FAILED
		*/
		private static const COOKIE_CAPTURE_FAILED:String = "CAPTURE FAILED";
		
		/**
		* Const COOKIE_CLEAR
		*/
		private static const COOKIE_CLEAR:String = "CLEAR SUCCESS";
		
		/**
		* Const COOKIE_REMOVE
		*/
		private static const COOKIE_REMOVE:String = "REMOVE SUCCESS";
		
		/**
		* Const COOKIE_REMOVE_ALL
		*/
		private static const COOKIE_REMOVE_ALL:String = "REMOVE ALL SUCCESS";
		
		/**
		* Const COOKIE_REMOVE_FAILED
		*/
		private static const COOKIE_REMOVE_FAILED:String = "REMOVE FAILED";
		
		/**
		* Const COOKIE_UPDATE
		*/
		private static const COOKIE_UPDATE:String = "UPDATE SUCCESS";
		
		/**
		* Const COOKIE_UPDATE_FAILED
		*/
		private static const COOKIE_UPDATE_FAILED:String = "UPDATE FAILED";
		
		/**
		* Const COOKIE_UPDATE_PENDING
		*/
		private static const COOKIE_UPDATE_PENDING:String = "UPDATE PENDING";
		
		
		
		/**
		* Registro de actividad.
		*/
		private static var $record:HashMap;
		
		
		
		/**
		* Referencia del objeto temporal.
		*/
		private var _cookie:SharedObject;
		
		/**
		* Referencia del handler.
		*/
		private var _handler:Function;
		
		/**
		* Nombre del objeto temporal.
		*/
		private var _name:String;
		
		/**
		* Tama&ntilde;o del objeto temporal.
		*/
		private var _size:int;
		
		
		
		/**
		* Constructor.
		* @param	name	Nombre del objeto.
		* @param	size	Tama&ntilde;o del objeto.
		* @return	AbstractCookie
		*/
		public function AbstractCookie( name:String, size:int = DEFAULT_SIZE ) {
			
			_name = name;
			_size = size;
			
			if( TypeUtil.isNull( $record ) ){
				$record = new HashMap();
			}
			
			CreateConexion();
			
		}
		
		
		
		/**
		* Captura los valores de la lista pasada como parametro.
		* @param	rest 	Lista de variables a capturar, si rest es igual a cero retorna todo el contenido 
		* 					y si no existe contenido retorna null.
		* @return	*
		*/
		public function capture( ...rest ):* {
			
			if( ! TypeUtil.isEmpty( rest ) ){
				
				var objTmp:* = ResolveCaptureOrRemove( COOKIE_CAPTURE, rest );
				
				if( ! TypeUtil.isNull( objTmp ) ){
					return objTmp;
				}
				
			}else{
				
				RegisterActivity( COOKIE_CAPTURE_ALL );
				return _cookie.data;
				
			}
			
			RegisterActivity( COOKIE_CAPTURE_FAILED );
			return null;
			
		}
		
		/**
		* Remueve todo el contenido del objeto y elimina el objeto del disco.
		* @param	void
		* @return	void
		*/
		public function clear():void {
			
			_cookie.clear();
			RegisterActivity( COOKIE_CLEAR );
			
		}
		
		/**
		* Remueve los valores de la lista pasada como parametro y retorna un objeto con los valores respectivos.
		* @param	rest 	Lista de variables a remover, si rest es igual a cero o no existe el contenido retorna false.
		* @return	*
		*/
		public function remove( ...rest ):* {
			
			var objTmp:*;
			
			if( ! TypeUtil.isEmpty( rest ) ){
				
				objTmp = ResolveCaptureOrRemove( COOKIE_REMOVE, rest );
				
				if( ! TypeUtil.isNull( objTmp ) ){
					return objTmp;
				}
				
			}else{
				
				objTmp = _cookie.data;
				
				clear();
				CreateConexion();
				
				RegisterActivity( COOKIE_REMOVE_ALL );
				return objTmp;
				
			}
			
			RegisterActivity( COOKIE_REMOVE_FAILED );
			return null;
			
		}
		
		/**
		* Inserta los valores pasados como parametros en el objeto.
		* @param	key			Nombre de la variable (String). Lista de valores (Object).
		* @param	value		Valor de la variable en caso de que key sea del tipo String.
		* @param	handler		Funcion de respaldo en caso de que la insercion quede en estado de PENDING.
		* 						<p>Cuando se ejecute el evento, el mismo retornara dos valores success:Boolena y 
		* 						event:NetStatusEvent, el primero retorna el estado de la accion y el segundo una 
		* 						referencia al evento ejecutado.</p>
		* @return	Boolean
		*/
		public function update( key:*, value:* = null, handler:Function = null ):Boolean {
			
			if( ! TypeUtil.isEmpty( key ) ){
				
				if( ! TypeUtil.isNull( value ) ){
					
					_cookie.data[ key ] = value;
					
				}else if( TypeUtil.isObject( key ) ){
					
					for( var a:String in key ){
						_cookie.data[ a ] = key[ a ];
					}
					
				}
				
				var flushStatus:String = null;
					
				try {
					flushStatus = _cookie.flush( _size );
				}catch( error:Error ){
					throw new Error( "Could not write SharedObject to disk" );
				}
				
				if( ! TypeUtil.isNull( flushStatus ) ){
					
					switch( flushStatus ){
						
						case SharedObjectFlushStatus.PENDING:
							_handler = handler;
							_cookie.addEventListener( NetStatusEvent.NET_STATUS, ResolveEvent );
							break;
							
						case SharedObjectFlushStatus.FLUSHED:
							RegisterActivity( COOKIE_UPDATE );
							return true;
							break;
						
					}
					
				}
				
				RegisterActivity( COOKIE_UPDATE_PENDING );
				return false;
				
			}
			
			RegisterActivity( COOKIE_UPDATE_FAILED + " isEMPTY" );
			return false;
			
		}	
		
		
		
		/**
		* Retorna el registro de actividad.
		* @param	void
		* @return	HashMap
		*/
		public static function CaptureActivity():HashMap {
			
			return $record;
			
		}
		
		/**
		* Retorna el registro de actividad para iteracion.
		* @param	void
		* @return	HashMapIterator
		*/
		public static function CaptureActivityFotIterator():HashMapIterator {
			
			return new HashMapIterator( $record );
			
		}
		
		
		
		/**
		* Crea la conexion con el objeto.
		* @param	void
		* @return	void
		*/
		private function CreateConexion():void {
			
			_cookie = SharedObject.getLocal( _name );
			RegisterActivity( COOKIE_CREATE );
			
		}
		
		/**
		* Administra el registro de actividad.
		* @param	action	Accion realizada.
		* @return	void
		*/
		private function RegisterActivity( action:String ):void {
			
			$record.put( _name, action );
			
		}
		
		/**
		* Resuelve la implementacion de los metodos CAPTURE y REMOVE.
		* @param	action		Accion ejecutada.
		* @param	reference	Lista de variables.
		* @return	*
		*/
		private function ResolveCaptureOrRemove( action:String, reference:Array ):* {
			
			var objCou:int = 0;
			var objTmp:Object = new Object();
			var arrTmp:Array = ArgumentsUtil.Verify( reference );
			
			if( arrTmp.length < 2 && ! TypeUtil.isString( arrTmp[ 0 ] ) ){
				arrTmp[ 0 ] = String( arrTmp[ 0 ] );
			}
			
			VerifyList: for( var a:String in _cookie.data ) {
				
				if( arrTmp.indexOf( a ) != -1 ){
					
					objTmp[ a ] = _cookie.data[ a ];
					
					if( action != COOKIE_CAPTURE ){
						delete _cookie.data[ a ];
					}
					
					objCou++;
					
					if( objCou > arrTmp.length - 1 ){
						break VerifyList;
					}
					
				}
				
			}
			
			if( objCou > 0 ){
				RegisterActivity( action );
				return objTmp;
				/**
				* Esta linea define que si el lago del obj es menor a 
				* 2 retorne solo el valor encontrado (modelo viejo)
				* return ( objCou > 1 ) ? objTmp : objTmp[ arrTmp ];
				*/				
			}
			
			return null;
			
		}
		
		/**
		* Resuelve la ejecucion del evento en caso de que la insercion que en modo de pending.
		* <p>Cuando se ejecute el evento, el mismo retornara dos valores success:Boolena y event:NetStatusEvent, 
		* el primero retorna el estado de la accion y el segundo una referencia al evento ejecutado.</p>
		* @param	event	Referencia del evento.
		* @return	void
		*/
		private function ResolveEvent( event:NetStatusEvent ):void {
			
			var success:Boolean;
			
			switch( event.info.code ){
				
				case "SharedObject.Flush.Success":
					RegisterActivity( COOKIE_UPDATE );
					success = true;
					break;
					
				case "SharedObject.Flush.Failed":
					RegisterActivity( COOKIE_UPDATE_FAILED );
					success = false;
					break;
				
			}
			
			if( ! TypeUtil.isNull( _handler ) ){
				_handler( success, event );
			}
			
			_cookie.removeEventListener( NetStatusEvent.NET_STATUS, ResolveEvent );
			
		}
		
		
		
	}
	
}
