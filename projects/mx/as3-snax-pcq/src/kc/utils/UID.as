
package kc.utils {
	import kc.core.KCStatic;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class UID extends KCStatic {
		
		// @const
		
		private static const CHARS:Array = new Array( 48,49,50,51,52,53,54,55,56,57,65,66,67,68,69,70 );
		private static const SEPARATOR:uint = 45;
		
		// @constructor
		
		public function UID() {
			super();
		}
		
		// @methods
		
		public static function create( template:Array = null ):String {
			
			if( ! template ) 
				template = new Array( 8,4,4,4,12 );
			
			var uid:Array = new Array();
			var last:int = template.length - 1;
			
			for ( var a:uint = 0; a < template.length; a++ ) {
				for ( var b:uint = 0; b < template[a]; b++ )
					uid.push( CHARS[ Math.floor( Math.random() * CHARS.length ) ] );
				if ( a < last )
					uid.push( SEPARATOR ); 
			}
			
			var time:String = String(
				"0000000" + new Date().getTime().toString(16).toUpperCase()
			).substr(
				Math.random() * template[last]
			);
			
			return String( 
				String.fromCharCode.apply( 
					null, 
					uid 
				) 
			).substr( 
				0, 
				-time.length 
			) + time;
					
		}
		
	}
	
}
