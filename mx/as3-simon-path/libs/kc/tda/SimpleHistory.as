
package kc.tda {
	import kc.api.IHistory;
	import kc.tda.SimpleCollection;
	import kc.utils.NumberUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleHistory extends SimpleCollection implements IHistory {
		
		// @protected
		
		protected var _index:int;
		
		// @constructor

		public function SimpleHistory( capacity:int = undefined ) {
			super( capacity );
		}
		
		// @override 
		
		override public function add(value:*):Boolean {
			
			if( _index > 0 ) {
				_records.splice( 0, _index );
			} else if ( availableCapacity == 0 ) {
				_records.pop();
			} _index = 0;
			
			var q:int = size();
			
			if ( value !== _records[_index] ) {				
				_records.unshift( value );				
			} 
			
			return ( q < size() );
			
		}
		
		override public function clear():void {
			_index = 0;
			super.clear();			
		}

		override public function purge(...rest):void {
			_index = undefined;
			super.purge();
		}
		
		 // @poperties (rw)
		
		public function get index():int {
			return ( isEmpty() ) 
				? SimpleCollection.NOT_FOUND
				: ( _index + 1 );
		}

		public function set index(value:int):void {
			_index = NumberUtil.limits( value-1, 0, size()-1, _index );
		}

		// @methods
		
		public function element():*{
			if( isEmpty() ) return null;
			return _records[_index];	
		}
		
		public function back():* {
			if( hasBack() ){
				_index++;
			} return element();
		}
		
		public function forward():* {
			if( hasForward() ){
				_index--;
			} return element();
		}
		
		public function seek(value:int):* {
			index = value;
			return element();
		}
		
		public function seekFirst():* {
			return seek( 0 );
		}
		
		public function seekLast():* {
			return seek( size() - 1 );
		} 
		
		// @helper
		
		public function hasBack():Boolean {
			return ( _index < ( size() - 1 ) );
		}
		
		public function hasForward():Boolean {
			return ( _index > 0 );
		}
		
	}
	
}
