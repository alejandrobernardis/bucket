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

package com.emc2zen.data.net {
	
	/**
	* @import
	*/
	
	import com.emc2zen.data.iterator.HashMapIterator;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.data.type.Uri;	
	
	/**
	* Resuelve una URI retornando los valores de la misma de manera discriminada.
	* @author	PollyJex
	*/
	public class ResolveURI extends Uri {
		
		
		private var $baseUri:String;
		
		
		/**
		* Constructor.
		* @param	void
		* @return	ResolveURI
		*/
		public function ResolveURI( uri:String ) {
			
			super();
			this.$baseUri = uri;
			
		}
		
		
		/**
		 * Resuelve la uri para fragmentarla.
		 * 
		 * MODELO DE URI: 
		 * 	http://username:password@www.domain.com:8080/path/to/filename.ext;param1=value1&param2=value2?query1=value1&query2=value2#fragment
		 * 
		 * 		- scheme: http:
		 * 	
		 * 		- authority //username:password@www.domain.com:8080
		 * 			userdata: username:password@
		 * 			hostname: www.domain.com
		 * 			port: 8080
		 * 	
		 * 		- path: /path/to/
		 * 
		 * 		- fileName: filename
		 * 	
		 * 		- fileExtension: .ext
		 * 
		 * 		- parameters: ;param1=value1&param2=value2
		 * 
		 * 		- query: ?query1=value1&query2=value2#fragment
		 * 			query: query1=value1&query2=value2
		 * 			fragment: fragment
		 * 
		 * 
		 * ver norma : 
		 * 
		 * 
		 * @param	void
		 * @return	void
		 */ 
		private function Resolve():void {
			var _uriTmp:String = this.$baseUri;
			// 1PARTE: http://username:password@www.domain.com:8080/path/to/filename.ext;param1=value1&param2=value2		
			// 2PARTE: query1=value1&query2=value2#fragment
		}
		
	}
	
}
