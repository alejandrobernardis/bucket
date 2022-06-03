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

	import com.emc2zen.data.iterator.AbstractIterator;

	/**
	* Modelo abstracto de interacion para objetos.
	* @author	PollyJex
	*/
	public class AbstractObjectIterator extends AbstractIterator {
		
		/**
		* Referencia del OBJECT.
		*/
		private var _object:*;
		
		/**
		* Referencia de la clave con respecto al puntero de lectura.
		*/
		private var _key:String;
		
		
		
		/**
		* Constructor.
		* @param	value	Valor a iterar.
		* @return	AbstractObjectIterator
		*/
		public function AbstractObjectIterator( value:Array, reference:* ) {
			
			this._object = reference;
			super( value );
			
			reset();
			
		}
		
		
		
		/**
		* Retorna la clave actual del puntero.
		* @param	void
		* @return	String
		*/
		public function key():String {
			
			return super.value();
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro.
		* @param	void
		* @return	*
		*/
		public override function next():* {
			
			_key = super.next();
			return ResolveGetValue();
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		public override function peek():* {
			
			return ResolveGetValue( true );
			
		}
		
		/**
		* Remueve del registro el ultimo elemento y retorna su valor.
		* @param	void
		* @return	*
		*/
		public override function remove():* {
			
			var value:* = ResolveGetValue();
			
			ResolveRemove();
			super.remove();	
			
			return value;
			
		}
		
		/**
		* Reseta el puntero de lectura.
		* @param	void
		* @return	void
		*/
		public override function reset():void {
			
			super.reset();
			_key = new String();
			
		}
		
		/**
		* Mueve el puntero de lectura al valor definido por value y retorna su valor.
		* @param	value	Posicion del puntero.
		* @return	*
		*/
		public override function seek( value:int ):* {
			
			_key = super.seek( value );
			return ResolveGetValue();
			
		}
		
		/**
		* Retorna el valor asociado a la posicion actual del puntero.
		* @param	void
		* @return	*
		*/
		public override function value():* {
			
			return ResolveGetValue();
			
		}		
		
		
		
		/**
		* Referencia del OBJETO.
		*/
		protected function get data():* {
			return _object;
		}
		
		/**
		* Resuelve el retorno del valor de la clave.
		* @param	value 	TRUE:PEEK | FALSE:KEY
		* @return	*
		*/
		protected function ResolveGetValue( value:Boolean = false ):* {
			
			if( ! value ){
				return _object[ key() ];
			}
			
			return _object[ super.peek() ];
			
		}
		
		/**
		* Resuelve el remover del registro el ultimo elemento y retorna su valor.
		* @param	void
		* @return	void
		*/
		protected function ResolveRemove():void {
			
			delete _object[ key() ];
			
		}
		
	}
	
}