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

package com.emc2zen.data.local {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.data.local.AbstractCookie;
	import com.emc2zen.util.TypeUtil;
	
	/**
	* Modelo para la implementacion de un objeto compartido local modo estatico.
	* @author	PollyJex
	* @example 
	* <listing version="3.0" >
	* 
	* import com.emc2zen.data.local.AbstractCookie;
	* import com.emc2zen.data.local.LocalCookie;
	* 
	* var $c:String = "PEPO";
	* 
	* LocalCookie.create( $c );
	* 
	* var $v:Function = AbstractCookie.CaptureActivity().getValue;
	* 
	* LocalCookie.update( $c, "nombre", "polly" );
	* LocalCookie.update( $c, "apellido", "jex" );
	* 
	* trace( $v( $c ) );
	* trace( LocalCookie.capture( $c, "nombre" ) );
	* trace( $v( $c ) );	
	* 
	* </listing>
	*/
	public dynamic class LocalCookie extends CoreStatic {
		
		/**
		* Resuelve la conexion con el objeto global.
		* @param	name	Nombre del objeto.
		* @param	size	Tama&ntilde;o del objeto.	
		* @return	AbstractCookie
		*/
		public static function create( name:String, size:int = -1 ):AbstractCookie {
			
			if( size < 0 ){
				size = AbstractCookie.DEFAULT_SIZE;
			}
			
			return new AbstractCookie( name, size );
			
		}
		
		
		
		/**
		* Captura los valores de la lista pasada como parametro.
		* @param	name	Nombre del objeto.
		* @param	rest 	Lista de variables a capturar, si rest es igual a cero retorna todo el contenido 
		* 					y si no existe contenido retorna null.
		* @return	*
		*/
		public static function capture( name:String, ...rest ):* {
			
			var $c:AbstractCookie = create( name );
			return $c.capture.apply( $c, rest );
			
		}
		
		/**
		* Remueve todo el contenido del objeto y elimina el objeto del disco.
		* @param	name	Nombre del objeto.
		* @return	void
		*/
		public static function clear( name:String ):void {
			
			create( name ).clear();
			
		}
		
		/**
		* Remueve los valores de la lista pasada como parametro y retorna un objeto con los valores respectivos.
		* @param	name	Nombre del objeto.
		* @param	rest 	Lista de variables a remover, si rest es igual a cero o no existe el contenido retorna false.
		* @return	*
		*/
		public static function remove( name:String, ...rest ):* {
			
			var $c:AbstractCookie = create( name );
			return $c.remove.apply( $c, rest );
			
		}
		
		/**
		* Inserta los valores pasados como parametros en el objeto.
		* @param	name		Nombre del objeto.
		* @param	key			Nombre de la variable (String). Lista de valores (Object).
		* @param	value		Valor de la variable en caso de que key sea del tipo String.
		* @param	handler		Funcion de respaldo en caso de que la insercion quede en estado de PENDING.
		* 						<p>Cuando se ejecute el evento, el mismo retornara dos valores success:Boolena y 
		* 						event:NetStatusEvent, el primero retorna el estado de la accion y el segundo una 
		* 						referencia al evento ejecutado.</p>
		* @return	Boolean
		*/
		public static function update( name:String, key:*, value:* = null, handler:Function = null ):Boolean {
			
			return create( name ).update( key, value, handler );
			
		}
		
	}
	
}
