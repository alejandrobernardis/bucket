
package pq.log {
	
	import pq.core.CoreStatic;
	
	public class Logger extends CoreStatic {
		
		private static var $log:Appender = null;
		private static var $active:Boolean = false;
		
		public function Logger() {
			super();
		}
		
		public static function LOG( level:Level, context:* = null, ...rest:Array ):void {
			
			if ( ! Logger.$active ) return;
			
			Logger.$log.level = level;
			Logger.$log.context = context;
			Logger.$log.message = rest;
			
			Logger.$log.send();
			
		}
		
		public static function active( value:Boolean ):void {
			Logger.$active = value;
			Logger.$log = ( ! value ) ? null : new Appender();
		}
		
		public static function level( value:String ):void {
			if ( Logger.$log == null ) return;
			Logger.$log.levels = value;
		}
		
		public static function appender( value:String ):void {
			if ( Logger.$log == null ) return;
			Logger.$log.appender = value;
		}
		
		public static function filter( value:String ):void {
			if ( Logger.$log == null ) return;
			Logger.$log.filters = value;
		}	
		
		public static function separator( value:String ):void {
			if ( Logger.$log == null ) return;
			Logger.$log.separator = value;
		}
		
		public static function test( external:Boolean = false ):void {
			var clazz:Class = ( ! external ) ? Logger : Debugger;
			trace( "\n1. Levels:" );
				Logger.LOG( Level.DEBUG, 	clazz, "Test" );
				Logger.LOG( Level.INFO, 	clazz, "Test" );
				Logger.LOG( Level.WARN, 	clazz, "Test" );
				Logger.LOG( Level.ERROR, 	clazz, "Test" );
				Logger.LOG( Level.CRITICAL, clazz, "Test" );
				Logger.LOG( Level.FATAL, 	clazz, "Test" );
			trace( "\n2. Packages:" );
				trace( Logger.$log.getFilters().join( "\n" ) );
			trace( "\n3. Configurations:" );	
		}
		
	}
	
}