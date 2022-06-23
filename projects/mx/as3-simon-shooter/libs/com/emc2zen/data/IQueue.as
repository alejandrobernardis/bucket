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
	* Define la API para la implementacion de un modelo basico de Queue.
	* @author	PollyJex
	*/
	public interface IQueue {
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		function clear():void;
		
		/**
		* Verifica si existe el valor en el registro.
		* @param	value 	Valor a verificar.
		* @return	Boolean
		*/
		function contains( value:* ):Boolean;
		
		/**
        * Retorna y remueve el primer elemnto del registro.
		* @param	void
		* @return	Boolean
        */
    	function dequeue():Boolean;
		
		/**
		* Retorna pero no remueve el primer elemento del registro.
		* @param	void
		* @return	*
		*/
		function element():*;
		
		/**
		* Inserta un valor en el registro de ser posible.
		* @param	value	Valor a insertar.
		* @return	Boolean
		*/
		function enqueue( value:* ):Boolean;
		
		/**
		* Verifica si en registro se encuentra vacio.
		* @param	void
		* @return	Boolean
		*/
		function isEmpty():Boolean;
		
		/**
		* Retorna pero no remueve el primer elemento del registro, si el mismo se encuentra vacio retorna null.
		* @param	void
		* @return	*
		*/
		function peek():*;
		
		/**
		* Retorna y remueve el primer elemento del registro, si el mismo se encuentra vacio retorna null.
		* @param	void
		* @return	*
		*/
		function poll():*;
		
		/**
		* Retorna el tama&ntilde; del registro.
		* @param	void
		* @return	int
		*/
		function size():int;
		
		/**
		* Retorna una copia del registro para ser iterado.
		* @param	void
		* @return	Array
		*/
		function toArray():Array;
		
	}
	
}
