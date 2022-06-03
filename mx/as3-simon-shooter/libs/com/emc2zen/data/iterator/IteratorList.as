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

package com.emc2zen.data.iterator {

	/**
	* @import
	*/
	
	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.IMap;
	import com.emc2zen.data.IIterator;
	import com.emc2zen.data.IIteratorList;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.data.map.TypedHashMap;
	import com.emc2zen.util.ArgumentsUtil;
	import com.emc2zen.util.IteratorUtil;
	import com.emc2zen.util.NumberUtil;
	import com.emc2zen.util.TypeUtil;

	/**
	* Modelo basico de interacion para objetos de tipo Array, Object o String en modo de lista.
	* @author	PollyJex
	*/
	public class IteratorList extends CoreObject implements IIteratorList {
		
		/**
		* Registro. Referencia del ARRAY.
		*/
		private var _record:Array;
		
		/**
		* Puntero de lectura.
		*/
		private var _index:int;
		
		/**
		* Puntero de lectura interno.
		*/
		private var _internalIndex:int;
		
		/**
		* Referencia del OBJECT.
		*/
		private var _object:*;
		
		/**
		* Referencia del tipo de lista a iterar.
		*/
		private var LIST_TYPE_OBJECT:Boolean;
		
		
		
		/**
		* Constructor.
		* @param	value	Objeto a iterar en modo de lista.
		* @param	type	Referencia del tipo.
		* @return	IteratorList
		*/
		public function IteratorList( value:*, type:* = undefined ) {
			
			LIST_TYPE_OBJECT = false;
			
			if( ! TypeUtil.isArray( value ) ){
				
				if( TypeUtil.isString( value ) ){
					
					value = value.split( "" );
					
				}else{
					
					this._object = value;
					
					if( TypeUtil.thisIs( value, HashMap ) || TypeUtil.thisIs( value, TypedHashMap ) ) {
						value = value.getKeys();
					}else{
						value = IteratorUtil.toArray( value );
					}
					
					LIST_TYPE_OBJECT = true;
					
				}
				
			}
			
			if( ! TypeUtil.isUndefined( type ) ){
				this._record = ArgumentsUtil.DiscriminateForType( value, type );
			}else{
				this._record = value;
			}
			
			reset();
			
		}		
		
		
		
		/**
		* Verifica si existe un elemento posterior al actual en el registro.
		* @param	void
		* @return	Boolean
		*/
		public function hasNext():Boolean {
			
			return new Boolean( _internalIndex < size() );
			
		}
		
		/**
		* Verifica si existe un elemento anterior al actual en el registro.
		* @param	void
		* @return	Boolean
		*/
		public function hasPrevious():Boolean {
			
			return new Boolean( _internalIndex > 0 );
			
		}
		
		/**
		* Retorna la posicion actual del puntero.
		* @param	void
		* @return	int
		*/
		public function index():int {
			
			return _index;
			
		}
		
		/**
		* Retorna la clave actual del puntero.
		* @param	void
		* @return	String
		*/
		public function key():String {
			
			if( LIST_TYPE_OBJECT ) {
				return _record[ index() ];
			}else{
				throw new Error( "This iterator does not support the key() method, if record is Array or String." );
			}
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro.
		* @param	void
		* @return	*
		*/
		public function next():* {
			
			_index = _internalIndex;
			_internalIndex ++;
			
			return value();
			
		}
		
		/**
		* Retorna la clave siguiente del puntero sin modificar el puntero.
		* @param	void
		* @return	*
		*/
		public function nextIndex():* {
			
			return _record[ index() + 1 ];
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		public function peek():* {
			
			if( LIST_TYPE_OBJECT ){
				
				if( TypeUtil.thisIs( _object, HashMap ) ){
					return _object.getValue( nextIndex() );
				}
				
				return _object[ nextIndex() ];
				
			}
			
			return nextIndex();
			
		}
		
		/**
		* Retorna el valor del elemento anterior al actual en el registro.
		* @param	void
		* @return	*
		*/
		public function previous():* {
			
			_internalIndex --;
			_index = _internalIndex;
			
			return value();
			
		}
		
		/**
		* Retorna la clave anterior del puntero sin modificar el puntero.
		* @param	void
		* @return	*
		*/
		public function previousIndex():* {
			
			return _record[ index() - 1 ];
			
		}
		
		/**
		* Remueve del registro el ultimo elemento y retorna su valor.
		* @param	void
		* @return	*
		*/
		public function remove():* {
			
			var retTmp:* = value();
			
			_record.splice( index(), 1 );
			
			if( LIST_TYPE_OBJECT ){
				
				if( TypeUtil.thisIs( _object, HashMap ) ){
					_object.remove();
				}else{
					delete _object[ index() ];
				}				
				
			}
			
			previous();
			
			return retTmp;
			
		}
		
		/**
		* Reseta el puntero de lectura.
		* @param	void
		* @return	void
		*/
		public function reset():void {
			
			_index = 0;
			_internalIndex = 0;
			
		}
		
		/**
		* Mueve el puntero de lectura al valor definido por value y retorna su valor.
		* @param	value	Posicion del puntero.
		* @return	*
		*/
		public function seek( value:int ):* {
			
			_index = NumberUtil.toLimit( value - 1, 0, size() - 1 );
			_internalIndex =  index() + 1;
			
			return this.value();
			
		}
		
		/**
		* Retorna el tama&ntilde;o del registro.
		* @param	void
		* @return	int
		*/
		public function size():int {
			
			return _record.length;
			
		}
		
		/**
		* Retorna el contenido del iterador en formato de Array.
		* @return	Array
		*/
		public function toArray():Array {
			
			return _record;
			
		}
		
		/**
		* Retorna el valor asociado a la posicion actual del puntero.
		* @param	void
		* @return	*
		*/
		public function value():* {
			
			if( LIST_TYPE_OBJECT ){
				
				if( TypeUtil.thisIs( _object, HashMap ) ){
					return _object.getValue( key() );
				}
				
				return _object[ key() ];
				
			}
			
			return _record[ index() ];
			
		}		
		
	}
	
}
