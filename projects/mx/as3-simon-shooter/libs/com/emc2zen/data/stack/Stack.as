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

package com.emc2zen.data.stack {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.IStack;

	/**
	* Modelo basico de una estrucutra de dato del tipo Stack.
	* @author	PollyJex
	*/
	public class Stack extends CoreObject implements IStack {
		
		/**
		* Registro.
		*/
		private var _record:Array;
		
		/**
		* Tama&ntilde;o del registro.
		*/
		private var _capacity:int;
		
		
		
		/**
		* Constructor.
		* @param	capacity 	Tama&ntilde;o del Stack.
		* @return	Stack
		*/
		public function Stack( capacity:int = 0 ) {
			
			_capacity = capacity;
			clear();
			
		}
		
		
		
		/**
		* Retorna la capacidad disponible en el registro.
		* @param	void
		* @return	int
		*/
		public function availableCapacity():int {
			
			return new int( capacity() - size() );
			
		}
		
		/**
		* Retorna la capacidad del registro.
		* @param	void
		* @return	int
		*/
		public function capacity():int {
			
			return _capacity;
			
		}
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		public function clear():void {
			
			_record = new Array();
			
		}
		
		/**
		* Verifica si existe value en el registro.
		* @param	value 	Valor a verificar.
		* @return	Boolean
		*/
		public function contains( value:* ):Boolean {
			
			return new Boolean( _record.indexOf( value ) != -1 );
			
		}
		
		/**
		* Verifica si en registro se encuentra vacio.
		* @param	void
		* @return	Boolean
		*/
		public function isEmpty():Boolean {
			
			return new Boolean( size() < 1 );
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		public function peek():* {
			
			return _record[ size() - 2 ];
			
		}
		
		/**
		* Elimina el ultimo elemento del registro y retorna su valor. 
		* @param	void
		* @return	*
		*/
		public function pop():* {
			
			if( ! isEmpty() ){
				
				return _record.pop();
				
			}
			
			return null;
			
		}
		
		/**
		* Agrega un elemento al inicio del registro y retorna el nuevo tama&ntilde;o del registro.
		* @param	value	Objeto a insertar.
		* @return	void
		*/
		public function push( value:* ):void {
			
			if( size() < capacity() ){
				
				_record.push( value );
				
			}
			
		}
		
		/**
		* Busca y retorna el valor de value en el registro, en caso de no existir retorna null.
		* @param	value 	Objeto a buscar.
		* @return	*
		*/
		public function search( value:* ):* {
			
			if( ! isEmpty() ){
				
				return _record.indexOf( value );
				
			}
			
			return null;
			
		}
		
		/**
		* Retorna el tama&ntilde; del registro.
		* @param	void
		* @return	int
		*/
		public function size():int {
			
			return _record.length;
			
		}
		
		/**
		* Retorna una copia del registro para ser iterado.
		* @param	void
		* @return	Array
		*/
		public function toArray():Array {
			
			return _record.slice().reverse();
			
		}
		
		/**
		* Retorna el valor del primer elemento del registro.
		* @param	void
		* @return	*
		*/
		public function top():* {
			
			return _record[ size() - 1 ];
			
		}		
		
	}
	
}
