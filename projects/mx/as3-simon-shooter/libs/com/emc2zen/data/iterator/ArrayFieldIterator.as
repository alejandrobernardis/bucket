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
	import com.emc2zen.util.NumberUtil;
	import com.emc2zen.util.TypeUtil;

	/**
	* Modelo basico de interacion para objetos de tipo Array discriminado por campo.
	* @author	PollyJex
	*/
	public class ArrayFieldIterator extends AbstractIterator {
		
		/**
		* Referencia del nombre del campo a discriminar.
		*/
		private var _field:String;
		
		
		
		/**
		* Constructor.
		* @param	value	Array a evaluar.
		* @param	field	Campo a discriminar.
		* @return	ArrayFieldIterator
		*/
		public function ArrayFieldIterator( value:Array, field:String = null ) {
			
			this._field = field;			
			super( value );
			
		}
		
		
		
		/**
		* Retorna el valor del siguiente elemento del registro.
		* @param	void
		* @return	*
		*/
		public override function next():* {
			
			return ResolveField( ResolveNext() );
			
		}
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		public override function peek():* {
			
			return ResolveField( ResolvePeek() );
			
		}
		
		/**
		* Mueve el puntero de lectura al valor definido por value y retorna su valor.
		* @param	value	Posicion del puntero.
		* @return	*
		*/
		public override function seek( value:int ):* {
			
			ResolveSeek( value );
			return ResolveField( this.value() );
			
		}
		
		
		
		/**
		* Resulve y retorna el valor por el nombre del campo.
		* @param	value	Valor.
		* @return	*
		*/
		private function ResolveField( value:* ):* {
			
			if( ! TypeUtil.isNull( _field ) ){
				return value[ _field ]; 
			}
			
			return value;
			
		}
		
	}
	
}
