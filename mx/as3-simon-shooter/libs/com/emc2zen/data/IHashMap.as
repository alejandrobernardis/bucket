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

	import com.emc2zen.data.IMap;

	/**
	* Define la API para la implementacion de un modelo basico de tipo HashMap.
	* @author	PollyJex
	*/
	public interface IHashMap extends IMap {
		
		/**
		* Reinicia el registro ecepto las claves pasadas como parametros
		* @param	rest	Lita de claves.
		* @return	void
		*/
        function clearAllExcept( ...rest ):void;
		
		/**
		* Retorna una lista con las claves existentes en el registro.
		* @param	voir
		* @return	Array
		*/
		function getKeys():Array;
		
		/**
		* Retorna una lista con los valores existentes en el registro.
		* @param	void
		* @return	Array
		*/
        function getValues():Array;
		
		/**
		* Inserta una lista de clave->valor en el regitro.
		* @param	key		Lista de claves, Object o HashMap
		* @param	value	Lista de valores.
		* @return	void
		*/
		function putAll( key:*, value:* = null ):void;
		
		/**
		* Reseta todas las claves del resgitro revalorizandolas con "".
		* @param	void
		* @return	void
		*/
		function reset():void;
		
		/**
		* Reseta todas las claves del resgitro revalorizandolas con "", ecepto las pasadas como parametro.
		* @param	rest	Lista de las claves.
		* @return	void
		*/
        function resetAllExcept( ...rest ):void;
		
	}
	
}
