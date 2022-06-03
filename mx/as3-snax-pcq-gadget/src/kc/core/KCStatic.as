
package kc.core {
	import kc.utils.ExceptionUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCStatic extends Object {

		// @errors
		
		public static const ERROR:String = "Illegal instantiation attempted on class of static type.";
		
		// @constructor

		public function KCStatic( catchException:Boolean = false ) {
			super();
			ExceptionUtil.ViewError( ERROR, catchException );
		}
		
	}
	
}
