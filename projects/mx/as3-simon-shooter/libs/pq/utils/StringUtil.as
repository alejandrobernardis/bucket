
package pq.utils {
	
	import pq.core.CoreStatic;	
	
	public final class StringUtil extends CoreStatic {
		
		public static function evalToNull( value:String ):String {
			return ( isEmpty(value) ) ? null : value;
		}
		
		public static function isEmpty( value:String ):Boolean {
			value = stripWhiteSpace( value );
			if ( value == null || ! ( value is String ) || value.search( /.+/i ) == -1 ) {
				return true;
			} else {
				return false;
			}			
		}
		
		public static function multiply( value:String, quantity:int ):String {
			var result:String = new String();
			while( quantity-- ) result += value;
			return result;
		}
		
		public static function hasWhiteSpace( value:String ):Boolean {
			return value.search( /\s/ig ) > -1;
		}
		
		public static function stripWhiteSpace( value:String ):String {
			return value.replace( /\s/ig, "" );
		}
		
		public static function substitute( value:String, ...rest ):String {
			
			var argDat:Array = rest;
			
			if ( rest[ 0 ] is Array && rest.length == 1 ) {
				argDat = rest[ 0 ];			
			}
			
			for( var a:int = 0; a < argDat.length; a++ ) {
				value = value.replace( "{"+(a+1)+"}", argDat[ a ] );
			}
			
			return value;
			
		}

	}
	
}