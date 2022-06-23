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

package com.emc2zen.core {

	/**
	* @import
	*/

	import com.emc2zen.core.Constant;
	import com.emc2zen.core.CoreSingleton;
	import com.emc2zen.data.IHashMap;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.util.TypeUtil;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IEventDispatcher;
	import flash.utils.flash_proxy;
	import flash.utils.Proxy
	
	use namespace flash_proxy;

	/**
	* Modelo de dato de enlace GLOBAL. Permite alamcenar VARIABLES y asociar sus cambios a dos eventos CHANGED (add, edit) y REMOVE (delete).
	* @author	PollyJex
	*/
	public dynamic class Global extends Proxy implements IEventDispatcher, IHashMap {
		
		/**
		* Constante de referencia para el reseteo de todas las propiedades.
		*/
		public static const CLEAR_PROPERTY:Constant = new Constant( "CLEAR_PROPERTY", 0, $CLASS_REF );
		
		/**
		* Constante de referencia para el reseteo de varias de propiedades.
		*/
		public static const CLEAR_EXCEPT_PROPERTY:Constant = new Constant( "CLEAR_EXCEPT_PROPERTY", 1, $CLASS_REF );
		
		/**
		* Constante de referencia para la insercion de una propiedad.
		*/
		public static const PUT_PROPERTY:Constant = new Constant( "PUT_PROPERTY", 2, $CLASS_REF );
		
		/**
		* Constante de referencia para la insercion de varias propiedades.
		*/
		public static const PUT_ALL_PROPERTY:Constant = new Constant( "PUT_ALL_PROPERTY", 3, $CLASS_REF );
		
		/**
		* Constante de referencia para la eliminacion de propiedades.
		*/
		public static const REMOVE_PROPERTY:Constant = new Constant( "REMOVE_PROPERTY", 4, $CLASS_REF );
		
		/**
		* Constante de referencia para el reseteo de todas las propiedades.
		*/
		public static const RESET_PROPERTY:Constant = new Constant( "RESET_PROPERTY", 5, $CLASS_REF );
		
		/**
		* Constante de referencia para el reseteo de varias de propiedades.
		*/
		public static const RESET_EXCEPT_PROPERTY:Constant = new Constant( "RESET_EXCEPT_PROPERTY", 6, $CLASS_REF );
		
		
		
		/**
		* Constante de referencia del nombre de la clase.
		*/
		private static const $CLASS_REF:String = "Global";
		
		
		
		/**
		* Instacia singleton.
		*/
		private static var $singleton:Global;
		
		
		
		/**
		* Referencia del despachador.
		*/
		private var _dispatcher:EventDispatcher;
		
		/**
		* Storage
		*/
		private var _storage:HashMap;
		
		
		
		/**
		* Constructor.
		* @param	access		Acceso privado.
		* @return	Global
		*/
		public function Global( access:SingletonPrivate = null ) {
			
			if( ! TypeUtil.isNull( access ) ){
				
				_storage = new HashMap();
				_dispatcher = new EventDispatcher( this );
				
			}else{
				
				new CoreSingleton( this );
				
			}
			
		}
		
		/**
		* Retorna una instacia de la clase.
		* @param	void
		* @return	Global
		*/
		public static function getInstance():Global {
			
			if( TypeUtil.isNull( $singleton ) ) {
				$singleton = new Global( new SingletonPrivate() );
			}
			
			return $singleton;
			
		}
		
		
		
		/**
		* Anula el comportamiento de una propiedad de objeto a la que se puede llamar como funci�n.
		* @param	name	Nombre del metodo.
		* @param	rest	...
		* @return	*
		*/
		override flash_proxy function callProperty( name:*, ...rest ):* {
			
			return getValue( name ).apply( _storage, rest );
			
		}
		
		/**
		* Anula la solicitud de eliminaci�n de una propiedad. Cuando se elimina una propiedad con el operador delete, se llama a este m�todo para realizar la eliminaci�n.
		* @param	name	Nombre de la propiedad.
		* @param	void
		* @return	Boolean
		*/
		override flash_proxy function deleteProperty( name:* ):Boolean {
			
			remove( name );
			return true;
			
		}
		
		/**
		* Anula cualquier solicitud del valor de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @return	*
		*/
		override flash_proxy function getProperty( name:* ):* {
			
			return getValue( name );
			
		}
		
		/**
		* Anula una llamada para cambiar el valor de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @param	value	Valor de la propiedad.
		* @return	void
		*/
		override flash_proxy function setProperty( name:*, value:* ):void {
			
			put( name, value );
			
		}
		
		
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		public function clear():void {
			ResolveKeyValueChanged( null, null, CLEAR_PROPERTY );
		}
		
		/**
		* Reinicia el registro ecepto las claves pasadas como parametros
		* @param	rest	Lita de claves.
		* @return	void
		*/
        public function clearAllExcept( ...rest ):void {		
			ResolveKeyValueChanged( rest, null, CLEAR_EXCEPT_PROPERTY );
		}
		
		/**
		* Verifica si el registro posee la clave.
		* @param	key		Clave.
		* @return	Boolean
		*/
		public function containsKey( key:String ):Boolean {
			return _storage.containsKey( key );
		}
		
		/**
		* Verifica si el registro posee el valor.
		* @param	value	Valor.
		* @return	Boolean
		*/
        public function containsValue( value:* ):Boolean {
			return _storage.containsValue( value );
		}
		
		/**
		* Retorna la clave asociada al valor.
		* @param	value	Valor.
		* @return	String
		*/
		public function getKey( value:* ):String {
			return _storage.getKey( value );
		}
		
		/**
		* Retorna una lista con las claves existentes en el registro.
		* @param	voir
		* @return	Array
		*/
		public function getKeys():Array {
			return _storage.getKeys();
		}
		
		/**
		* Retorna el valor asociado a la clave.
		* @param	key		String
		* @return	*
		*/
        public function getValue( key:String ):* {
			return _storage.getValue( key );
		}
		
		/**
		* Retorna una lista con los valores existentes en el registro.
		* @param	void
		* @return	Array
		*/
        public function getValues():Array {
			return _storage.getValues();
		}
		
		/**
		* Verifica si en registro se enecuentra vacio.
		* @param	void
		* @return	void
		*/
		public function isEmpty():Boolean {
			return _storage.isEmpty();
		}
		
		/**
		* Inserta clave->valor en el regitro.
		* @param	key		Clave.
		* @param	value	Valor.
		* @return	void
		*/
		public function put( key:String, value:* ):void {
			ResolveKeyValueChanged( key, value, PUT_PROPERTY );
		}
		
		/**
		* Inserta una lista de clave->valor en el regitro.
		* @param	key		Lista de claves, Object o HashMap
		* @param	value	Lista de valores.
		* @return	void
		*/
		public function putAll( key:*, value:* = null ):void {
			ResolveKeyValueChanged( key, value, PUT_ALL_PROPERTY );
		}
		
		/**
		* Remueve una clave y su valor asociado del registro.
		* @param	key		Clave.
		* @return	void
		*/
        public function remove( key:String ):void {
			if( containsKey( key ) ){
				ResolveKeyValueChanged( key, null, REMOVE_PROPERTY );
			}
		}
		
		/**
		* Reseta todas las claves del resgitro revalorizandolas con "".
		* @param	void
		* @return	void
		*/
		public function reset():void {    
			ResolveKeyValueChanged( null, null, RESET_PROPERTY );
		}
		
		/**
		* Reseta todas las claves del resgitro revalorizandolas con "", ecepto las pasadas como parametro.
		* @param	rest	Lista de las claves.
		* @return	void
		*/
        public function resetAllExcept( ...rest ):void {   
			ResolveKeyValueChanged( rest, null, RESET_EXCEPT_PROPERTY );
		}
		
		/**
		* Retorna el tama&ntilde;o del registro.
		* @param	void
		* @return	int
		*/
        public function size():int { 
			return _storage.size();
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
		public function addEventListener( type:String, listener:Function, useCapture:Boolean = false, priority:int = 0, useWeakReference:Boolean = false ):void {
			_dispatcher.addEventListener( type, listener, useCapture, priority, useWeakReference );
		}
		
		/**
		* DISPATCH EVENT.
		* @param	event
		* @return	Boolean
		*/
		public function dispatchEvent( event:Event ):Boolean {
			return _dispatcher.dispatchEvent( event );
		}
		
		/**
		* HAS EVENT.
		* @param	type
		* @return	Boolean
		*/
		public function hasEventListener( type:String ):Boolean {
			return _dispatcher.hasEventListener( type );
		}
		
		/**
		* REMOVE EVENT.
		* @param	type
		* @param	listener
		* @param	useCapture
		* @return	void
		*/
		public function removeEventListener( type:String, listener:Function, useCapture:Boolean = false ):void  {
			_dispatcher.removeEventListener( type, listener, useCapture );
		}
		
		/**
		* WILL TRIGGER.
		* @param	type
		* @return	Boolean
		*/
		public function willTrigger( type:String ):Boolean {
			return _dispatcher.willTrigger( type );
		}	
		
		
		
		/**
		* Resuelve el cambio de un KEY > VALUE tanto por PUT o como THIS[K] o la eliminacion por DELETE o como REMOVE
		* @param	name	Key
		* @param	value	Valor
		* @return	void
		*/
		private function ResolveKeyValueChanged( name:*, value:*, action:Constant ):* {
			
			/* 
				
				GlobalEvent.REMOVE:
					CLEAR_PROPERTY
					REMOVE_PROPERTY
				
				GlobalEvent.CHANGED:
					CLEAR_EXCEPT_PROPERTY
					PUT_PROPERTY
					PUT_ALL_PROPERTY
					RESET_PROPERTY
					RESET_EXCEPT_PROPERTY
				
			*/
			
			var argTmp:Array = new Array( action );
			
			if( TypeUtil.isString( name ) ){
				
				var oldValue:* = getValue( name );
				
			}			
			
			if( action == CLEAR_PROPERTY || action == REMOVE_PROPERTY ){
				
				if( ! TypeUtil.isNull( name ) ){
					
					_storage.remove( name );
					argTmp = argTmp.concat( name, oldValue );
					
				}else{
					
					_storage.clear();
					
				}
				
				dispatchEvent( new GlobalEvent( GlobalEvent.REMOVE, argTmp ) );
				return true;
				
			}else{
				
				switch( action ){
					
					case CLEAR_EXCEPT_PROPERTY:
						_storage.clearAllExcept.apply( _storage, name );
						break;
						
					case PUT_PROPERTY:
						
						if( value !== oldValue ){
							_storage.put( name, value );
						}else{
							return -1;
						}
						
						break;
						
					case PUT_ALL_PROPERTY:
						_storage.putAll( name, value );
						break;
						
					case RESET_PROPERTY:
						_storage.reset();
						break;
					
					case RESET_EXCEPT_PROPERTY:
						_storage.resetAllExcept.apply( _storage, name );
						break;
					
				}
				
				if( action != RESET_PROPERTY ){
					
					argTmp = argTmp.concat( name );
					
					if( ( action.id == 3 && ! TypeUtil.isNull( value ) ) || ( action.id == 2 ) ){
						
						argTmp = argTmp.concat( value );
						
						if( action.id == 2 && ! TypeUtil.isUndefined( oldValue ) ){
							
							argTmp = argTmp.concat( oldValue );
							
						}
						
					}					
					
				}	
				
				dispatchEvent( new GlobalEvent( GlobalEvent.CHANGED, argTmp ) );
				
			}
			
			return -1;
			
		}
		
	}
	
}

/**
* Implementacion que asegura que la clase sea utilizada bajo el patron singleton.
* @author	PollyJex
*/
final class SingletonPrivate {}
