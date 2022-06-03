
package pq.utils {
	
	import com.emc2zen.core.CoreStatic;
	
	public class Hasher extends CoreStatic {
		
		private static const encodingID:String 	= "I";
		private static const encodingKey:String = "9B3B6EDFBFC34F98B94A305D2ED7C308";
		
		public function Hasher() {
			super();
		}
		
		public static function encode( theString : String ) : String {
			
			var theResult : String = "";
			var iKey : int = 0;
			var i : int;
			
			for (i = 0; i < theString.length; ++i ) {
				
				var theNumber : int = theString.charCodeAt(i) ^ encodingKey.charCodeAt(iKey);
				var xored : String = theNumber.toString();
				
				if (theNumber < 10) {
					xored = "00" + xored;
				}else if (theNumber < 100){
					xored = "0" + xored;
				}
				
				theResult = theResult + xored;
					
				if(iKey == encodingKey.length-1){
					iKey = 0;
				}else{
					iKey++;
				}
				
			}
			
			return (encodingID + theResult);
			
		}
		
		public static function decode( theString : String ) : String {
			
			var i:int;
			var iKey:int = 0;
			var coef:uint = 3;
			var str:String = theString.substring( 1 );
			var result:String = new String("");
			
			for ( var a:uint = 0; a < ( str.length / coef ); a++ ) {
				
				var pos:uint = a * coef;
				var xored:String = str.substring( pos, pos + coef );				
				result = result + String.fromCharCode( int( xored ) ^ encodingKey.charCodeAt(iKey) );
				
				if(iKey == encodingKey.length-1){
					iKey = 0;
				}else{
					iKey++;
				}
				
			}
			
			return result;
			
		}
		
	}

}