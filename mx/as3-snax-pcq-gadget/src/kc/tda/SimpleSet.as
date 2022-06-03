
package kc.tda {
	import kc.api.ICollection;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleSet extends SimpleCollection implements ICollection {
	
		// @constructor

		public function SimpleSet( capacity:int = undefined ) {
			super( capacity );
		}
		
		// @override
		
		override public function add( value:* ):Boolean {
			if( contains( value ) ) return false;
			return super.add( value );
		}
		
	}
	
}
