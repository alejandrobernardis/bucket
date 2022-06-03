
package pq.log {
	
	import pq.utils.StringUtil;
	
	public class Level {
		
		public static const ALL:Level 		= new Level( uint.MIN_VALUE,	"all", 		0x666666 );
		public static const DEBUG:Level 	= new Level( 10000, 			"debug", 	0x339999 );
		public static const INFO:Level 		= new Level( 20000, 			"info",	 	0x3399FF );
		public static const WARN:Level 		= new Level( 30000, 			"warn", 	0xFFCC00 );
		public static const ERROR:Level 	= new Level( 40000, 			"error", 	0xBB0000 );
		public static const CRITICAL:Level 	= new Level( 50000, 			"critical", 0xDD6600 );
		public static const FATAL:Level 	= new Level( 60000, 			"fatal", 	0xFF0000 );
		public static const OFF:Level 		= new Level( uint.MAX_VALUE, 	"off", 		0x666666 );
		
		private var _id:int;
		private var _label:String;
		private var _colour:uint;
		
		public function Level( id:int, label:String, colour:uint ) {
			this._id = id;
			this._label = label;
			this._colour = colour;
		}
		
		public function get id():int {
			return this._id;
		}
		
		public function get label():String {
			return this._label;
		}
		
		public function get colour():uint {
			return this._colour;
		}
		
		public function equals( value:Level ):Boolean {
			return ( this._id == value.id );
		}
		
		public function gequals( value:Level ):Boolean {
			return ( this._id >= value.id );
		}
		
		public function lequals( value:Level ):Boolean {
			return ( this._id <= value.id );
		}
		
		public static function resolveAsId( value:String ):int {
			return ResolveAs( value ).id;
		}
		
		public static function resolveAsName( value:int ):String {
			return ResolveAs( value ).label;
		}
		
		public static function resolveAsColour( value:* ):uint {
			return ResolveAs( value ).colour;
		}
		
		public static function isLevel( value:* ):Level {
			value = ResolveAs( value );
			return ( value.label != Level.OFF.label ) ? value : null;
		}
		
		private static function ResolveAs( value:* ):Level {
			
			if( value is String || value is int ){
				
				var level:Level;
				var list:Array = [ "ALL", "DEBUG", "INFO", "WARN", "ERROR", "CRITICAL", "FATAL" ];
				
				while( list.length ){
					
					level = Level[ String( list.shift() ) ];				
					
					if( value is String && level.label == value || value is int && level.id == value ){
						return level;
					}
					
				}
				
			}			
			
			return Level.OFF;
			
		} 	
		
		public function toString():String {
			var result:String = new String( "[Level id=\"{1}\" label=\"{2}\"]" );
			return StringUtil.substitute( result, this.id, this.label );
		}
		
	}
	
}