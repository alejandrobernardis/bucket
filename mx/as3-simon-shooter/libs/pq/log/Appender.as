
package pq.log {
	
	import pq.log.*;
	
	public class Appender extends Filter {
		
		public static const OUTPUT:String = "output";
		public static const FIREBUG:String = "firebug";
		public static const SIMPLE:String = "simple";
		
		public function Appender() {
			super();
		}
		
		public function send():void {
			if ( ! validate() ) return;
			this._appender.send( this );
		}	
		
	}
	
}

