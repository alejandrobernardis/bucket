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

	import com.emc2zen.core.CoreObject;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.util.TypeUtil;

	/**
	* Modelo basico de una constante, es util esta clase para la implementacion de constantes publicas y/o staticas.
	* @author	PollyJex
	*/
	public class Constant extends CoreObject {
		
		/**
		* Mapa de las clases que acceden a Constant.
		*/
		private static var $uniqueMap:HashMap = new HashMap();
		
		/**
		* Identificador literal.
		*/
		private var _name:String;
		
		/**
		* Identificador numerico.
		*/
		private var _id:int;	
		
		/**
		* Identificator de tipo.
		*/
		private var _type:String;
		
		
		
		/**
		* Constructor.
		* @param	name	Identificador literal.
		* @param	id		Identificador numerico.
		* @return	Constant
		*/
		public function Constant( name:String, id:int = -1, type:String = "Constant" ) {
			
			if( id < 0 ){
				
				var intTmp:int = 0;
				
				if( $uniqueMap.containsKey( type ) ){	
					intTmp = $uniqueMap.getValue( type );
					intTmp ++;
				}	
				
				id = intTmp;
				$uniqueMap.put( type, intTmp );
				
			}
			
			this._name = name;
			this._id = id;
			this._type = type;
			
		}
		
		/**
		* Retorna el identificador literal de la constante.
		* @param	void
		* @return	String
		*/
		public function get name():String {
			
			return _name;
			
		}
		
		/**
		* Retorna el identificador numerico de la constante.
		* @param	void
		* @return	int
		*/
		public function get id():int {
			
			return _id;
			
		}
		
		/**
		* Retorna el identificador literal del tipo de la constante.
		* @param	void
		* @return	int
		*/
		public function get type():String {
			
			return _type;
			
		}
		
		/**
		* Retorna una cadena con el valor de la clase.
		* @param	void
		* @return	String
		*/
		override public function toString():String {
			
			return _name;
			
		}
		
		/**
		* Retorna una cadena con el valor de la clase.
		* @param	void
		* @return	String
		*/
		public function toFullString():String {
			
			return "[" + _type + " name=\""+ _name + "\" id=\"" + _id  +"\"]";
			
		}
		
	}
	
}
