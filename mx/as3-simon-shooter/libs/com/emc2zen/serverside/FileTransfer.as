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
	
	import com.emc2zen.data.file.FileMimeType;
	import com.emc2zen.data.file.FileType;
	import com.emc2zen.data.iterator.ArrayIterator;
	import com.emc2zen.data.queue.Queue;
	import com.emc2zen.util.TypeUtil;
	import flash.events.DataEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.HTTPStatusEvent;
	import flash.events.IEventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.FileFilter;
	import flash.net.FileReference;
	import flash.net.FileReferenceList;
	import flash.net.URLRequest;	
	import flash.net.URLVariables;
	
	/* ### EVENTS ### */
	
	/**
	 * Se distribuye cuando el usuario cancela la carga o descarga de un 
	 * archivo mediante el cuadro de diálogo de búsqueda de archivos. 
	 * Flash Player no distribuye este evento si el usuario cancela una 
	 * carga o descarga mediante otros métodos (cerrando el navegador o 
	 * la aplicación actual).
	 * 
	 * @eventType flash.event.Event.CANCEL
	 */
	[Event( name="cancel", type="flash.events.Event" )]
	
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
	 * Se distribuye si se intenta llamar a URLLoader.load() para 
	 * cargar datos de un servidor situado fuera del entorno limitado 
	 * de seguridad.
	 * 
	 * @eventType flash.event.SecurityErrorEvent.SECURITY_ERROR
	 */
	[Event( name="securityError", type="flash.events.SecurityErrorEvent" )]
	
	/**
	 * Se distribuye cuando el usuario selecciona un archivo para la carga 
	 * o descarga en el cuadro de diálogo de búsqueda de archivos. (Este 
	 * cuadro de diálogo se abre cuando llama a los métodos 
	 * FileReference.browse(), FileReferenceList.browse() o 
	 * FileReference.download().) Cuando el usuario selecciona un archivo 
	 * y confirma la operación (por ejemplo, haciendo clic en Aceptar), 
	 * se llenan las propiedades del objeto FileReference.
	 * 
	 * @eventType flash.event.Event.select
	 */
	[Event( name="select", type="flash.events.Event" )]
	
	/**
	 * Se distribuye cuando se han recibido datos del servidor tras 
	 * una carga correcta. Este evento no se distribuye si no se 
	 * devuelven datos desde el servidor.
	 * 
	 * @eventType flash.event.DataEvent.UPLOAD_COMPLETE_DATA
	 */
	[Event( name="uploadCompleteData", type="flash.events.DataEvent" )]	
	
	/* ### CLASS ### */
	
	/**
	 * Administra la conexion con el servidor para la carga y descarga de uno o mas archivos.
	 * @author	PollyJex
	 */
	public class FileTransfer implements IEventDispatcher {
		
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
		
		/**
		 * Define si el explorador permite una lista de archivos o solo uno.
		 */
		private var _fileList:Boolean;
		
		/**
		 * Cola para la cara de archivos.
		 */
		private var _fileQueue:Queue;
		
		/**
		 * Referencia del objeto FileReference.
		 */
		private var _fileReference:FileReference;	
		
		/**
		 * Referencia del objeto FileReferenceList.
		 */
		private var _fileReferenceList:FileReferenceList;		
		
		/* ### CONSTRUCTOR ### */
		
		/**
		 * Constructor.
		 * @param	mode	Define el modo que se selecciona uno o varios archivos.
		 * @return	FileTransfer
		 */
		public function FileTransfer( fileList:Boolean = false ) {
			
			this._request = new URLRequest();
			this._variables = new URLVariables();
			this._dispatcher = new EventDispatcher( this );
			this._fileQueue = new Queue();
			this._fileReference = new FileReference();
			this._fileReferenceList = new FileReferenceList();
			
			this.ResolveEvents();
			
			this._fileReferenceList.addEventListener( Event.CANCEL, HandlerCancel );
			this._fileReferenceList.addEventListener( Event.SELECT, HandlerSelect );
			
			this.fileList = fileList;
			
		}
		
		/* ### GETTER/SETTER ### */
		
		/**
		 * Retorna los datos del archivo.
		 * @return	FileReference
		 */
		public function get fileData():FileReference {
			
			return this._fileReference;
			
		}
		
		/**
		 * Retona un Array con la lista de archivos y sus datos.
		 * @return	Array
		 */
		public function get fileDataList():Array {
			
			return this._fileQueue.toArray();
			
		}
		
		/**
		 * Define el modo que se seleccionan uno o varios archivos.
		 * @return	Boolean
		 */
		public function get fileList():Boolean {
			
			return this._fileList;
			
		}
		
		public function set fileList( value:Boolean ):void {
			
			this._fileList = value;
			
		}		
		
		/**
		 * Metodo de envio.
		 * @return	String
		 */
		public function get method():String {
			
			return this._request.method;
			
		}
		
		public function set method( value:String ):void {
			
			this._request.method = ( value.toUpperCase() != "GET" ) ? "POST" : "GET" ;
			
		}
		
		/**
		 * Direccion de envio.
		 * @return	String
		 */
		public function get url():String {
			
			return this._request.url;
			
		}
		
		public function set url( value:String ):void {
			
			this._request.url = value;
			
		}
		
		/**
		 * Datos de envio.
		 * @return	Object
		 */
		public function get data():Object {
			
			return this._request.data;
			
		}
		
		public function set data( value:Object ):void {
			
			this._request.data = value;
			
		}
		
		/* ### METHODS ### */
		
		/**
		 * Muestra un cuadro de diálogo de búsqueda de archivos en el que el 
		 * usuario puede seleccionar uno o varios archivos locales para la carga.
		 * @param	typeList	Lista de tipos de archivos ( Array[ FileFilter ] | FileFilter )
		 * @return	Boolean
		 */
		public function browse( typeList:* ):Boolean {
			
			var list:Array = new Array();
			
			if( TypeUtil.thisIs( typeList, FileFilter ) ){
				
				list.push( typeList );
				
			}else if( TypeUtil.isArray( typeList ) ){
				
				list = typeList;
				
			}else{
				
				throw new Error( "El tipo de lista no corresponde al modelo de dato." );
				
			}
			
			if( ! this.fileList ){
				
				return this._fileReference.browse( list );
				
			}else{
				
				return this._fileReferenceList.browse( list );
				
			}
			
		}
		
		/**
		 * Cancela la carga o descarga de archivos.
		 * @return	void
		 */
		public function cancel():void {
			
			this._fileReference.cancel();
			
		}
		
		/**
		 * Inicializa la descarga de un solo archivo.
		 * @param	defaultName		Nombre por default.
		 * @return	void
		 */
		public function download( defaultName:String = null ):void {
			
			this._fileReference.download( this._request, defaultName );
			
		}
		
		/**
		 * Inicializa la carga de un solo archivo.
		 * @param	defaultName		Nombre por default
		 * @param	testUpload		Testea si la carga se puede realizar correctamente.
		 * @return	void
		 */
		public function upload( defaultName:String = "FileData", testUpload:Boolean = false ):void {
			
			this._fileReference.upload( this._request, defaultName, testUpload );
			
		}
		
		/**
		 * Inicializa la carga de la lsiat de archivos.
		 * @return	void
		 */
		public function uploadQueue():void {
			
			ResolveQueue();
			
		}
		
		/**
		 * Reinicia la lista de archivos a cargar.
		 * @return	void
		 */
		public function clearQueue():void {
			
			this._fileQueue.clear();
			
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
			
			if( this._fileList ){
				
				this.ResolveQueue(); 
				
			}
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerOpen( event:Event ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerCancel( event:Event ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerSelect( event:Event ):void {
			
			if( this.fileList ){
				
				var ai:ArrayIterator = new ArrayIterator( this._fileReferenceList.fileList );
				
				while( ai.hasNext() ){
					
					ai.next();
					
					if( ! this._fileQueue.contains( ai.value() ) ){
						
						this._fileQueue.enqueue( ai.value() );
						
					}
					
				}
				
			}
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerHttpStatus( event:HTTPStatusEvent ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerIoError( event:IOErrorEvent ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerProgress( event:ProgressEvent ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerSecurityError( event:SecurityErrorEvent ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		private function HandlerData( event:DataEvent ):void {
			
			this._dispatcher.dispatchEvent( event );
			
		}
		
		/* ### INTERNAL HELPERS ### */
		
		/**
		 * Resuelve la implementacion de una cola de carga.
		 * @return	void
		 */
		private function ResolveQueue():void {
			
			if( ! this._fileQueue.isEmpty() ){
				
				this._fileReference = this._fileQueue.poll();
				this.ResolveEvents();
				this.upload();
				
				return;
				
			}
			
			this._dispatcher.dispatchEvent( new FileTransferEvent( FileTransferEvent.COMPLETE_QUEUE, this.fileDataList ) );
			
		}
		
		/**
		 * Setea los eventos de los objetos FileReference y FileReferenceList
		 * @return	void
		 */
		private function ResolveEvents():void {
			
			this._fileReference.addEventListener( Event.COMPLETE, HandlerComplete );
			this._fileReference.addEventListener( Event.OPEN, HandlerOpen );
			this._fileReference.addEventListener( Event.CANCEL, HandlerCancel );
			this._fileReference.addEventListener( Event.SELECT, HandlerSelect );
			this._fileReference.addEventListener( HTTPStatusEvent.HTTP_STATUS, HandlerHttpStatus );
			this._fileReference.addEventListener( IOErrorEvent.IO_ERROR, HandlerIoError );
			this._fileReference.addEventListener( ProgressEvent.PROGRESS, HandlerProgress );
			this._fileReference.addEventListener( SecurityErrorEvent.SECURITY_ERROR, HandlerSecurityError );
			this._fileReference.addEventListener( DataEvent.UPLOAD_COMPLETE_DATA, HandlerData );
			
		}
		
		/**
		 * Resuelve la url que se utiliza en la operación.
		 * @param	url		Valor de la url a utilizar.
		 * @return	String
		 */
		private function ResolveURL( url:String ):String {
			
			if( TypeUtil.isEmpty( url ) ){
				
				if( TypeUtil.isEmpty( this.url ) ){
					
					throw new Error( "No se ha definido la url de conexion." );
					
				}else{
					
					return this.url;
					
				}
				
			}
			
			return url;
			
		}		
		
	}
	
}

/**
 * TODO: poder enviar variables con la carga de archivos.
 * TODO: soporte para add / remove archivos de la lista.
 */