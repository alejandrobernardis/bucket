
package kc.data {
	import kc.utils.ClassUtil;
	import kc.utils.StringUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class Record extends Object {

		// @variables
		
		protected var _key:String;
		protected var _value:*;

		// @constructor

		public function Record( key:String, value:* ) {
			_key = key;
			_value = value;
		}
		
		// @properties (r)
		
		public function get key():String {
			return _key;
		}
		
		public function get value():* {
			return _value;
		}
		
		// @toString
		
		public function toString():String {
			
			var pattern:String = "[{1} key=\"{2}\" value=\"{3}\"]";
			
			return StringUtil.substitute( 
				pattern, 
				ClassUtil.shortName(this), 
				_key, 
				_value 
			);
			
		}
		
	}
	
}
