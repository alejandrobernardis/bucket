
package pq.ui {
	
	import pq.utils.StringUtil;
	
	public class Size extends Object {		
		
		private var _width:Number;
		private var _height:Number;
		
		public function Size( value:String = null ) {
			if ( value != null ) {
				var result:Array = value.split( " " );
				this._width = ResolveValue( result[0] );
				this._height = ResolveValue( result[1] ) || this._width;
			}
		}
		
		private function ResolveValue( value:* = null ):Number {
			if ( value == null || value.search( /^([\-\+]?\d*[\.]?\d*|[\.]\d*)$/ ) == -1 ) return NaN;
			return Number( value );
		}
		
		public function get width():Number { 
			return this._width; 
		}
		
		public function set width( value:Number ):void {
			this._width = value;
		}
		
		public function get height():Number { 
			return this._height; 
		}
		
		public function set height( value:Number ):void {
			this._height = value;
		}
		
		public function toString():String {
			var pattern:String = "[Size width=\"{1}\" height=\"{2}\"]";
			return StringUtil.substitute( pattern, this.width, this.height );
		}
		
	}
	
}