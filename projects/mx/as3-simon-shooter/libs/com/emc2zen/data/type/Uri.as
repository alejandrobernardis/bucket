/**
* @protected
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
	
	import com.emc2zen.data.map.HashMap;
	
	/**
	* Modelo basico de una URI, solo lectura.
	* @author	PollyJex
	*/
	public class Uri {
		
		/**
		 * Nombre que se refiere a una especificación para asignar los identificadores, 
		 * e.g. urn:, tag:, cid:. En algunos casos también identifica el protocolo de 
		 * acceso al recurso, por ejemplo http:, mailto:, ftp:.
		 */
		protected var _scheme:String;
		
		/**
		 * Elemento jerárquico que identifica la autoridad de nombres e.g. 
		 * //www.dns.com.ar, //dns.com //user:pass@www.dns.com.ar
		 */
		protected var _authority:String;
		
		/**
		 * Elemento que identifica el nombre de usuario que es enviado e.g.
		 * http://USERNAME:password@www.dns.com.ar
		 */
		protected var _username:String;
		
		/**
		 * Elemento que identifica la contraseña que es eviada e.g.
		 * http://username:PASSWORD@www.dns.com.ar
		 */
		protected var _password:String;
		
		/**
		 * Elemento que identifica el nombre de dominio e.g. www.dsn.com,
		 * 127.0.0.1, www.dns.com.ar.
		 */
		protected var _hostname:String;
		
		/**
		 * Elemento que identifica el nombre del dominio de nivel superior que posee la 
		 * uri e.g. .com.ar, .com, .org, .net.
		 */
		protected var _tld:String;
		
		/**
		 * Especifica un número de puerto TCP. Usualmente es omitido (en este caso, 
		 * su valor por omisión es 80) y probablemente, para el usuario es lo que 
		 * tiene menor relevancia en todo el URI.
		 */
		protected var _port:String;
		
		/**
		 * Información usualmente organizada en forma jerárquica, que identifica al 
		 * recurso en el ámbito del esquema URI y la autoridad de nombres 
		 * e.g. /dir_1/dir_2/dir_3
		 */
		protected var _path:String;
		
		/**
		 * Elemento que identifica el nombre de archivo que se esta utilizando e.g.
		 * http://www.dns.com.ar/filename.ext
		 */
		protected var _fileName:String;
		
		/**
		 * Elemento que identifica el nombre de la extension del archivo que se esta 
		 * utilizando e.g. http://www.dns.com.ar/filename.ext
		 */
		protected var _fileExtension:String;
		
		/**
		 * Lista de parametros enviados a traves de la URI e.g.
		 * http://www.dns.com.ar/filename.ext;key=value
		 */
		protected var _parameters:HashMap;
		
		/**
		 * Información con estructura no jerárquica (usualmente pares "clave=valor") 
		 * que identifica al recurso en el ámbito del esquema URI y la autoridad de 
		 * nombres. El comienzo de este componente se indica mediante el carácter '?'.
		 */
		protected var _query:HashMap;
		
		/**
		 * Permite identificar una parte del recurso principal, o vista de una 
		 * representación del mismo. El comienzo de este componente se indica 
		 * mediante el carácter '#'.
		 */
		protected var _fragment:String;	
		
		/**
		 * Identifica las URI que no poseen jerarquia e.g.
		 * mailto:username@hostname.com.ar
		 */
		protected var _nonHierarchical:String;
		
		
		
		/**
		* Constructor.
		* @param	void
		* @return	URI
		*/
		public function Uri() {
			reset();
		}
		
		
		/**
		 * Resetea las propiedades del objeto.
		 * @param	void
		 * @return	void
		 */
		protected function reset():void {
			
			this._scheme = new String();
			this._authority = new String();
			this._username = new String();
			this._password = new String();
			this._hostname = new String();
			this._tld = new String();
			this._port = new String();
			this._path = new String();
			this._fileName = new String();
			this._fileExtension = new String();
			this._parameters = new HashMap();
			this._query = new HashMap();
			this._fragment = new String();	
			this._nonHierarchical = new String();
			
		}
		
		
		
		/**
		 * Esquema
		 */
		public function get scheme():String { 
			return _scheme; 
		}
		
		/** 
		 * Autoridad
		 */
		public function get authority():String { 
			return _authority; 
		}
		
		/**
		 * Nombre de usuario
		 */
		public function get username():String { 
			return _username; 
		}
		
		/**
		 * Contraseña de usuario
		 */
		public function get password():String { 
			return _password; 
		}
		
		/**
		 * Nombre del host
		 */
		public function get hostname():String { 
			return _hostname; 
		}
		
		/**
		 * Nombre del dominio de nivel superior
		 */
		public function get tld():String { 
			return _tld; 
		}
		
		/**
		 * Puerto
		 */
		public function get port():String { 
			return _port; 
		}
		
		/**
		 * Ruta
		 */
		public function get path():String { 
			return _path; 
		}
		
		/**
		 * Nombre del archivo
		 */
		public function get fileName():String { 
			return _fileName; 
		}
		
		/**
		 * Extension del archivo
		 */
		public function get fileExtension():String { 
			return _fileExtension; 
		}
		
		/**
		 * Parametros
		 */
		public function get parameters():HashMap { 
			return _parameters; 
		}
		
		/**
		 * Consulta
		 */
		public function get query():HashMap { 
			return _query; 
		}
		
		/**
		 * Fragmento
		 */
		public function get fragment():String { 
			return _fragment; 
		}
		
		/**
		 * Sin jerarquia.
		 */
		public function get nonHierarchical():String { 
			return _nonHierarchical; 
		}
		
		
	}
	
}
