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

package com.emc2zen.util {	

	/**
	* @import
	*/
	
	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.util.StringUtil;
	import com.emc2zen.util.TypeUtil;
	import flash.display.LoaderInfo;
	import flash.external.ExternalInterface;
	
	/**
	* Utilidades para el formateo de URI's.
	* @author	PollyJex
	*/
	public class URIUtil extends CoreStatic {	
		
		/**
		* Retona la URI del documento.
		* @return	String
		*/
		public static function get url():String {
			return LoaderInfo.getLoaderInfoByDefinition( URIUtil ).url;
		}
		
		/**
		* Retona la URI del documento utilizando de interprete JavaScript.
		* @return	String
		*/
		public static function get urlForJS():String {
			return ExternalInterface.call( "window.location.href.toString" );
		}
		
		
		
		/**
		* Modifica una URI para que no sea cacheada por el servidor (truco).
		* @param	uri		Uri a modificar.
		* @return	String
		*/
		public static function AntiCache( uri:String = null ):String {					
			
			// TODO: Modificar esto por un modelo GUID
			var cache:String = new String( "AntiCache=" + ( Math.ceil( Math.random() * 999999 ) ) );			
			
			if( TypeUtil.isNull( uri ) ){
				return new String( "?" + cache );
			}
			
			var separator:String = new String();
			
			if ( uri.indexOf ( "?" ) != -1 ) { 
				separator = "&"; 
			} else { 
				separator = "?"; 
			}
			
			return new String( uri + separator + cache );
			
		}
		
		
		
		/**
		 * Verifica si el esquema de la uri es "file:"
		 * @param	uri		Uri a verificar.
		 * @return	Boolean
		 */
		public static function isFile( uri:String ):Boolean {
			return ( getScheme( uri ) == "file" ) ? true : false;
		}
		
		/**
		 * Verifica si el esquema de la uri es "http:"
		 * @param	uri		Uri a verificar.
		 * @return	Boolean
		 */
		public static function isHttp( uri:String ):Boolean {
			return ( getScheme( uri ) == "http" ) ? true : false;
		}
		
		/**
		 * Verifica si el esquema de la uri es "https:"
		 * @param	uri		Uri a verificar.
		 * @return	Boolean
		 */
		public static function isHttps( uri:String ):Boolean {
			return ( getScheme( uri ) == "https" ) ? true : false;
		}	
		
		/**
		 * Verifica si el esquema de la uri y retorna una cadena con el valor.
		 * @param	uri		Uri a verificar.
		 * @return	Boolean
		 */
		private static function getScheme( uri:String ):String {
			
			var end:int = uri.search( ":" );
			
			if( end == -1 ){
				return null;
			}
			
			return new String( uri.substr( 0, end ) ).toLowerCase();
			
		}
		
		
		
		/**
		* Realiza una limpieza de la uri pasada como argumento y retorna un objeto con los 
		* valores de manera discriminada.
		* 
		* TODO: Implementar un modelo con un Objeto que defina las peopiedades de la URI. 
		* TODO: Soporte para URI relativa y sin esquema.
		* 
		* @param	uri		Valor de la URI.
		* @param	forJS	Busca el valor a traves de JavaScript.
		* @return	Object
		*/
		public static function ResolveURI( uri:String = null, forJS:Boolean = false ):Object {
			
			var uriTmp:Array = new Array();
			var parTmp:Array = new Array();
			var objTmp:Object = new Object();				
			var strTmp:String = new String();
			var arrTmp:Array = new Array();
			var verify:int = new int();
			var a:int = new int();
			
			
			
			if( TypeUtil.isNull( uri ) ){
				
				if( ! forJS ){
					uri = URIUtil.url;
				}else{
					uri = URIUtil.urlForJS;
				}
				
			}else if( isFile( uri ) ){
				
				return null;
				
			}
			
			
			
			uriTmp = StringUtil.trim( uri ).split( "?" );
			
			// Base
			objTmp.uriBase = uri;
			strTmp = new String( uriTmp[ 0 ] );
			
			
			// Schema
			objTmp.schema = new String();
			
			verify = strTmp.search( "([A-Za-z0-9]+)\:\/\/" );
			
			if( verify != -1 ){	
				
				objTmp.schema = new String( strTmp.substr( 0, strTmp.search( ":" ) ) ).toLowerCase();
				strTmp = StringUtil.remove( strTmp, "([A-Za-z0-9]+)\:\/\/" );
				
			}
			
			
			// Userdata
			objTmp.username = new String();
			objTmp.password = new String();			
			
			verify = strTmp.search( "([a-zA-Z0-9]+)\:([a-zA-Z0-9]+)\@" );
			
			if( verify != -1 ){				
				
				
				arrTmp = String( strTmp.substr( 0, strTmp.search( "@" ) ) ).split( ":" );
				
				objTmp.username = arrTmp[ 0 ];
				objTmp.password = arrTmp[ 1 ];
				
				strTmp = StringUtil.remove( strTmp, "([a-zA-Z0-9]+)\:([a-zA-Z0-9]+)\@" );
				
			}
			
			
			// Hostname & Port
			objTmp.hostname = new String();
			objTmp.port = new String();
			
			arrTmp = strTmp.split( "/" );
			strTmp = arrTmp[ 0 ];
			verify = strTmp.search( ":" );
			
			if( verify != -1 ){				
				
				objTmp.hostname = strTmp.substr( 0, verify );
				objTmp.port = strTmp.substr( verify + 1 );
				
			}else{
				
				objTmp.hostname = strTmp;
				
			}
			
			arrTmp.shift();
			strTmp = arrTmp.pop();
			
			
			// Authority
			objTmp.authority = new String();
			
			if( ! TypeUtil.isEmpty( objTmp.username ) && ! TypeUtil.isEmpty( objTmp.password ) ){
				objTmp.authority += objTmp.username + ":" + objTmp.password + "@";
			}
			
			if( ! TypeUtil.isEmpty( objTmp.hostname ) ){
				objTmp.authority += objTmp.hostname;
			}
			
			if( ! TypeUtil.isEmpty( objTmp.port ) ){
				objTmp.authority += ":" + objTmp.port;
			}
			
			
			// Path
			objTmp.path = new String( arrTmp.join( "/" ) + "/" );
			
			
			// FileName, FileExtension & Parameters
			objTmp.fileName = new String();
			objTmp.fileExtension = new String();
			objTmp.parameters = new HashMap();
			
			verify = strTmp.search( ";" );
			
			if( verify != -1 ){	
				
				arrTmp = String( strTmp.split( ";" )[ 1 ] ).split( "&" );
				
				for( a = 0; a < arrTmp.length; a++ ){	
					
					parTmp = arrTmp[ a ].split( "=" );
					objTmp.parameters.put( parTmp[ 0 ], parTmp[ 1 ] );	
					
				}
				
				strTmp = strTmp.substr( 0, verify );
				
			}
			
			arrTmp = strTmp.split( "." );
			objTmp.fileName = arrTmp[ 0 ];
			objTmp.fileExtension = arrTmp[ 1 ];
			
			
			// Query & Fragment
			objTmp.query = new HashMap();
			objTmp.fragment = new String();
			
			strTmp = new String( uriTmp[ 1 ] );
			
			if( ! TypeUtil.isEmpty( strTmp ) ) {
				
				// Fragment
				verify = strTmp.search( "#" );
				
				if( verify != -1 ){
					objTmp.fragment = strTmp.substr( verify + 1 );
					strTmp = strTmp.substr( 0, verify );
				}
				
				// Query
				arrTmp = strTmp.split( "&" );
				
				for( a = 0; a < arrTmp.length; a++ ){
					
					parTmp = arrTmp[ a ].split( "=" );
					objTmp.query.put( parTmp[ 0 ], parTmp[ 1 ] );
					
				}
				
			}
			
			return objTmp;
			
		}		
		
	}
	
}
