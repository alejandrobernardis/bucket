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

package com.emc2zen.data.queue {

	/**
	* @import
	*/

	import com.emc2zen.data.queue.Queue;
	import com.emc2zen.data.type.AbstractType;

	/**
	* Modelo basico de una estrucutra de dato del tipo Queue discriminada por tipos.
	* @author	PollyJex
	*/
	public class TypedQueue extends Queue {
		
		/**
		* Tipo de datos.
		*/
		private var _type:AbstractType;
		
		
		
		/**
		* Constructor.
		* @param	type		Tipo de dato.
		* @param	capacity 	Tama&ntilde;o del Queue.
		* @return	TypedQueue
		*/
		public function TypedQueue( type:*, capacity:int = 0 ) {
			
			this._type = new AbstractType( type );
			super( capacity );
			
		}
		
		
		
		/**
		* Verifica si existe el valor en el registro.
		* @param	value 	Valor a verificar.
		* @return	Boolean
		*/
		public override function contains( value:* ):Boolean {
			
			if( _type.isSupported( value ) ){
				return super.contains( value );
			}
			
			return false;
			
		}
		
		/**
		* Inserta un valor en el registro de ser posible.
		* @param	value	Valor a insertar.
		* @return	Boolean
		*/
		public override function enqueue( value:* ):Boolean {
			
			if( _type.isSupported( value ) ){
				return super.enqueue( value );
			}
			
			return false;
			
		}
		
		/**
		* Inserta un valor al inicio del registro de ser posible.
		* @param	value	Valor a insertar.
		* @return	Boolean
		*/
		public override function enqueueFront( value:* ):Boolean {
			
			if( _type.isSupported( value ) ){
				return super.enqueueFront( value );
			}
			
			return false;
			
		}
		
	}
	
}
