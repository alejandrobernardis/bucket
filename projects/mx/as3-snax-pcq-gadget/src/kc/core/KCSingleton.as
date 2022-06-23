
package kc.core {
	import kc.api.IPurger;
	import kc.utils.ExceptionUtil;
	import kc.utils.StringUtil;

	import flash.utils.Dictionary;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCSingleton extends Object {
		
		// @const
		
		public static const ERROR:String = "Illegal instantiation attempted on class of singleton type.";
		public static const ERROR_NO_RECORDS:String = "No records.";		public static const ERROR_NO_REGISTERED:String = "No class registered for interface: {1}.";
		
		public static const DEFAULT_METHOD:String = "getInstance";
		
		// @variables
			 
		private static var _records:Dictionary;
		protected var _meta_name:String;
		
		// @constructor
		
		public function KCSingleton() {
			super();
			ExceptionUtil.ViewError( ERROR );
		}

		// @methods
		
		public static function setApiClass( api:String, value:Class ):void {
			
			if( ! _records )
				_records = new Dictionary( true );
							
			if( ! KCSingleton.getApiClass( api ) )
				_records[api] = value;
				
		}
		
		public static function getApiClass( api:String ):Class {
			
			if( ! _records )
				ExceptionUtil.ViewError( ERROR_NO_RECORDS );			 
			
			return _records[api];
						
		}
		
		public static function getApiInstance( api:String = null ):* {
			
			var instance:Class = KCSingleton.getApiClass(api);
			
			if( ! instance ){
				return ExceptionUtil.ViewError( 
					StringUtil.substitute( 
						ERROR_NO_REGISTERED,
						api
					)
				);
			} 
			
			return instance[ DEFAULT_METHOD ]();
			
		}
		
		public static function purgeApis(...rest):void {
			
			for( var e:* in _records ){
				if( _records[e] is IPurger )
					_records[e].purge();
				_records[e] = null;
				delete _records[e];
			}
			
			_records = null;
			
		} 
		
	}
	
}
