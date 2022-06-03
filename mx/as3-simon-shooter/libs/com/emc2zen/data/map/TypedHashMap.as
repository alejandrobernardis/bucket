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

	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.data.type.AbstractType;
	import com.emc2zen.util.TypeUtil;

	/**
	* Modelo basico de una estrucutra de dato del tipo HashMap discriminado por tipos.
	* @author	PollyJex
	*/
	public class TypedHashMap extends HashMap {
		
		/**
		* Tipo de datos.
		*/
		private var _type:AbstractType;
		
		
		
		/**
		* Constructor.
		* @param	type		Valor del tipo de dato.
		* @param	weakKeys	Uso de referencias debiles.
		* @return	TypedHashMap
		*/
		public function TypedHashMap( type:*, weakKeys:Boolean = false ) {
			
			this._type = new AbstractType( type );
			super( weakKeys );
			
		}
		
		
		
		/**
		* Verifica si el registro posee el valor.
		* @param	value	Valor.
		* @return	Boolean
		*/
        public override function containsValue( value:* ):Boolean {
			
			if( _type.isSupported( value ) ){
				return super.containsValue( value );
			}
			
			return false;
			
		}
		
		/**
		* Inserta clave->valor en el regitro.
		* @param	key		Clave.
		* @param	value	Valor.
		* @return	void
		*/
		public override function put( key:String, value:* ):void {
			
			ResolvePutForType( key, value );
			
		}
		
		/**
		* Inserta una lista de clave->valor en el regitro.
		* @param	key		Lista de claves, Object o HashMap
		* @param	value	Lista de valores.
		* @return	void
		*/
		public override function putAll( key:*, value:* = null ):void {
			
			ResolvePutAll( key, value, _type );
			
		}
		
	}
	
}
