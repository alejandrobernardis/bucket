
package activia.simon.shooter.ui {
	
	public class ScreensStack extends Object {
		
		protected var _records:Array;
		private var _capacity:int;
		
		public function ScreensStack( capacity:int = 0 ) {
			_capacity = capacity;
			clear();		
		}
		
		public function availableCapacity():int {
			return new int( capacity() - size() );
		}
		
		public function capacity():int {
			return _capacity;
		}
		
		public function clear():void {
			_records = new Array();
		}
		
		public function contains( value:* ):Boolean {
			return new Boolean( _records.indexOf( value ) != -1 );	
		}
		
		public function isEmpty():Boolean {
			return new Boolean( size() < 1 );
		}
		
		public function peek():* {
			return _records[ 1 ];
		}
		
		public function pop():* {
			if( ! isEmpty() ) return _records.shift();
			return null;
		}
		
		public function push( value:* ):void {
			if( size() < capacity() ) _records.unshift( value );
		}
		
		public function search( value:* ):* {
			if( ! isEmpty() ) return _records.indexOf( value );
			return null;
		}
		
		public function size():int {
			return _records.length;
		}
		
		public function toArray():Array {
			return _records.slice();
		}
		
		public function top():* {
			return _records[0];
		}	
		
		public function purge():void {
			this._capacity = undefined;
			this._records = null;
		}
		
	}
	
}