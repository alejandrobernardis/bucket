
package pq.log {
	
	import flash.events.EventDispatcher;
	import flash.events.IEventDispatcher;
	import pq.api.IAppender;
	import pq.log.appenders.FirebugAppender;
	import pq.log.appenders.OutputAppender;
	import pq.log.appenders.SimpleAppender;
	import pq.utils.TypeUtil;
	
	public class Layout extends EventDispatcher implements IEventDispatcher {
		
		protected var _appender:IAppender;
		protected var _level:Level;
		protected var _context:*;
		protected var _message:*;
		
		public function Layout() {
			super( this );
		}
		
		public function get appender():String { 
			return this._appender.toString(); 
		}
		
		public function set appender( value:String ):void {
			this._appender = ResolveAppender( value );
		}
		
		public function get level():Level { 
			return this._level; 
		}
		
		public function set level( value:Level ):void { 
			this._level = value; 
		}
		
		public function get context():* { 
			return this._context; 
		}
		
		public function set context( value:* ):void { 
			this._context = value; 
		}
		
		public function get message():* { 
			return this._message; 
		}
		
		public function set message( value:* ):void { 
			if ( ( value as Array ).length == 1 ) value = value[0];
			this._message = value; 
		}
		
		public function clear( ...rest ):void {
			this._appender = null;
			this._level = null;
			this._context = null;
		}
		
		public function purge( ...rest ):void {
			this.clear();
			this._appender = null;
		}
		
		private function ResolveAppender( value:String ):IAppender {
			
			switch( value.toLowerCase() ) {
				
				case Appender.FIREBUG:
					return new FirebugAppender();
					
				case Appender.OUTPUT:
					return new OutputAppender();
				
				case Appender.SIMPLE:
				default:
					return new SimpleAppender();
				
			}
			
		}
		
	}
	
}