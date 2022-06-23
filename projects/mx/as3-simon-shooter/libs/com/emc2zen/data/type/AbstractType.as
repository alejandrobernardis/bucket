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
	import com.emc2zen.data.IType;
	import com.emc2zen.util.TypeUtil;

	/**
	* Modelo basico de referencia a tipos.
	* @author	PollyJex
	*/
	public class AbstractType extends CoreObject implements IType {
		
		/**
		* Referencia del tipo.
		*/
		private var _type:*;
		
		
		/**
		* Constructor.
		* @param	value	Tipo.
		* @return	AbstractType
		*/
		public function AbstractType( value:* ) {
			
			if( TypeUtil.isNull( value ) || TypeUtil.isUndefined( value ) ){
				throw new Error( "Argument must not be NULL or UNDEFINED." );
			}
			
			_type = value;
			
		}
		
		
		
		/**
		* Referencia del tipo. Lectura/Escritura.
		*/
		public function get type():* {
			return _type;
		}
		
		public function set type( value:* ):void {
			_type = value;
		}
		
		
		/**
		* Verifica si value es soportada por el tipo.
		* @param	value	Valor a comprobar.
		* @return	Boolean
		*/
		public function isSupported( value:* ):Boolean {
			
			return TypeUtil.thisIs( value, _type );
			
		}
		
	}
	
}
