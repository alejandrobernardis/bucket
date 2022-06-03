
package kc.utils {
	import kc.core.KCStatic;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class NumberUtil extends KCStatic {
		
		// @const
		
		private static const MIN_LISTED_VALUE:Number = 0;
		private static const MAX_LISTED_VALUE:Number = 64;

		// @constructor
		
		public function NumberUtil() {
			super();
		}
		
		// @methods
		
		public static function addLeadingZero( value:Number ):String {
			
			return ( value > -1 && value < 10 )
				? "0" + value.toString()
				: value.toString();
				
		}

		public static function isModule( value:Number, module:Number ):Boolean {
			return ( ( value % module ) == 0 );
		}
		
		public static function module( value:Number, module:Number ):Number {
			if( isModule( value, module ) )
				return value;
			else if( value < module )
				return module;
			else
				return Math.ceil(value/module)*module;
		}
		
		public static function limits( value:Number, min:Number, max:Number, def:Number = 0 ):Number {
			return Math.min( max, Math.max( min, value ) ) || def;
		}
		
		public static function percentage( value:Number, percentage:Number ):Number {
			return ( ( percentage * value ) / 100 );
		}
		
		public static function fixed( value:Number, decimals:Number = 2 ):Number {
			
			var pow:Number = Math.pow( 10, Math.round( decimals ) );
			return Math.round( value * pow ) / pow;
			
		}
		
		public static function hex( value:Number, prefix:String = null ):String {
			
			var result:String = value.toString( 16 );
			
			if( value < 16 ) 
				result = "0" + result;
			
			return String( ( prefix || "" ) + result );
			
		}
		
		public static function listed( min:Number = NaN, max:Number = NaN ):Array {
			
			var vmin:Number = Math.min( min, max ) || MIN_LISTED_VALUE;
			
			var vmax:Number = ( ( ! isNaN(min) ) 
				? Math.max( min, max ) 
				: max 
			) || MAX_LISTED_VALUE;
			
			var list:Array = new Array();
			
			while( vmin <= vmax ){
				list.push( vmin++ );
			}
			
			return list;
			
		}
		
		public static function uniqueRandom( min:Number = NaN, max:Number = NaN ):Array {
			
			var list:Array = new Array();
			var positions:Array = listed( min, max );
			
			var vLength:Number = positions.length;
			var vPosition:Number;
			
			for( var a:uint = 0; a < vLength; a++ ){
				vPosition = Math.floor( Math.random() * ( vLength - a ) );
				list.push( positions[ vPosition ] );
				positions.splice( vPosition, 1 );
			}
			
			return list;
			
		}
		
	}
	
}
