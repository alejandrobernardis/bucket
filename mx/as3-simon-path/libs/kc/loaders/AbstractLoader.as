
package kc.loaders {
	import kc.api.IIterator;
	import kc.api.ILoader;
	import kc.tda.SimpleIterator;
	import kc.utils.ClassUtil;
	import kc.utils.ExceptionUtil;
	import kc.utils.PurgerUtil;
	import kc.utils.StringUtil;
	import kc.utils.UID;

	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLLoaderDataFormat;
	import flash.net.URLRequest;
	import flash.net.URLRequestMethod;
	import flash.net.URLVariables;
	import flash.system.LoaderContext;

	[Event( name="close", type="flash.events.Event" )]
	[Event( name="complete", type="flash.events.Event" )]
	[Event( name="open", type="flash.events.Event" )]
	[Event( name="progress", type="flash.events.ProgressEvent" )]
	[Event( name="httpStatus", type="flash.events.HTTPStatusEvent" )]
	[Event( name="ioError", type="flash.events.IOErrorEvent" )]
	[Event( name="securityError", type="flash.events.SecurityErrorEvent" )]

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class AbstractLoader extends EventDispatcher implements ILoader {

		// @const

		public static const LOAD:String = "load";
		public static const SEND:String = "send";
		public static const SEND_AND_LOAD:String = "sendAndLoad";

		public static const NOT_FOUND:int = -1;

		// @variables

		protected var _loader:*;
		protected var _content:*;
		protected var _request:URLRequest;
		protected var _requestUrl:String;
		protected var _requestMethod:String;
		protected var _requestData:URLVariables;
		protected var _requestHeaders:Array;
		protected var _requestContentType:String;
		protected var _context:LoaderContext;
		protected var _type:String;
		protected var _dataFormat:String;
		protected var _progress:uint;
		protected var _bytyesLoaded:uint;
		protected var _bytyesTotal:uint;
		protected var _events:Array;
		protected var _eventsTarget:*;

		protected var _catchExceptions:Boolean;
		protected var _antiCache:Boolean;
		protected var _loaded:Boolean;
		protected var _uid:String;

		// @constructor

		public function AbstractLoader() {

			super( this );

			_events = [
				[ Event.COMPLETE, CompleteHandler, false, 0, false ],
				[ Event.OPEN, dispatchEvent, false, 0, false ],
				[ ProgressEvent.PROGRESS, ProgressHandler, false, 0, false ],
				[ HTTPStatusEvent.HTTP_STATUS, dispatchEvent, false, 0, false ],
				[ IOErrorEvent.IO_ERROR, ErrorHandler, false, 0, false ],
				[ SecurityErrorEvent.SECURITY_ERROR, ErrorHandler, false, 0, false ]
			];

		}

		// @properties (rw)

		public function get url():String {
			return _requestUrl;
		}

		public function set url(value:String):void {
			_requestUrl = value;
		}

		public function get method():String {
			return _requestMethod || URLRequestMethod.POST;
		}

		public function set method(value:String):void {
			_requestMethod = ( value != URLRequestMethod.GET )
				? URLRequestMethod.POST
				: URLRequestMethod.GET;
		}

		public function get variables():URLVariables {
			return _requestData;
		}

		public function set variables(value:URLVariables):void {
			_requestData = value;
		}

		public function get headers():Array {
			return _requestHeaders || new Array();
		}

		public function set headers(value:Array):void {
			_requestHeaders = value;
		}

		public function get contentType():String {
			return _requestContentType;
		}

		public function set contentType(value:String):void {
			_requestContentType = value;
		}

		public function get context():LoaderContext {
			return _context;
		}

		public function set context(value:LoaderContext):void {
			_context = value;
		}

		public function get type():String {
			return _type || LoaderType.getType( _requestUrl );
		}

		public function set type(value:String):void {
			_type = value;
		}

		public function get dataFormat():String {
			return _dataFormat || URLLoaderDataFormat.TEXT;
		}

		public function set dataFormat(value:String):void {
			_dataFormat = value;
		}

		// @control

		public function get catchExceptions():Boolean {
			return _catchExceptions;
		}

		public function set catchExceptions(value:Boolean):void {
			_catchExceptions = value;
		}

		public function get antiCache():Boolean {
			return _antiCache;
		}

		public function set antiCache(value:Boolean):void {
			_antiCache = value;
		}

		// @properties (r)

		public function get uid():String {
			if( ! _uid ){
				_uid = UID.create();
			} return _uid;
		}

		public function get content():* {
			return _content || null;
		}

		public function get progress():uint {
			return _progress;
		}

		public function get bytesLoaded():uint {
			return _bytyesLoaded || 0;
		}

		public function get bytesTotal():uint {
			return _bytyesTotal || 0;
		}

		public function isLoaded():Boolean {
			return _loaded;
		}

		public function eventsList():Array {
			return _events.slice();
		}

		// @methods

		public function clear():void {
			ResolveClear();
		}

		public function close():void {

			if( ! _loader ) return;

			if( ClassUtil.isMethod( _loader, "close" ) ) {
				try{
					_loader.close();
				}catch(e:*){
					// ExceptionUtil.ViewError( e, true );
				}
			}

			if( dispatchEvent( new Event( Event.CLOSE ) ) ){
				ResolveClear();
			}

		}

		public function load( url:String = null, method:String = null ):void {
			ResolveConexion( LOAD, url, method );
		}

		public function send( url:String = null, method:String = null ):void {
			ResolveConexion( SEND, url, method );
		}

		public function sendAndLoad( url:String = null, method:String = null ):void {
			ResolveConexion( SEND_AND_LOAD, url, method );
		}

		protected function ResolveConexion( action:String, url:String = null, method:String = null ):void {

			// Clear

			ResolveClear();

			// Properties

			if( ! url ){
				//TODO: Implementar un analizador de URL.
				if( StringUtil.isEmpty( _requestUrl ) )
					ExceptionUtil.ViewError(
						"The URL is undefined: #" + action,
						_catchExceptions
					);
			} else {
				_requestUrl = url;
			}

			if( method != null ) {
				this.method = method;
			}

			// Request

			_request = new URLRequest();
			_request.url = ResolveURL();
			_request.method = this.method;
			_request.data = this.variables;
			_request.contentType = this.contentType;
			_request.requestHeaders = this.headers;

		}

		// @handlers

		protected function CompleteHandler(e:Event):void {
			_loaded = true;
			if( dispatchEvent( new Event( Event.COMPLETE ) ) ){
				ResolveClear( false );
			}
		}

		protected function ProgressHandler(e:ProgressEvent):void {
			_bytyesLoaded = e.bytesLoaded;
			_bytyesTotal = e.bytesTotal;
			_progress = ( _bytyesLoaded / _bytyesTotal ) * 100;
			dispatchEvent(e);
		}

		protected function ErrorHandler(e:ErrorEvent):void {
			ResolveClear();
			if( ! _catchExceptions ) {
				dispatchEvent(e as Event);
			}else{
				ExceptionUtil.ViewError( e, _catchExceptions );
			}
		}

		// @purge

		public function purge(...rest):void {
			close();
			PurgerUtil.cleanCollection( _requestHeaders );
			PurgerUtil.cleanCollection( _events );
			_loader = null;
			_content = null;
			_request = null;
			_requestUrl = null;
			_requestMethod = null;
			_requestData = null;
			_requestHeaders = null;
			_requestContentType = null;
			_context = null;
			_type = null;
			_dataFormat = null;
			_events = null;
			_eventsTarget = null;
			_progress = undefined;
			_bytyesLoaded = undefined;
			_bytyesTotal = undefined;
			_catchExceptions = undefined;
			_antiCache = undefined;
			_loaded = undefined;
		}

		// @helpers

		protected function ResolveClear( content:Boolean = true ):void {

			ResetProgress();
			ResolveEvents(null, true);
			_loader = null;

			if( content ) {
				_loaded = false;
				_content = null;
			}

		}

		protected function ResetProgress():void {
			_progress = 0;
			_bytyesLoaded = 0;
			_bytyesTotal = 0;
		}

		protected function ResolveEvents( list:Array = null, remove:Boolean = false ):void {

			if( ! _loader ) return;
			if( ! _eventsTarget ) _eventsTarget = _loader;

			var f:String = ( ! remove )
				? "addEventListener"
				: "removeEventListener";

			var i:IIterator = new SimpleIterator( list || _events );

			while( i.hasNext() ) {
				_eventsTarget[f].apply(
					_loader,
					( ! remove )
						? i.next()
						: i.next().slice( 0, 2 )
				);
			}

		}

		protected function ResolveURL():String {
			return ( ! _antiCache )
				? _requestUrl
				: ResolveCache( _requestUrl );
		}

		protected function ResolveCache( value:String ):String {
			return new String(
				value + (
					( value.search(/\?[a-z].+/gi) != NOT_FOUND )
						? "&"
						: "?"
				) + "kcfac=" + new Date().getTime().toString()
			);
		}

	}

}
