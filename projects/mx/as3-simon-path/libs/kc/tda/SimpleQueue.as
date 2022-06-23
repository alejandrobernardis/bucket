
package kc.tda {
	import kc.api.IQueue;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleQueue extends SimpleCollection implements IQueue {

		// @constructor

		public function SimpleQueue( capacity:int = undefined ) {
			super( capacity );
		}
		
		// @override
		
		override public function remove( value:* ):Boolean {
			return ( value != null )
				? super.remove( value )
				: ( dequeue() != null );
		}
		
		// @method
		
		public function element():* {
			if( isEmpty() ) return null;
			return _records[0];
		}
		
		public function peek():* {
			if( isEmpty() ) return null;
			return _records[1];
		}
		
		public function enqueue( value:* ):Boolean {
			return add( value );
		}
		
		public function dequeue():* {
			var q:int = size();
			var value:* = _records.shift();
			return ( q > size() ) 
				? value 
				: null;
		}
		
	}
	
}
