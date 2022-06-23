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

package com.emc2zen.data {

	/**
	* @import
	*/



	/**
	* Define la API para la implementacion de un modelo basico de Map.
	* @author	PollyJex
	*/
	public interface IMap {
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		function clear():void;
		
		/**
		* Verifica si el registro posee la clave.
		* @param	key		Clave.
		* @return	Boolean
		*/
		function containsKey( key:String ):Boolean;
		
		/**
		* Verifica si el registro posee el valor.
		* @param	value	Valor.
		* @return	Boolean
		*/
        function containsValue( value:* ):Boolean;
		
		/**
		* Retorna la clave asociada al valor.
		* @param	value	Valor.
		* @return	String
		*/
		function getKey( value:* ):String;
		
		/**
		* Retorna el valor asociado a la clave.
		* @param	key		String
		* @return	*
		*/
        function getValue( key:String ):*;
		
		/**
		* Verifica si en registro se encuentra vacio.
		* @param	void
		* @return	Boolean
		*/
		function isEmpty():Boolean;
		
		/**
		* Inserta clave->valor en el regitro.
		* @param	key		Clave.
		* @param	value	Valor.
		* @return	void
		*/
		function put( key:String, value:* ):void;
		
		/**
		* Remueve una clave y su valor asociado del registro.
		* @param	key		Clave.
		* @return	void
		*/
        function remove( key:String ):void;
		
		/**
		* Retorna el tama&ntilde;o del registro.
		* @param	void
		* @return	int
		*/
        function size():int;          
		
	}
	
}
