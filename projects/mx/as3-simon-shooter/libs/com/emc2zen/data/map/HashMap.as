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

package com.emc2zen.data.map {
	
	/**
	* @import
	*/

	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.IHashMap;
	import com.emc2zen.data.type.AbstractType;
	import com.emc2zen.util.ArgumentsUtil;
	import com.emc2zen.util.TypeUtil;
	import flash.utils.Dictionary;

	/**
	* Modelo basico de una estrucutra de dato del tipo HashMap.
	* @author	PollyJex
	*/
	public class HashMap extends CoreObject implements IHashMap {
		
		/**
		* Registro del HashMap.
		*/
		private var _record:Dictionary;
		
		/**
		* Recuento de la cantidad de registros del HashMap.
		*/
		private var _recordCount:int;
		
		/**
		* Uso de la referencia debil.
		*/
		private var $weakKeys:Boolean;
		
		
		
		/**
		* Constructor.
		* @param	weakKeys	Uso de referencias debiles.
		* @return	HashMap
		*/
		public function HashMap( weakKeys:Boolean = false ) {
			
			this.$weakKeys = weakKeys;
			clear();
			
		}
		
		
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		public function clear():void {
			
			_record = new Dictionary( $weakKeys );
			_recordCount = 0;
			
		}
		
		/**
		* Reinicia el registro ecepto las claves pasadas como parametros
		* @param	rest	Lita de claves.
		* @return	void
		*/
        public function clearAllExcept( ...rest ):void {
			
			if( rest.length < 1 ){
				return;
			}
			
			var dicTmp:Dictionary = _record;
			var lisTmp:Array = ArgumentsUtil.Verify( rest );
			
			clear();
			
			for( var a:int = 0; a < lisTmp.length; a++ ){	
				
				put( lisTmp[ a ], dicTmp[ lisTmp[ a ] ] );
				
			}			
			
		}
		
		/**
		* Verifica si el registro posee la clave.
		* @param	key		Clave.
		* @return	Boolean
		*/
		public function containsKey( key:String ):Boolean {
			
			return new Boolean( ! TypeUtil.isUndefined( getValue( key ) ) );
			
		}
		
		/**
		* Verifica si el registro posee el valor.
		* @param	value	Valor.
		* @return	Boolean
		*/
        public function containsValue( value:* ):Boolean {
			
			return new Boolean( ! TypeUtil.isNull( ResolveKeyValue( value ) ) );
			
		}
		
		/**
		* Retorna la clave asociada al valor.
		* @param	value	Valor.
		* @return	String
		*/
		public function getKey( value:* ):String {
			
			return ResolveKeyValue( value );
			
		}
		
		/**
		* Retorna una lista con las claves existentes en el registro.
		* @param	voir
		* @return	Array
		*/
		public function getKeys():Array {
			
			return ResolveListOfKeysOrValues();
			
		}
		
		/**
		* Retorna el valor asociado a la clave.
		* @param	key		String
		* @return	*
		*/
        public function getValue( key:String ):* {
			
			return _record[ key ];
			
		}
		
		/**
		* Retorna una lista con los valores existentes en el registro.
		* @param	void
		* @return	Array
		*/
        public function getValues():Array {
			
			return ResolveListOfKeysOrValues( true );
			
		}
		
		/**
		* Verifica si en registro se encuentra vacio.
		* @param	void
		* @return	Boolean
		*/
		public function isEmpty():Boolean {
			
			return new Boolean( _recordCount < 1 );
			
		}
		
		/**
		* Inserta clave->valor en el regitro.
		* @param	key		Clave.
		* @param	value	Valor.
		* @return	void
		*/
		public function put( key:String, value:* ):void {
			
			ResolvePutForType( key, value );
			
		}
		
		/**
		* Inserta una lista de clave->valor en el regitro.
		* @param	key		Lista de claves, Object o HashMap
		* @param	value	Lista de valores.
		* @return	void
		*/
		public function putAll( key:*, value:* = null ):void {
			
			ResolvePutAll( key, value );
			
		}
		
		/**
		* Remueve una clave y su valor asociado del registro.
		* @param	key		Clave.
		* @return	void
		*/
        public function remove( key:String ):void {
			
			if( containsKey( key ) ){
				
				delete _record[ key ];
				_recordCount --;
				
			}
			
		}
		
		/**
		* Reseta todas las claves del resgitro revalorizandolas con "".
		* @param	void
		* @return	void
		*/
		public function reset():void {    
			
			ResolveResetKey();
			
		}
		
		/**
		* Reseta todas las claves del resgitro revalorizandolas con "", ecepto las pasadas como parametro.
		* @param	rest	Lista de las claves.
		* @return	void
		*/
        public function resetAllExcept( ...rest ):void {   
			
			if( rest.length < 1 ){
				return;
			}	
			
			var lisTmp:Array = ArgumentsUtil.Verify( rest );
			
			ResolveResetKey( lisTmp );
			
		}
		
		/**
		* Retorna el tama&ntilde;o del registro.
		* @param	void
		* @return	int
		*/
        public function size():int { 
			
			return _recordCount;	
			
		}
		
		
		
		/**
		* Resuelve la insercion de dato, dependiendo del tipo.
		* @param	key		Lista de claves.
		* @param	value	Lista de valores.
		* @param	type	Tipo de dato.
		* @return	void
		*/
		protected function ResolvePutForType( key:*, value:* = null, type:AbstractType = null ):void {
			
			if( ! TypeUtil.isNull( type ) && ! type.isSupported( value ) ){ 
				return;
			}			
			
			if( ! containsKey( key ) ){
				_recordCount ++;
			}
			
			_record[ key ] = value;	
			
		}
		
		/**
		* Resuelve la insercion de dato, dependiendo del tipo.
		* @param	key		Lista de claves.
		* @param	value	Lista de valores.
		* @param	type	Tipo de dato.
		* @return	void
		*/
		protected function ResolvePutAll( key:*, value:* = null, type:AbstractType = null ):void {
			
			if( TypeUtil.isNull( key ) ){
				return;
			}
			
			var keyTmp:Array;
			var valTmp:Array;
			
			if( TypeUtil.thisIs( key, HashMap ) && TypeUtil.isNull( value ) ){
				
				keyTmp = key.getKeys();
				valTmp = key.getValues();
				
			}else if( TypeUtil.isArray( key ) && TypeUtil.isArray( value ) ){
				
				keyTmp = key;
				valTmp = value;
				
			}else if( TypeUtil.isObject( key ) ){
				
				for( var a:String in key ){
					
					ResolvePutForType( key, value, type );
					
				}
				
				return;
				
			}
			
			for( var b:int = 0; b < keyTmp.length; b++  ){
				
				ResolvePutForType( keyTmp[ b ], valTmp[ b ], type );
				
			}
			
		}
		
		
		
		/**
		* Metodo AUX que retorna una lista con las claves o los valores existentes en el registro.
		* @param	value	KEY:FALSE | VALUE:TRUE
		* @return	String
		*/
		private function ResolveListOfKeysOrValues( value:Boolean = false ):Array {
			
			var arrTmp:Array = new Array();
			var valTmp:*;
			
			for( var a:String in _record ){
				
				if( ! value ){
					valTmp = a;
				}else{
					valTmp = getValue( a );
				}
				
				arrTmp.push( valTmp );
				
			}
			
			return arrTmp;
			
		}
		
		/**
		* Metodo AUX que permite la comprobacion de contenio KEY > VALUE.
		* @param	value	valor a buscar
		* @return	String
		*/
		private function ResolveKeyValue( value:* ):String {
			
			for( var a:String in _record ){
				
				if( getValue( a ) === value ) {
					return a;
				}
				
			}
			
			return null;
			
		}	
		
		/**
		* Resuelve el reseteo de las claves.
		* @param	list	Lista de claves que no se deben resetear.
		* @return	void
		*/
		private function ResolveResetKey( list:Array = null ):void {
			
			var resTmp:Boolean;
			
			for( var a:String in _record ){
				
				resTmp = true;
				
				if( ! TypeUtil.isNull( list ) ){
					
					VerifyList: for( var b:int = 0; b < list.length; b ++ ){
						
						if( a == list[ b ] ) {
							resTmp = false;
							break VerifyList;
						}
						
					}					
					
				}
				
				if( resTmp ){
					
					_record[ a ] = null;
					
				}
				
			}
			
		}
		
	}
	
}
