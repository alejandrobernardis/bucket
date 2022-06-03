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

package com.emc2zen.data.type {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreObject;

	/**
	* Modelo basico de un nodo implementado en estructuras de datos.
	* @author	PollyJex
	*/
	public class AbstractNode extends CoreObject {
		
		/**
		* Valor de nodo actual.
		*/
		private var _data:*;
		
		
		
		/**
		* Constructor.
		* @param	data	Valor del nodo actual.
		* @return	AbstractNode
		*/
		public function AbstractNode( data:* = null ) {
			
			this._data = data;
			
		}
		
		
		
		/**
		* Nodo actual. Lectura/Escritura. 
		*/
		public function get data():* {
			return _data;
		}
		
		public function set data( value:* ):void {
			this._data = data;
		}		
		
	}
	
}
