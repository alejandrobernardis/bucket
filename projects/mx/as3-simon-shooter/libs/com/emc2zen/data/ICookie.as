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
	* Define la API para la implementacion de una Cookie.
	* @author	PollyJex
	*/
	public interface ICookie {
		
		/**
		* Captura los valores de la lista pasada como parametro.
		* @param	rest 	Lista de variables a capturar, si rest es igual a cero retorna todo el contenido 
		* 					y si no existe contenido retorna null.
		* @return	*
		*/
		function capture( ...rest ):*;
		
		/**
		* Remueve todo el contenido del objeto y elimina el objeto del disco.
		* @param	void
		* @return	void
		*/
		function clear():void;
		
		/**
		* Remueve los valores de la lista pasada como parametro y retorna un objeto con los valores respectivos.
		* @param	rest 	Lista de variables a remover, si rest es igual a cero o no existe el contenido retorna false.
		* @return	*
		*/
		function remove( ...rest ):*;
		
		/**
		* Inserta los valores pasados como parametros en el objeto.
		* @param	key			Nombre de la variable (String). Lista de valores (Object).
		* @param	value		Valor de la variable en caso de que key sea del tipo String.
		* @param	handler		Funcion de respaldo en caso de que la insercion quede en estado de PENDING.
		* 						<p>Cuando se ejecute el evento, el mismo retornara dos valores success:Boolena y 
		* 						event:NetStatusEvent, el primero retorna el estado de la accion y el segundo una 
		* 						referencia al evento ejecutado.</p>
		* @return	Boolean
		*/
		function update( key:*, value:* = null, handler:Function = null ):Boolean;
		
	}
	
}
