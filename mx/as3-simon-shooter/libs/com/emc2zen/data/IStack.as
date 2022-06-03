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
	* Define la API para la implementacion de un modelo basico de Stack.
	* @author	PollyJex
	*/
	public interface IStack {
		
		/**
		* Retorna la capacidad del registro.
		* @param	void
		* @return	int
		*/
		function capacity():int;
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
		function clear():void;
		
		/**
		* Verifica si existe value en el registro.
		* @param	value 	Valor a verificar.
		* @return	Boolean
		*/
		function contains( value:* ):Boolean;
		
		/**
		* Verifica si en registro se encuentra vacio.
		* @param	void
		* @return	Boolean
		*/
		function isEmpty():Boolean;
		
		/**
		* Retorna el valor del siguiente elemento del registro, pero no altera el puntero de lectura.
		* @param	void
		* @return	*
		*/
		function peek():*;
		
		/**
		* Elimina el ultimo elemento del registro y retorna su valor. 
		* @param	void
		* @return	*
		*/
		function pop():*;
		
		/**
		* Agrega un elemento al inicio del registro y retorna el nuevo tama&ntilde;o del registro.
		* @param	value	Objeto a insertar.
		* @return	void
		*/
		function push( value:* ):void;
		
		/**
		* Busca y retorna el valor de value en el registro, en caso de no existir retorna null.
		* @param	value 	Objeto a buscar.
		* @return	*
		*/
		function search( value:* ):*;
		
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
		
		/**
		* Retorna el valor del primer elemento del registro.
		* @param	void
		* @return	*
		*/
		function top():*;
		
	}
	
}
