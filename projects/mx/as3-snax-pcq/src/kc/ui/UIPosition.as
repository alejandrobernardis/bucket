
package kc.ui {
	import kc.api.IPosition;
	import kc.utils.StringUtil;

	public class UIPosition extends Object implements IPosition {
		
		// @const
		
		// -.01 +10...
		public static const PATTERN_POSITION_STRING:RegExp = /^([\-\+]?\d*[\.]?\d*|[\.]\d*)$/;
		
		// @private
		
		private var _x:Number;
		private var _y:Number;
		
		// @constructor
		
		public function UIPosition( value:String = null ) {
			if ( value != null ) {
				var result:Array = value.split( " " );
				_x = ResolveValue( result[0] );
				_y = ResolveValue( result[1] ) || _x;
			}
		}
		
		// @properties (rw)
		
		public function get x():Number { 
			return _x; 
		}
		
		public function set x( value:Number ):void {
			_x = value;
		}
		
		public function get y():Number { 
			return _y; 
		}
		
		public function set y( value:Number ):void {
			_y = value;
		}
		
		// @methods
		
		public function position( x:Number, y:Number = NaN ):void {
			_x = x;
			_y = y || _x;
		}
		
		// @toString
		
		public function toString():String {
			var pattern:String = "[UIPosition x=\"{1}\" y=\"{2}\"]";
			return StringUtil.substitute( pattern, _x, _y );
		}
		
		// @helpers
		
		protected function ResolveValue( value:* = null ):Number {
			return ( value == null || value.search( PATTERN_POSITION_STRING ) == -1 )
				? NaN 
				: Number( value );
		}
		
	}   
	
}
