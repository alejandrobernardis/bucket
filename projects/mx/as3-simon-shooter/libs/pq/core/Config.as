package pq.core {
	import pq.api.IConfig;

	import com.emc2zen.serverside.Conexion;
	import com.emc2zen.serverside.ConexionEvent;

	import flash.errors.IllegalOperationError;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	
	
	[Event(name="complete", type="flash.events.Event")]
	[Event(name="error", type="flash.events.ErrorEvent")]
	[Event(name="progress", type="flash.events.ProgressEvent")]
	
	public class Config extends EventDispatcher implements IConfig {
		
		private var _cnx:Conexion;
		private var _url:String;
		
		protected var _data:XML;
		protected var _action:String = "NO_ACTION";
		
		public function Config( data:XML = null ) {
			super( this );
			this._data = data;
		}
		
		public function get data():XML {
			return this._data;
		}
		
		public function get action():String {
			return this._action;
		}
		
		public function set action( value:String ):void {
			this._action = value;
		}
		
		public function get url():String {
			return this._url;
		}
		
		public function set url( value:String ):void {
			this._url = value;
		}
		
		public function dependency( value:String ):String {
			
			var list:Array;
			var node:XMLList;
			var attribute:String = null;
			var vnode:String;
			var lnode:Array = value.match( /\{([a-zA-Z]([\w\_\-])*)(([\.][a-zA-Z]([\w\_\-])*)*([\.](@?)[a-zA-Z]([\w\_\-])*))?\}/g );
			
			if ( lnode != null && lnode.length > 0 ) {
				
				for ( var $a:uint = 0; $a < lnode.length; $a++ ) {
					
					node = this._data.children();	
					vnode = String( lnode[$a] ); 
					list = String( vnode.match( /([a-zA-Z]([\w\_\-])*)(([\.][a-zA-Z]([\w\_\-])*)*([\.](@?)[a-zA-Z]([\w\_\-])*))?/g )[0] ).split( "." );
					
					if( String( list[ list.length - 1 ] ).search( /\@/ ) > -1 ){
						attribute = String( list.pop() ).replace( /\@/, "" );
					}
					
					for ( var $b:uint = 0; $b < list.length; $b++ ) {
						if( node.hasOwnProperty( list[$b] ) ){
							node = node.child( list[$b] );
						}else if( $b > 0 && ! node.hasOwnProperty( list[$b] ) ){
							return null;
						}
					}
					
					if( attribute != null ){
						value = value.replace( vnode, node.attribute( attribute ) );
					}else{
						value = value.replace( vnode, node.text() );
					}
					
				}
				
				return value;
				
			}
			
			return value;
			
		}
		
		public function load( url:String = null ):void {
			
			if( this._url == null && url == null ){
				throw new IllegalOperationError( "La URL no fue definida." );
			}else if( url != null ){
				this._url = url;
			}
			
			this._cnx = new Conexion();
			this._cnx.action = this._action;
			this._cnx.method = "GET";
			this._cnx.addEventListener( ConexionEvent.COMPLETE, CompleteHandler );			
			this._cnx.addEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			this._cnx.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler ); 
			this._cnx.addEventListener( ProgressEvent.PROGRESS, ProgressHandler );
			this._cnx.send( this._url );
			
		}
		
		protected function ClearHandler( e:Event ):void {
			this._cnx.removeEventListener( ConexionEvent.COMPLETE, CompleteHandler );
			this._cnx.removeEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			this._cnx.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler );
			this._cnx.removeEventListener( ProgressEvent.PROGRESS, ProgressHandler ); 
			this._cnx = null;
		}
		
		protected function ProgressHandler( e:ProgressEvent ):void {
			this.dispatchEvent( new ProgressEvent( ProgressEvent.PROGRESS, false, false, e.bytesLoaded, e.bytesTotal ) );
		}
		
		protected function ErrorHandler( e:ErrorEvent ):void {
			this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR, false, false, e.text ) );	
			this.ClearHandler(e);
		}
		
		protected function CompleteHandler( e:ConexionEvent ):void {	
			this._data = new XML( String( e.property ) );
			this._data.ignoreWhitespace = true;
			this._data.ignoreComments = true;
			this.dispatchEvent( new Event( Event.COMPLETE ) );
			this.ClearHandler(e);
		}
		
		public function purge(...rest):void {
			this._action = null;
			this._data = null;
			this._url = null;			
		}
		
	}
	
}