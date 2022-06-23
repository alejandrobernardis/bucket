
package kc.utils {
	import kc.core.KCStatic;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class StringUtil extends KCStatic {

		// @const
		
		public static const EMPTY:String = "";
		public static const WHITE_SPACE:String = " ";
		public static const WHITE_SPACE_INTEGER:int = 32;
		
		private static const NOT_FOUND:int = -1;
		
		// @constructor
		
		public function StringUtil() {
			super();
		}
		
		// @validate
		
		public static function isEmail( value:String ):Boolean {
			if( isEmpty(value) ){
				return false;
			} return ( value.search( RegExpUtil.PATTERN_EMAIL ) != -1 );
		}
		
		public static function isEmpty( value:String ):Boolean {
			if( value ){
				value = value.replace( RegExpUtil.PATTERN_WHITE_SPACE, EMPTY );
				return ( value.search( RegExpUtil.PATTERN_LITERAL ) == NOT_FOUND );
			} return true;
		}
		
		public static function valueCase( value:String ):int {
			if( ! isEmpty( value ) ){
				return ( value == value.toUpperCase() )
					? 1
					: 0;
			} return NOT_FOUND;
		}

		// @manipulate
		
		public static function multiply( value:String, quantity:int ):String {
			if( quantity == 0 ) return EMPTY;
			var result:String = new String();
			while( quantity-- ) result += value;
			return result; 
		}
		
		public static function substitute( value:String, ...rest ):String {
			
			if( isEmpty(value) ){
				return EMPTY;	
			} 
			
			rest = ArrayUtil.discriminateArgument( rest );
			
			for( var a:uint = 1; a <= rest.length; a++ ){
				value = value.replace(
					new RegExp( "\\{" + a + "\\}",  "g" ),
					rest[a-1] 
				);
			}
			
			return value;
			
		}
		
		// @whiteSpace
		
		public static function stripWhiteSpace( value:String ):String {
			if( isEmpty(value) ){
				return EMPTY;	
			} return value.replace( RegExpUtil.PATTERN_WHITE_SPACE, EMPTY );
		}
		
		public static function isWhiteSpace( value:String ):Boolean {
			if( isEmpty(value) ){
				return true;	
			} return ( value.search( RegExpUtil.PATTERN_WHITE_SPACE ) > NOT_FOUND );	
		}
		
		public static function hasWhiteSpace( value:String ):Boolean {
			if( isEmpty(value) ){
				return false;	
			} return ( value.search( RegExpUtil.PATTERN_WHITE_SPACE ) > NOT_FOUND );
		}
		
		// @trim
		
		public static function ltrim( value:String ):String {
			if( isEmpty(value) ){
				return EMPTY;	
			} return value.replace( RegExpUtil.PATTERN_WHITE_SPACE_LEFT, EMPTY );			
		}  
		
		public static function rtrim( value:String ):String {
			if( isEmpty(value) ){
				return EMPTY;	
			} return value.replace( RegExpUtil.PATTERN_WHITE_SPACE_RIGHT, EMPTY );
		}
		
		public static function trim( value:String ):String {
			return rtrim( ltrim( value ) );		
		}
		
		// @capitalize/uncapitalize
		
		public static function lcFirstChar( value:String ):String {
			if( isEmpty(value) ){
				return EMPTY;	
			} return new String( value.substr( 0, 1 ).toLowerCase() + value.substr( 1 ) );
		}   
		
		public static function ucFirstChar( value:String ):String {
			if( isEmpty(value) ){
				return EMPTY;	
			} return new String( value.substr( 0, 1 ).toUpperCase() + value.substr( 1 ) );
		}
		
		public static function capitalize( value:String ):String {
			return ResolveCapitalize( value );
		} 
		
		public static function unCapitalize( value:String ):String {
			return ResolveCapitalize( value, true );
		}
		
		private static function ResolveCapitalize( value:String, lower:Boolean = false ):String {
			
			if( isEmpty(value) ){
				return EMPTY;	
			} 
			
			var list:Array = value.split( WHITE_SPACE );
			value = "";
			
			for ( var a:int = 0; a < list.length; a++) {
				value += ( 
					( ! lower ) 
						? ucFirstChar( list[a] )
						: lcFirstChar( list[a] ) 
				) + WHITE_SPACE;
			}
			
			return trim( value );
			
		}
		
	}
	
}        