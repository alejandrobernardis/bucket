
package pq.utils {	
	
	import pq.core.CoreStatic;

	public class UID extends CoreStatic {
		
		private static const UID_TEMPLATE:Array = [ 8, 4, 4, 4, 12 ];
		private static const DASH_CHAR_CODE:uint = 45;
		private static const ALPHA_CHAR_CODES:Array = [ 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 65, 66, 67, 68, 69, 70 ];
		
		public static function create( template:Array = null ):String {
			
			var a:uint;
			var b:uint;			
			var index:int = 0;
			var uid:Array = new Array( 36 );
			
			if( template == null ){
				template = UID_TEMPLATE;
			}
			
			for( a = 0; a < template.length; a++ ){
				
				for( b = 0; b < template[ a ]; b++ ){
					uid[ index++ ] = ALPHA_CHAR_CODES[ Math.floor( Math.random() *  16 ) ];
				}
				
				if( a < template.length - 1 ){
					uid[ index++ ] = DASH_CHAR_CODE;
				}
				
			}
			
			return String.fromCharCode.apply( null, uid );
			
		}
		
	}
	
}