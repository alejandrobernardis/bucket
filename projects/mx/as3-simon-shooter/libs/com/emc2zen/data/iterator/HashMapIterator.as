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

	import com.emc2zen.data.iterator.AbstractObjectIterator;
	import com.emc2zen.data.map.HashMap;

	/**
	* Modelo basico de interacion para objetos de tipo HashMap.
	* @author	PollyJex
	*/
	public class HashMapIterator extends AbstractObjectIterator {
		
		/**
		* Constructor.
		* @param	value	HashMap a iterar.
		* @return	HashMapIterator
		*/
		public function HashMapIterator( value:HashMap ) {
			
			super( value.getKeys(), value );
			
		}	
		
		
		
		/**
		* Resuelve el retorno del valor de la clave.
		* @param	value 	TRUE:PEEK | FALSE:KEY
		* @return	*
		*/
		protected override function ResolveGetValue( value:Boolean = false ):* {
			
			if( ! value ){
				return data.getValue( key() );
			}
			
			return data.getValue( super.peek() );
			
		}
		
		/**
		* Resuelve el remover del registro el ultimo elemento y retorna su valor.
		* @param	void
		* @return	void
		*/
		protected override function ResolveRemove():void {
			
			delete data.remove( key() );
			
		}
		
	}
	
}
