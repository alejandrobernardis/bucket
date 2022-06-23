package activia.simon.shooter.core {
	import pq.core.CoreSingleton;
	import pq.log.Debugger;
	import pq.utils.StringUtil;

	import flash.events.AsyncErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.SecurityErrorEvent;
	import flash.events.StatusEvent;
	import flash.net.LocalConnection;
	
	
	public class FacebookUtil extends EventDispatcher {
		
		private static var $singleton:FacebookUtil;
		
		public function FacebookUtil( access:SingletonClass = null ) {			
			if( access != null ){
				super( this );
			}else {				
				new CoreSingleton();
			}
		}
		
		public static function destroy():void {	
			$singleton.purge();
			$singleton = null;			
		}
		
		public static function getInstance():FacebookUtil {			
			if( $singleton == null ){
				$singleton = new FacebookUtil( new SingletonClass() );
				$singleton.config();
			}			
			return $singleton;			
		}	
		
		private var _cnx:LocalConnection;
		private var _cnxname:String;
		
		private function config():void{
			this._cnx = new LocalConnection();
			DataLayer.applyAllowDomains( this._cnx );
			this._cnx.addEventListener( AsyncErrorEvent.ASYNC_ERROR, ErrorHandler );
			this._cnx.addEventListener( Event.DEACTIVATE, ErrorHandler );
			this._cnx.addEventListener( Event.ACTIVATE, ErrorHandler );
			this._cnx.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler );
			this._cnx.addEventListener( StatusEvent.STATUS, ErrorHandler );			
			this._cnxname = String( DataLayer.FLASH_VARS.fb_local_connection );
		}	
		
		private function ErrorHandler( e:* ):void {
			
			var error:Object = {};
			error.type = e.type;
			
			if ( e.hasOwnProperty("error") || e.hasOwnProperty("text") ) {
				error.error = e.error || e.text || "Error no controlado.";
			}
			
			if ( e.hasOwnProperty("code") ) {
				error.code = e.code || "not-code";
			}
			
			if ( e.hasOwnProperty("level") ) {
				error.code = e.level || "not-level";
			}
			
			Debugger.FATAL( this, error );
			
		}
		
		public function goto( url:String ):void {
			if ( this._cnx != null ) {
				this._cnx.send( this._cnxname, "navigateToURL", url );
			}
		}
		
		public function call( method:String, param:Array ):void {
			if ( this._cnx != null ) {
				this._cnx.send( this._cnxname, "callFBJS", method, param );
			}
		}	
		
		public function addCallBack( method:String, func:Function ):void {
			if ( this._cnx != null ) {
				if ( this._cnx.client == null ) {
					this._cnx.client = new Object();
				}
				this._cnx.client[ method ] = func;
			}			
		}
		
		public function resolveXML( value:XML ):void {
			
			if ( ! value.hasOwnProperty( "method" ) ) {
				if ( value.text().toString().search( /^http\:\/\//i ) > -1 ) {
					Debugger.DEBUG( this, value.text().toString() );
					this.goto( value.text().toString() );
				} return;
			}
			
			var method:String = value.method.text().toString();
			
			if ( StringUtil.isEmpty( method ) ) {
				Debugger.ERROR( this, "El nombre del metodo no fue definido." );
				return;
			}
			
			var list:Array = new Array();
			
			for each ( var node:XML in value..param ) {
				if ( DataLayer.collection.contain( node.@id.toString() ) ) {
					list.push( DataLayer.collection.value( node.@id.toString() ) );
				}
			}
			
			this.call( method, list );
			Debugger.DEBUG( this, method, list );
			
		}
		
		public function purge( ...rest ):void {
			this._cnx.removeEventListener( AsyncErrorEvent.ASYNC_ERROR, ErrorHandler );
			this._cnx.removeEventListener( Event.DEACTIVATE, ErrorHandler );
			this._cnx.removeEventListener( Event.ACTIVATE, ErrorHandler );
			this._cnx.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler );
			this._cnx.removeEventListener( StatusEvent.STATUS, ErrorHandler );
			this._cnx = null;
			this._cnxname = null;
			$singleton = null;
		}
		
	}

}

internal final class SingletonClass { }