
package {

	import kc.logging.SimpleLog;
	import kc.core.KCDataLayer;
	import kc.core.KCSingleton;

	import flash.events.AsyncErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.SecurityErrorEvent;
	import flash.events.StatusEvent;
	import flash.net.LocalConnection;

	/**
	 * @author Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
	 */
	public class KCFacebook extends EventDispatcher {

		private static var $singleton:KCFacebook;
		
		public function KCFacebook( access:SingletonClass = null ) {			
			if( access != null ){
				super( this );
			}else {				
				new KCSingleton();
			}
		}
		
		public static function destroy():void {	
			$singleton.purge();
			$singleton = null;			
		}
		
		public static function getInstance():KCFacebook {			
			if( $singleton == null ){
				$singleton = new KCFacebook( new SingletonClass() );
				$singleton.config();
			}			
			return $singleton;			
		}	
		
		private var _cnx:LocalConnection;
		private var _cnxname:String;
		
		private function config():void{
			
			this._cnx = new LocalConnection();
			this._cnx.allowDomain("*");
			this._cnx.addEventListener( AsyncErrorEvent.ASYNC_ERROR, ErrorHandler );
			this._cnx.addEventListener( Event.DEACTIVATE, ErrorHandler );
			this._cnx.addEventListener( Event.ACTIVATE, ErrorHandler );
			this._cnx.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorHandler );
			this._cnx.addEventListener( StatusEvent.STATUS, ErrorHandler );			
			
			try{
				this._cnxname = String( KCDataLayer.flashVars.fb_local_connection );
			}catch(e:Error){
				SimpleLog.print('facebook-cathc',e);
			}
			
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
			
			SimpleLog.dump("facebook-error", error);
			
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