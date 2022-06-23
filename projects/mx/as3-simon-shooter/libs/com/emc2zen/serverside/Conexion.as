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

package com.emc2zen.serverside {	

	/**
	 * @import
	 */
	
	import com.emc2zen.util.TypeUtil;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.HTTPStatusEvent;
	import flash.events.IEventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLLoader;
	import flash.net.URLRequest;
	import flash.net.URLVariables;
	import flash.utils.flash_proxy;
	import flash.utils.Proxy;
	
	/* ### EVENTS ### */
	
	/**
	 * Se distribuye tras decodificar y colocar todos los datos 
	 * recibidos en la propiedad data del objeto URLLoader. Es 
	 * posible acceder a los datos recibidos una vez distribuido 
	 * este evento.
	 * 
	 * @eventType com.emc2zen.serverside.ConexionEvent.COMPLETE
	 */
	[Event( name="complete", type="com.emc2zen.serverside.ConexionEvent" )]
	
	/**
	 * Se distribuye cuando se inicia la operación de descarga 
	 * tras una llamada al método URLLoader.load().
	 * 
	 * @eventType flash.event.Event.OPEN
	 */
	[Event( name="open", type="flash.events.Event" )]
	
	/**
	 * Se distribuye al recibirse datos mientras progresa una 
	 * operación de descarga.
	 * 
	 * @eventType flash.event.ProgressEvent.PROGRESS
	 */
	[Event( name="progress", type="flash.events.ProgressEvent" )]
	
	/**
	 * Se distribuye si una llamada a URLLoader.load() intenta 
	 * acceder a datos sobre HTTP y si el entorno de Flash Player 
	 * actual puede detectar y devolver el código de estado para 
	 * la solicitud. (Es posible que algunos entornos de navegador 
	 * no proporcionen esta información.) Tenga en cuenta que se 
	 * enviará el evento httpStatus (si existe) antes que (y además 
	 * de) cualquier evento complete o error.
	 * 
	 * @eventType flash.event.HTTPStatusEvent.HTTP_STATUS
	 */
	[Event( name="httpStatus", type="flash.events.HTTPStatusEvent" )]
	
	/**
	 * Se distribuye si el resultado de una llamada a URLLoader.load() 
	 * es un error grave que hace que la descarga finalice.
	 * 
	 * @eventType flash.event.IOErrorEvent.IO_ERROR
	 */
	[Event( name="ioError", type="flash.events.IOErrorEvent" )]
	
	/**
	 * Se distribuye si se intenta llamar a URLLoader.load() para 
	 * cargar datos de un servidor situado fuera del entorno limitado 
	 * de seguridad.
	 * 
	 * @eventType flash.event.SecurityErrorEvent.SECURITY_ERROR
	 */
	[Event( name="securityError", type="flash.events.SecurityErrorEvent" )]
	
	/* ### CLASS ### */
	
	/**
	* Permite realizar una conexion con el servidor, tanto para enviar como para enviar y recibir.
	* @author	PollyJex
	* 
	* @example 
	* <listing version="3.0" >
	* 
	* 	var $handler:Function = function( event:ConexionEvent ):void {
	* 		trace( "DATA:", event.property );
	* 	}
	*  
	* 	var cnx:Conexion = new Conexion();
	* 	cnx.url = "http://www.domain.com/handler.php";
	* 	cnx.method = "POST";
	* 	cnx.action = "LOGIN";
	* 	cnx.username = "pepo";
	* 	cnx.password = "q2w3e4";
	* 	cnx.addEventListener( ConexionEvent.COMPLETE, $handler );
	* 	cnx.send();
	* 
	* </listing>
	*/
	public dynamic class Conexion extends Proxy implements IEventDispatcher {
		
		/**
		 * Mantiene la conexion con el servidor.
		 */
		private var _loader:URLLoader;
		
		/**
		 * Recive el resultado de la operacion.
		 */
		private var _request:URLRequest;
		
		/**
		 * Variables que seran enviadas a traves de la conexion.
		 */
		private var _variables:URLVariables;	
		
		/**
		 * Define el path del handler al que se debe acceder en el servidor.
		 */
		private var _url:String;
		
		/**
		 * Define el metodo que se utilizara para enviar los datos al servidor.
		 */
		private var _method:String;
		
		/**
		 * Controlador de eventos.
		 */
		private var _dispatcher:EventDispatcher;
		
		/* ### CONSTRUCTOR ### */
		
		/**
		* Constructor.
		* @param	void
		* @return	Conexion
		*/
		public function Conexion( url:String = null ) {
			
			this.clear();
			
			this._dispatcher = new EventDispatcher( this );
			
			this._loader = new URLLoader();			
			this._loader.addEventListener( Event.COMPLETE, HandlerComplete );
			this._loader.addEventListener( Event.OPEN, HandlerOpen );			
			this._loader.addEventListener( ProgressEvent.PROGRESS, HandlerProgress );			
			this._loader.addEventListener( HTTPStatusEvent.HTTP_STATUS, HandlerHttpStatus );
			this._loader.addEventListener( IOErrorEvent.IO_ERROR, HandlerIoError );
			this._loader.addEventListener( SecurityErrorEvent.SECURITY_ERROR, HandlerSecurityError );
			
			this.url = url;
			
		}
		
		/* ### GETTER/SETTER ### */
		
		/**
		 * Datos recividos por el proceso de envio.
		 * @return	*
		 */
		public function get data():* {
			
			return this._loader.data;
			
		}
		
		/**
		 * Formato de los datos recividos por el proceso 
		 * de envio ( text (d) | binary | variables ).
		 * @return	String
		 */
		public function get dataFormat():String {
			
			return this._loader.dataFormat;
			
		}
		
		public function set dataFormat( value:String ):void {
			
			this._loader.dataFormat = value;
			
		}		
		
		/**
		 * Metodo de envio.
		 * @return	String
		 */
		public function get method():String {
			
			return this._method;
			
		}
		
		public function set method( value:String ):void {
			
			this._method = ( value.toUpperCase() != "GET" ) ? "POST" : "GET" ;
			
		}
		
		/**
		 * Direccion de envio.
		 * @return	String
		 */
		public function get url():String {
			
			return this._url;
			
		}
		
		public function set url( value:String ):void {
			
			this._url = value;
			
		}
		
		/* ### METHODS ### */
		
		/**
		 * Reinicia la lista de variables.
		 * @return	void
		 */
		public function clear():void {
			
			this._variables = new URLVariables();
			
		}
		
		/**
		 * Envia la petición al servidor.
		 * @param	url		Direccion de envio.
		 * @param	method	Metodo de envio.
		 * @return	void
		 * ##########################################################################
		 * @exception	En caso de no definirse un url en el constructor o en el 
		 * 				metodo, se emite una excepcion del tipo Error.
		 * ##########################################################################
		 */
		public function send( url:String = null, method:String = "POST" ):void {
			
			if( TypeUtil.isEmpty( url ) ){
				
				if( TypeUtil.isEmpty( this.url ) ){
					
					throw new Error( "No se ha definido la url de conexion." );
					
				}else{
					
					url = this.url;
					
				}
				
			}
			
			if( ! TypeUtil.isEmpty( this.method ) ){
				
				method = this.method;
				
			}
			
			this._request = new URLRequest( url );
			this._request.method = method;
			
			if( ! TypeUtil.isEmpty( this._variables ) ){
				
				this._request.data = this._variables;
				
			}			
			
			this._loader.load( this._request );			
			
		}
		
		/* ### PROXY ### */
		
		/**
		* Anula la solicitud de eliminación de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @param	void
		* @return	Boolean
		*/
		override flash_proxy function deleteProperty( name:* ):Boolean {
			
			return delete this._variables[ name ];
			
		}
		
		/**
		* Anula cualquier solicitud del valor de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @return	*
		*/
		override flash_proxy function getProperty( name:* ):* {
			
			return this._variables[ name ];
			
		}
		
		/**
		* Anula una llamada para cambiar el valor de una propiedad.
		* @param	name	Nombre de la propiedad.
		* @param	value	Valor de la propiedad.
		* @return	void
		*/
		override flash_proxy function setProperty( name:*, value:* ):void {
			
			this._variables[ name ] = value;
			
		}
		
		/* ### EVENTS ### */
		
		/**
		* ADD EVENT.
		* @param	type
		* @param	listener
		* @param	useCapture
		* @param	priority
		* @param	useWeakReference
		* @return	void
		*/
		public function addEventListener( type:String, listener:Function, useCapture:Boolean = false, priority:int = 0, useWeakReference:Boolean = false ):void {
			
			this._dispatcher.addEventListener( type, listener, useCapture, priority, useWeakReference );
			
		}
		
		/**
		* DISPATCH EVENT.
		* @param	event
		* @return	Boolean
		*/
		public function dispatchEvent( event:Event ):Boolean {
			
			return this._dispatcher.dispatchEvent( event );
			
		}
		
		/**
		* HAS EVENT.
		* @param	type
		* @return	Boolean
		*/
		public function hasEventListener( type:String ):Boolean {
			
			return this._dispatcher.hasEventListener( type );
			
		}
		
		/**
		* REMOVE EVENT.
		* @param	type
		* @param	listener
		* @param	useCapture
		* @return	void
		*/
		public function removeEventListener( type:String, listener:Function, useCapture:Boolean = false ):void {
			
			this._dispatcher.removeEventListener( type, listener, useCapture );
			
		}
		
		/**
		* WILL TRIGGER.
		* @param	type
		* @return	Boolean
		*/
		public function willTrigger( type:String ):Boolean {
			
			return this._dispatcher.willTrigger( type );
			
		}
		
		/* ### HANDLERS ### */
		
		private function HandlerComplete( event:Event ):void {
			this._dispatcher.dispatchEvent( new ConexionEvent( ConexionEvent.COMPLETE, this._loader.data ) );
		}
		
		private function HandlerOpen( event:Event ):void {
			this._dispatcher.dispatchEvent( event );
		}		
		
		private function HandlerProgress( event:ProgressEvent ):void {
			this._dispatcher.dispatchEvent( event );
		}
		
		private function HandlerHttpStatus( event:HTTPStatusEvent ):void {
			this._dispatcher.dispatchEvent( event );
		}
		
		private function HandlerIoError( event:IOErrorEvent ):void {
			this._dispatcher.dispatchEvent( event );
		}
		
		private function HandlerSecurityError( event:SecurityErrorEvent ):void {
			this._dispatcher.dispatchEvent( event );
		}
		
	}
	
}
