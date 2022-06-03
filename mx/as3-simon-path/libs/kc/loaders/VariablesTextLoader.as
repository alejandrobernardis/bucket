
package kc.loaders {
	import kc.api.ILoader;

	import flash.net.URLLoaderDataFormat;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class VariablesTextLoader extends TextLoader implements ILoader {

		// @constructor
		
		public function VariablesTextLoader() {
			super();
		}
		
		// @override
		
		override public function get dataFormat():String {
			return URLLoaderDataFormat.VARIABLES;			
		}
		
	}
	
}
