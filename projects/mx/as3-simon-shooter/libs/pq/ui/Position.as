
package pq.ui {
	
	import pq.utils.StringUtil;
	
	public class Position extends Object {
		
		private var _x:Number;
		private var _y:Number;
		
		public function Position( value:String = null ) {
			if ( value != null ) {
				var result:Array = value.split( " " );
				this._x = ResolveValue( result[0] );
				this._y = ResolveValue( result[1] ) || this._x;
			}
		}
		
		private function ResolveValue( value:* = null ):Number {
			if ( value == null || value.search( /^([\-\+]?\d*[\.]?\d*|[\.]\d*)$/ ) == -1 ) return NaN;
			return Number( value );
		}
		
		public function get x():Number { 
			return this._x; 
		}
		
		public function set x( value:Number ):void {
			this._x = value;
		}
		
		public function get y():Number { 
			return this._y; 
		}
		
		public function set y( value:Number ):void {
			this._y = value;
		}
		
		public function toString():String {
			var pattern:String = "[Position x=\"{1}\" y=\"{2}\"]";
			return StringUtil.substitute( pattern, this.x, this.y );
		}
		
	}
	
}