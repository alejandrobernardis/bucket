
package kc.core {
	import kc.api.IPurger;
	import kc.utils.ClassUtil;
	import kc.utils.PurgerUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCClassFactory extends Object implements IPurger {

		// @variables
		
		protected var _value:*;
		protected var _properties:Object;
		
		// @constructor

		public function KCClassFactory( value:* ) {
			super();
			_value = value;
		}
		
		// @properties (r)
		
		public function get properties():Object {
			return _properties;
		}

		// @methods
		
		public function newInstance( properties:Object = null ):* {
			var instance:* = new _value();
			var data:Array = ClassUtil.writablePropertiesList( _value );
			if( properties != null ){
				_properties = properties;
				for( var key:String in _properties ){
					if( data.indexOf( key ) != -1 ){
						instance[key] = _properties[key];
					}
				}
			} PurgerUtil.cleanCollection( data ); 
			return instance;
		}
		
		// @purge
		
		public function purge(...rest):void {
			PurgerUtil.cleanCollection( _properties );
			_value = null;
			_properties = null;
		}
		
	}
	
}
