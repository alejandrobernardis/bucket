
package kc.tda {
	import kc.api.IMap;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleWeakMap extends SimpleMap implements IMap {

		// @constructor

		public function SimpleWeakMap( capacity:int = undefined ) {
			_weakReferences = true;
			super( capacity );
		}
		
	}
	
}
