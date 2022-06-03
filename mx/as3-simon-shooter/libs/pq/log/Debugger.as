
package pq.log {
	
	import pq.core.CoreStatic;
	
	public class Debugger extends CoreStatic {
		
		public function Debugger() {
			super();
		}
		
		public static function DEBUG( context:*, ...rest:Array ):void {
			Logger.LOG.apply( Logger, new Array( Level.DEBUG, context ).concat( rest ) );
		}
		
		public static function INFO( context:*, ...rest:Array ):void {
			Logger.LOG.apply( Logger, new Array( Level.INFO, context ).concat( rest ) );
		}
		
		public static function WARN( context:*, ...rest:Array ):void {
			Logger.LOG.apply( Logger, new Array( Level.WARN, context ).concat( rest ) );
		}
		
		public static function ERROR( context:*, ...rest:Array ):void {
			Logger.LOG.apply( Logger, new Array( Level.ERROR, context ).concat( rest ) );
		}
		
		public static function CRITICAL( context:*, ...rest:Array ):void {
			Logger.LOG.apply( Logger, new Array( Level.CRITICAL, context ).concat( rest ) );
		}
		
		public static function FATAL( context:*, ...rest:Array ):void {
			Logger.LOG.apply( Logger, new Array( Level.FATAL, context ).concat( rest ) );
		}
		
		public static function active( value:Boolean ):void {
			Logger.active.apply( Logger, new Array( value ) );
		}
		
		public static function level( value:String ):void {
			Logger.level.apply( Logger, new Array( value ) );
		}
		
		public static function appender( value:String ):void {
			Logger.appender.apply( Logger, new Array( value ) );
		}	
		
		public static function filter( value:String ):void {
			Logger.filter.apply( Logger, new Array( value ) );
		}
		
		public static function separator( value:String ):void {
			Logger.separator.apply( Logger, new Array( value ) );
		}
		
		public static function test():void {
			Logger.test.apply( Logger, new Array( true ) );
		}
		
	}
	
}