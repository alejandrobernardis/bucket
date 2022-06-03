
package kc.data {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class MutableRecord extends Record {

		// @constructor

		public function MutableRecord( key:String, value:* ) {
			super( key, value );
		}
		
		// @properties (w)
		
		public function set key( value:String ):void {
			_key = value;
		}
		
		public function set value( value:* ):void {
			_value = value;
		}
		
	}
	
}
