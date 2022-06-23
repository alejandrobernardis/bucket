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

	import com.emc2zen.data.stack.Stack;
	import com.emc2zen.data.type.AbstractType;

	/**
	* Modelo basico de una estrucutra de dato del tipo Stack discriminada por tipos.
	* @author	PollyJex
	*/
	public class TypedStack extends Stack {
		
		/**
		* Tipo de datos.
		*/
		private var _type:AbstractType;
		
		
		
		/**
		* Constructor.
		* @param	type		Tipo de dato.
		* @param	capacity 	Tama&ntilde;o del Stack.
		* @return	TypedStack
		*/
		public function TypedStack( type:*, capacity:int = 0 ) {
			
			this._type = new AbstractType( type );
			super( capacity );
			
		}
		
		
		
		/**
		* Verifica si existe value en el registro.
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
		* Agrega un elemento al inicio del registro y retorna el nuevo tama&ntilde;o del registro.
		* @param	value	Objeto a insertar.
		* @return	void
		*/
		public override function push( value:* ):void {
			
			if( _type.isSupported( value ) ){
				
				super.push( value );
				
			}	
			
		}
		
		/**
		* Busca y retorna el valor de value en el registro, en caso de no existir retorna null.
		* @param	value 	Objeto a buscar.
		* @return	*
		*/
		public override function search( value:* ):* {
			
			if( _type.isSupported( value ) ){
				
				return super.search( value );
				
			}
			
			return null;
			
		}	
		
		/**
		* Retorna el tipo implementado.
		* @param	void
		* @return	*
		*/
		public function type():* {
			
			return _type.type;
			
		}
		
	}
	
}
