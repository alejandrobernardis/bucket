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
	import com.emc2zen.data.IIterator;
	import com.emc2zen.util.NumberUtil;

	/**
	* Modelo abstracto de interacion.
	* @author	PollyJex
	*/
	public class AbstractIterator extends CoreObject implements IIterator {
		
		/**
		* Registro. Referencia del ARRAY.
		*/
		private var _record:Array;
		
		/**
		* Puntero de lectura.
		*/
		private var _index:int;
		
		
		
		/**
		* Constructor.
		* @param	value	Valor a iterar.
		* @return	AbstractIterator
		*/
		public function AbstractIterator( value:Array ) {
			
			this._record = value;
			reset();
			
		}
		
		
		
		/**
		* Verifica si existe un elemento posterior al actual en el registro.
		* @param	void
		* @return	Boolean
		*/
		public function hasNext():Boolean {
			
			return new Boolean( index() < ( size() - 1 ) );
			
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
		* Retorna el valor del siguiente elemento del registro.
		* @param	void
		* @return	*
		*/
		public function next():* {
			
			return ResolveNext();
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		public function peek():* {
			
			return ResolvePeek();
			
		}
		
		/**
		* Remueve del registro el ultimo elemento y retorna su valor.
		* @param	void
		* @return	*
		*/
		public function remove():* {
			
			return _record.splice( _index --, 1 );
			
		}
		
		/**
		* Reseta el puntero de lectura.
		* @param	void
		* @return	void
		*/
		public function reset():void {
			
			_index = -1;
			
		}
		
		/**
		* Mueve el puntero de lectura al valor definido por value y retorna su valor.
		* @param	value	Posicion del puntero.
		* @return	*
		*/
		public function seek( value:int ):* {
			
			ResolveSeek( value );
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
			
			return this._record;
			
		}
		
		/**
		* Retorna el valor asociado a la posicion actual del puntero.
		* @param	void
		* @return	*
		*/
		public function value():* {
			
			return _record[ index() ];
			
		}
	
		
		
		/**
		* Resuelve el valor del siguiente elemento del registro.
		* @param	void
		* @return	*
		*/
		protected function ResolveNext():* {
			
			return _record[ ++ _index ];
			
		}
		
		/**
		* Resuelve el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		protected function ResolvePeek():* {
			
			return _record[ index() + 1 ];
			
		}		
		
		/**
		* Resuelve el movimiento del puntero de lectura al valor definido por value.
		* @param	value	Posicion del puntero.	
		* @return	void
		*/
		protected function ResolveSeek( value:int ):void {
			
			_index = NumberUtil.toLimit( value - 1, 0, size() - 1 );
			
		}
		
	}
	
}
