
package kc.utils {
	import kc.core.KCStatic;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class ArrayUtil extends KCStatic {

		// @const

		private static const NOT_FOUND:int = -1;

		// @constructor

		public function ArrayUtil() {
			super();
		}

		// @methods

		public static function toArray( value:Object, record:int = 1 ):Array {

			var result:Array = new Array();

			if ( ! value ) {
				return result;
			}else if ( value is Array ) {
				return value as Array;
			}

			for ( var key:* in value ) {
				switch( record ) {
					case -1:
						result.push( key );
						break;
					case 0:
						result.push( [ key, value[key] ] );
						break;
					case 1:
						result.push( value[key] );
						break;
				}
			}

			return result;

		}

		public static function getItemIndex( value:Object, source:Array ):int {
			for ( var a:int = 0; a < source.length; a++ ) {
				if ( source[a] === value )
					return a;
			} return NOT_FOUND;
		}

		public static function discriminateByType( value:*, source:Array ):Array {
			var result:Array = new Array();
			for ( var a:int = 0; a < source.length; a++ ) {
				if ( source[a] is value )
					result.push( source[a] );
			} return result;
		}

		public static function discriminateArgument( value:Array ):Array {
			if( ! value )
				return new Array();
			else if( value.length == 1 && value[0] is Array )
				return value[0] || new Array();
			return value;
		}

		public static function discriminateArgumentByType( value:*, source:Array ):Array {
			return discriminateByType( value, discriminateArgument( source ) );
		}

		public static function x2a(value:XML):Array {

			var arr:Array = [];
			var idx:int = 0;

			var val2:int = value.attributes().length();

			for (var j:int = 0; j < val2; j++){
				value.attributes()[j];
				arr[idx++] = value.attributes()[j].toString();
			}

			var val:int = value.elements().length();

			for (var i:int = 0; i < val; i++){
				arr[idx++] = x2a(value.elements()[i]);
			}

			return arr;

		}

	}

}
