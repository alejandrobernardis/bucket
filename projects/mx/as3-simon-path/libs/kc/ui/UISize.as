
package kc.ui {
	import kc.utils.StringUtil;
	import kc.api.IResizable;

	public class UISize extends Object implements IResizable {
		
		// @const
		
		// -.01 +10...
		public static const PATTERN_SIZE_STRING:RegExp = /^([\-\+]?\d*[\.]?\d*|[\.]\d*)$/;
		
		// @private
		
		private var _width:Number;
		private var _height:Number;  
		
		// @constructor

		public function UISize( value:String = null ) {
			if ( value != null ) {
				var result:Array = value.split( " " );
				_width = ResolveValue( result[0] );
				_height = ResolveValue( result[1] ) || _width;
			}
		}
		
		// @properties (rw)
		
		public function get width():Number { 
			return _width; 
		}
		
		public function set width( value:Number ):void {
			_width = value;
		}
		
		public function get height():Number { 
			return _height; 
		}
		
		public function set height( value:Number ):void {
			_height = value;
		}
		
		// @method
		
		public function resize( w:Number, h:Number = NaN ):void {
			_width = w;
			_height = h || _width;
		}
		
		// @toString
		
		public function toString():String {
			var pattern:String = "[UISize width=\"{1}\" height=\"{2}\"]";
			return StringUtil.substitute( pattern, _width, _height );
		}
		
		// @helpers
		
		protected function ResolveValue( value:* = null ):Number {
			return ( value == null || value.search( PATTERN_SIZE_STRING ) == -1 )
				? NaN 
				: Number( value );
		}
		
	}
	
}

               