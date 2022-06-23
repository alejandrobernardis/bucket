
package activia.simon.shooter.ui.actors {
	
	public class ActorsQueue extends Object {
		
		protected var _records:Array;
		private var _capacity:int;
		
		public function ActorsQueue( capacity:int = 0 ) {
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
		
		public function contains( value:Actor ):Boolean {
			return new Boolean( _records.indexOf( value ) != -1 );	
		}
		
		public function dequeue():Actor {
			if ( isEmpty() ) return null;
			return _records.shift();
		}
		
		public function element():Actor {
			return _records[0];
		}
		
		public function enqueue( value:Actor ):Boolean {
			if ( availableCapacity() == 0 ) return false; 
			return _records.push( value ) > 0;
		}
		
		public function isEmpty():Boolean {
			return new Boolean( size() < 1 );
		}
		
		public function remove( value:Actor ):Actor {
			
			if ( isEmpty() ) return null;
			
			var i:int;
			var pos:uint;
			
			for ( i = 0; i < size(); i ++ ) {
				if ( value.uid === Actor( _records[i] ).uid ) {
					pos = i; 
					break;
				}
			}
			
			return _records.splice( pos, 1 );			
			
		}
		
		public function toArray():Array {
			return _records.slice();
		}
		
		public function size():int {
			return _records.length;
		}
		
		public function purge():void {
			this._capacity = undefined;
			this._records = null;
		}
		
	}

}