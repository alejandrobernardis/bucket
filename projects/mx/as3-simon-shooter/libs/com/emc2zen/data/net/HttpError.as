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
	
	import com.emc2zen.core.Constant;
	import com.emc2zen.util.TypeUtil;
	
	/**
	* Capa de ERROR del protocolo HTTP.
	* <p>
	* 	<span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10' target='_blank'>Status Code Definitions </a> ... 10</span>
	* 		<ol>
	* 			<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1' target='_blank'>Informational 1xx </a> ... 10.1</span>
	* 				<br/><br/>
	* 				<ol>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.1' target='_blank'>100 Continue </a> ... 10.1.1</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.1.2' target='_blank'>101 Switching Protocols </a> ... 10.1.2</span></li>
	* 				</ol>
	* 			</li>
	* 			<br/>
	* 			<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2' target='_blank'>Successful 2xx </a> ... 10.2</span>
	* 				<br/><br/>
	* 				<ol>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.1' target='_blank'>200 OK </a> ... 10.2.1</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.2' target='_blank'>201 Created </a> ... 10.2.2</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.3' target='_blank'>202 Accepted </a> ... 10.2.3</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.4' target='_blank'>203 Non-Authoritative Information </a> ... 10.2.4</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.5' target='_blank'>204 No Content </a> ... 10.2.5</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.6' target='_blank'>205 Reset Content </a> ... 10.2.6</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.2.7' target='_blank'>206 Partial Content </a> ... 10.2.7</span></li>
	* 				</ol>
	* 			</li>
	* 			<br/>
	* 			<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3' target='_blank'>Redirection 3xx </a> ... 10.3</span>
	* 				<br/><br/>
	* 				<ol>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.1' target='_blank'>300 Multiple Choices </a> ... 10.3.1</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.2' target='_blank'>301 Moved Permanently </a> ... 10.3.2</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.3' target='_blank'>302 Found </a> ... 10.3.3</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.4' target='_blank'>303 See Other </a> ... 10.3.4</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.5' target='_blank'>304 Not Modified </a> ... 10.3.5</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.6' target='_blank'>305 Use Proxy </a> ... 10.3.6</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.7' target='_blank'>306 (Unused) </a> ... 10.3.7</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.3.8' target='_blank'>307 Temporary Redirect </a> ... 10.3.8</span></li>
	* 				</ol>
	* 			</li>
	* 			<br/>
	* 			<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4' target='_blank'>Client Error 4xx </a> ... 10.4</span>
	* 				<br/><br/>
	* 				<ol>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.1' target='_blank'>400 Bad Request </a> ... 10.4.1</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.2' target='_blank'>401 Unauthorized </a> ... 10.4.2</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.3' target='_blank'>402 Payment Required </a> ... 10.4.3</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.4' target='_blank'>403 Forbidden </a> ... 10.4.4</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.5' target='_blank'>404 Not Found </a> ... 10.4.5</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.6' target='_blank'>405 Method Not Allowed </a> ... 10.4.6</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.7' target='_blank'>406 Not Acceptable </a> ... 10.4.7</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.8' target='_blank'>407 Proxy Authentication Required </a> ... 10.4.8</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.9' target='_blank'>408 Request Timeout </a> ... 10.4.9</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.10' target='_blank'>409 Conflict </a> ... 10.4.10</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.11' target='_blank'>410 Gone </a> ... 10.4.11</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.12' target='_blank'>411 Length Required </a> ... 10.4.12</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.13' target='_blank'>412 Precondition Failed </a> ... 10.4.13</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.14' target='_blank'>413 Request Entity Too Large </a> ... 10.4.14</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.15' target='_blank'>414 Request-URI Too Long </a> ... 10.4.15</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.16' target='_blank'>415 Unsupported Media Type </a> ... 10.4.16</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.17' target='_blank'>416 Requested Range Not Satisfiable </a> ... 10.4.17</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.4.18' target='_blank'>417 Expectation Failed </a> ... 10.4.18</span></li>
	* 				</ol>
	* 			</li>
	* 			<br/>
	* 			<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5' target='_blank'>Server Error 5xx </a> ... 10.5</span>
	* 				<br/><br/>
	* 				<ol>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.1' target='_blank'>500 Internal Server Error </a> ... 10.5.1</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.2' target='_blank'>501 Not Implemented </a> ... 10.5.2</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.3' target='_blank'>502 Bad Gateway </a> ... 10.5.3</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.4' target='_blank'>503 Service Unavailable </a> ... 10.5.4</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.5' target='_blank'>504 Gateway Timeout </a> ... 10.5.5</span></li>
	* 					<li><span><a href='http://www.w3.org/Protocols/rfc2616/rfc2616-sec10.html#sec10.5.6' target='_blank'>505 HTTP Version Not Supported </a> ... 10.5.6</span></li>
	* 				</ol>
	* 			</li>
	* 		</ol>
	* </p>
	* <br/>
	* <p>See: <a href="http://www.w3.org/Protocols/rfc2616/rfc2616.html" target="_blank">RFC-2616</a></p>
	* <p>Download: <a href="http://www.ietf.org/rfc/rfc2616.txt" target="_blank">RFC-2616</a></p>
	* @author	PollyJex
	*/
	public class HttpError extends Constant {
		
		/**
		* HTTP ERROR 100: Continue.
		*/
		public static const HTTP_ERROR_100:HttpError = new HttpError( "HTTP ERROR 100: Continue.", 100 );
		
		/**
		* HTTP ERROR 101: Switching Protocols.
		*/
		public static const HTTP_ERROR_101:HttpError = new HttpError( "HTTP ERROR 101: Switching Protocols.", 101 );
		
		
		
		/**
		* HTTP ERROR 200: OK.
		*/
		public static const HTTP_ERROR_200:HttpError = new HttpError( "HTTP ERROR 200: OK.", 200 );
		
		/**
		* HTTP ERROR 201: Created.
		*/
		public static const HTTP_ERROR_201:HttpError = new HttpError( "HTTP ERROR 201: Created.", 201 );
		
		/**
		* HTTP ERROR 202: Accepted.
		*/
		public static const HTTP_ERROR_202:HttpError = new HttpError( "HTTP ERROR 202: Accepted.", 202 );
		
		/**
		* HTTP ERROR 203: Non-Authoritative Information.
		*/
		public static const HTTP_ERROR_203:HttpError = new HttpError( "HTTP ERROR 203: Non-Authoritative Information.", 203 );
		
		/**
		* HTTP ERROR 204: No Content.
		*/
		public static const HTTP_ERROR_204:HttpError = new HttpError( "HTTP ERROR 204: No Content.", 204 );
		
		/**
		* HTTP ERROR 205: Reset Content.
		*/
		public static const HTTP_ERROR_205:HttpError = new HttpError( "HTTP ERROR 205: Reset Content.", 205 );
		
		/**
		* HTTP ERROR 206: Partial Content.
		*/
		public static const HTTP_ERROR_206:HttpError = new HttpError( "HTTP ERROR 206: Partial Content.", 206 );
		
		
		
		/**
		* HTTP ERROR 100: Continue
		*/
		public static const HTTP_ERROR_300:HttpError = new HttpError( "HTTP ERROR 300: Multiple Choices.", 300 );
		
		/**
		* HTTP ERROR 300: Multiple Choices.
		*/
		public static const HTTP_ERROR_301:HttpError = new HttpError( "HTTP ERROR 301: Moved Permanently.", 301 );
		
		/**
		* HTTP ERROR 302: Found.
		*/
		public static const HTTP_ERROR_302:HttpError = new HttpError( "HTTP ERROR 302: Found.", 302 );
		
		/**
		* HTTP ERROR 303: See Other.
		*/
		public static const HTTP_ERROR_303:HttpError = new HttpError( "HTTP ERROR 303: See Other.", 303 );
		
		/**
		* HTTP ERROR 304: Not Modified.
		*/
		public static const HTTP_ERROR_304:HttpError = new HttpError( "HTTP ERROR 304: Not Modified.", 304 );
		
		/**
		* HTTP ERROR 305: Use Proxy.
		*/
		public static const HTTP_ERROR_305:HttpError = new HttpError( "HTTP ERROR 305: Use Proxy.", 305 );
		
		/**
		* HTTP ERROR 307: Temporary Redirect.
		*/
		public static const HTTP_ERROR_307:HttpError = new HttpError( "HTTP ERROR 307: Temporary Redirect.", 307 );
		
		
		
		/**
		* HTTP ERROR 400: Bad Request. 
		*/
		public static const HTTP_ERROR_400:HttpError = new HttpError( "HTTP ERROR 400: Bad Request.", 400 );
		
		/**
		* HTTP ERROR 401: Unauthorized.
		*/
		public static const HTTP_ERROR_401:HttpError = new HttpError( "HTTP ERROR 401: Unauthorized.", 401 );
		
		/**
		* HTTP ERROR 402: Payment Required.
		*/
		public static const HTTP_ERROR_402:HttpError = new HttpError( "HTTP ERROR 402: Payment Required.", 402 ); 
		
		/**
		* HTTP ERROR 403: Forbidden.
		*/
		public static const HTTP_ERROR_403:HttpError = new HttpError( "HTTP ERROR 403: Forbidden.", 403 ); 
		
		/**
		* HTTP ERROR 404: Not Found.
		*/
		public static const HTTP_ERROR_404:HttpError = new HttpError( "HTTP ERROR 404: Not Found.", 404 ); 
		
		/**
		* HTTP ERROR 405: Method Not Allowed.
		*/
		public static const HTTP_ERROR_405:HttpError = new HttpError( "HTTP ERROR 405: Method Not Allowed.", 405 ); 
		
		/**
		* HTTP ERROR 406: Not Acceptable.
		*/
		public static const HTTP_ERROR_406:HttpError = new HttpError( "HTTP ERROR 406: Not Acceptable.", 406 ); 
		
		/**
		* HTTP ERROR 407: Proxy Authentication Required.
		*/
		public static const HTTP_ERROR_407:HttpError = new HttpError( "HTTP ERROR 407: Proxy Authentication Required.", 407 ); 
		
		/**
		* HTTP ERROR 408: Request Time-out.
		*/
		public static const HTTP_ERROR_408:HttpError = new HttpError( "HTTP ERROR 408: Request Time-out.", 408 ); 
		
		/**
		* HTTP ERROR 409: Conflict.
		*/
		public static const HTTP_ERROR_409:HttpError = new HttpError( "HTTP ERROR 409: Conflict.", 409 ); 
		
		/**
		* HTTP ERROR 410: Gone.
		*/
		public static const HTTP_ERROR_410:HttpError = new HttpError( "HTTP ERROR 410: Gone.", 410 ); 
		
		/**
		* HTTP ERROR 411: Length Required.
		*/
		public static const HTTP_ERROR_411:HttpError = new HttpError( "HTTP ERROR 411: Length Required.", 411 ); 
		
		/**
		* HTTP ERROR 412: Precondition Failed.
		*/
		public static const HTTP_ERROR_412:HttpError = new HttpError( "HTTP ERROR 412: Precondition Failed.", 412 ); 
		
		/**
		* HTTP ERROR 413: Request Entity Too Large.
		*/
		public static const HTTP_ERROR_413:HttpError = new HttpError( "HTTP ERROR 413: Request Entity Too Large.", 413 ); 
		
		/**
		* HTTP ERROR 414: Request-URI Too Large.
		*/
		public static const HTTP_ERROR_414:HttpError = new HttpError( "HTTP ERROR 414: Request-URI Too Large.", 414 ); 
		
		/**
		* HTTP ERROR 415: Unsupported Media Type.
		*/
		public static const HTTP_ERROR_415:HttpError = new HttpError( "HTTP ERROR 415: Unsupported Media Type.", 415 ); 
		
		/**
		* HTTP ERROR 416: Requested range not satisfiable.
		*/
		public static const HTTP_ERROR_416:HttpError = new HttpError( "HTTP ERROR 416: Requested range not satisfiable.", 416 ); 
		
		/**
		* HTTP ERROR 417: Expectation Failed.
		*/
		public static const HTTP_ERROR_417:HttpError = new HttpError( "HTTP ERROR 417: Expectation Failed.", 417 ); 
		
		
		
		/**
		* HTTP ERROR 500: Internal Server Error.
		*/
		public static const HTTP_ERROR_500:HttpError = new HttpError( "HTTP ERROR 500: Internal Server Error.", 500 ); 
		
		/**
		* HTTP ERROR 501: Not Implemented.
		*/
		public static const HTTP_ERROR_501:HttpError = new HttpError( "HTTP ERROR 501: Not Implemented.", 501 ); 
		
		/**
		* "HTTP ERROR 502: Bad Gateway.
		*/
		public static const HTTP_ERROR_502:HttpError = new HttpError( "HTTP ERROR 502: Bad Gateway.", 502 ); 
		
		/**
		* HTTP ERROR 503: Service Unavailable.
		*/
		public static const HTTP_ERROR_503:HttpError = new HttpError( "HTTP ERROR 503: Service Unavailable.", 503 ); 
		
		/**
		* HTTP ERROR 504: Gateway Time-out.
		*/
		public static const HTTP_ERROR_504:HttpError = new HttpError( "HTTP ERROR 504: Gateway Time-out.", 504 ); 
		
		/**
		* HTTP ERROR 505: HTTP Version not supported.
		*/
		public static const HTTP_ERROR_505:HttpError = new HttpError( "HTTP ERROR 505: HTTP Version not supported.", 505 ); 
		
		
		
		/**
		* Resuelve el DETALLE del ERROR HTTP por el numero de ID.
		* @param	value	Identificador numerico.
		* @return	String
		*/
		public static function resolveErrorHttpAsName( value:int ):String {
			
			var strTmp:String = HttpError[ "HTTP_ERROR_" + value ].name;
			
			if ( ! TypeUtil.isUndefined( strTmp ) ) {
				return strTmp;
			}else {
				return null;
				//throw new Error( value + " is not a valid code within the data layer." );
			}
			
		}
		
		
		/**
		* Constructor
		* @param	name		Identificador literal.
		* @param	id			Identificador numerico.
		* @return	HttpError
		*/
		public function HttpError( name:String, id:int ) {
			
			super( name, id, "HttpError" );
			
		}		
		
	}
	
}
