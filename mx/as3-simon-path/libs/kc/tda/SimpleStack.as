
package kc.tda {
	import kc.api.IStack;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleStack extends SimpleCollection implements IStack {
		
		// @constructor
		
		public function SimpleStack( capacity:int = undefined ) {
			super( capacity );
			_capacity = capacity;
		}

		// @override
		
		override public function add( value:* ):Boolean {
			return push(value);
		}

		override public function remove( value:* ):Boolean {
			return ( value != null )
				? super.remove( value )
				: ( pop() != null );
		}
		
		// @methods
		
		public function element():* {
			if( isEmpty() ) return null;
			return _records[0];
		}
		
		public function peek():* {
			if( isEmpty() ) return null;
			return _records[1];
		}

		public function push( value:* ):Boolean {
			if( availableCapacity == 0 ) return false;
			var q:int = size();
			return ( q < _records.unshift(value) );
		}
		
		public function pop():* {
			var q:int = size();
			var value:* = _records.shift();
			return ( q > size() ) 
				? value 
				: null;
		}
		
	}
	
}
