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

	import com.emc2zen.data.ICookie;
	import com.emc2zen.data.local.AbstractCookie;
	import com.emc2zen.util.TypeUtil;
	import flash.utils.flash_proxy;
	import flash.utils.Proxy;
	
	use namespace flash_proxy;

	/**
	* Modelo para la implementacion de un objeto compartido local.
	* @author	PollyJex
	* 
	* @example 
	* <listing version="3.0" >
	* 
	* import com.emc2zen.data.iterator.HashMapIterator;
	* import com.emc2zen.data.local.AbstractCookie;
	* import com.emc2zen.data.local.Cookie;
	* 
	* var a:String;
	* var $cc:*;
	* var $s:String = "PEPO";
	* var $c:Cookie = new Cookie( $s );
	* var $v:Function = AbstractCookie.CaptureActivity().getValue;
	* trace( $v( $s ) );
	*	
	* $c.clear();
	* trace( $v( $s ) );
	*	
	* $c.name = "Polly Jex";
	* trace( "ADD NAME 1", $v( $s ) );
	*	
	* trace( $c.name, $c.capture( "name" ) )
	* trace( "CAPTURE NAME 1", $v( $s ) );
	* 	
	* $c["name"] = "Polly Jex";
	* trace( "ADD NAME 2", $v( $s ) );
	*	
	* trace( $c["name"], $c.capture( "name" ) )
	* trace( "CAPTURE NAME 2", $v( $s ) );
	*	
	* $c.update( "name", "Polly Jex" );
	* trace( "ADD NAME 3", $v( $s ) );
	*	
	* trace( $c.name, $c["name"], $c.capture( "name" ) )
	* trace( "CAPTURE NAME 3", $v( $s ) );
	*	
	* $c.update( "realfname", "alejandro" );
	* $c.update( "reallname", "bernardis" );
	* 
	* $c.update( { profesion:"programdor", pcs:4 } );
	*	
	* $cc = $c.capture();
	* for( a in $cc ) trace( ">>>\t",a, $cc[a] );
	* 
	* </listing>
	*/
	public dynamic class Cookie extends Proxy implements ICookie {
		
		/**
		* Referencia del objeto.
		*/
		private var _cookie:AbstractCookie;
		
		
		
		/**
		* Constructor.
		* @param	name	Nombre del objeto.
		* @param	size	Tama&ntilde;o del objeto.
		* @return	Cookie
		*/
		public function Cookie( name:String, size:int = -1 ) {
			
			if( size == -1 ){
				size = AbstractCookie.DEFAULT_SIZE;
			}
			
			_cookie = new AbstractCookie( name, size );
			
		}
		
		
		
		/**
		* Anula la solicitud de eliminación de una propiedad. Cuando se elimina una propiedad con el operador delete, se llama a este método para realizar la eliminación.
		* @param	name	Nombre de la propiedad.
		* @return	Boolean
		*/
		override flash_proxy function deleteProperty( name:* ):Boolean {
			
			return ( ! TypeUtil.isNull( remove( name ) ) ) ? true : false;
			
		}
		
		/**
		* Anula cualquier solicitud del valor de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @return	*
		*/
		override flash_proxy function getProperty( name:* ):* {
			
			return capture( name );
			
		}
		
		/**
		* Anula una llamada para cambiar el valor de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @param	value	Valor de la propiedad.
		* @return	void
		*/
		override flash_proxy function setProperty( name:*, value:* ):void {
			
			update( name, value );
			
		}
		
		
		
		/**
		* Captura los valores de la lista pasada como parametro.
		* @param	rest 	Lista de variables a capturar, si rest es igual a cero retorna todo el contenido 
		* 					y si no existe contenido retorna null.
		* @return	*
		*/
		public function capture( ...rest ):* {
			
			return _cookie.capture.apply( _cookie, rest );
			
		}
		
		/**
		* Remueve todo el contenido del objeto y elimina el objeto del disco.
		* @param	void
		* @return	void
		*/
		public function clear():void {
			
			_cookie.clear();
			
		}
		
		/**
		* Remueve los valores de la lista pasada como parametro y retorna un objeto con los valores respectivos.
		* @param	rest 	Lista de variables a remover, si rest es igual a cero o no existe el contenido retorna false.
		* @return	*
		*/
		public function remove( ...rest ):* {
			
			return _cookie.remove.apply( _cookie, rest );
			
		}
		
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
		public function update( key:*, value:* = null, handler:Function = null ):Boolean {
			
			return _cookie.update( key, value, handler );
			
		}
		
	}
	
}
