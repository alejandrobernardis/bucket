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
	
	import com.emc2zen.core.CoreInterface;
	import flash.events.Event;

	/**
	* Modelo basico de un evento.
	* @author	PollyJex
	*/
	public class CoreEvent extends Event implements CoreInterface {
		
		/**
		* Propiedades del evento, es util para cuando se desea 
		* enviar argumentos ya que esta propiedad los encapsula.
		*/
		private var _property:*;
		
		/**
		* Constructor.
		* @param	type			Nombre del evento.
		* @param	property		Argumentos opcionales.
		* @param	bubbles			Indica si un evento es un evento de propagacion.
		* @param	cancelable		Indica si se puede evitar el comportamiento asociado al evento.
		* @return	CoreEvent
		*/
		public function CoreEvent( type:String, property:* = null, bubbles:Boolean = false, cancelable:Boolean = false ) {
			
			this._property = property;
			
			super( type, bubbles, cancelable );
			
		}
		
		/**
		 * Propiedades.
		 * @return	*
		 */
		public function get property():* {
			
			return this._property;
			
		}
		
	}
	
}
