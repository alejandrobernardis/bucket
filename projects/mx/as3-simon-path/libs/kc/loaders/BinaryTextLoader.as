
package kc.loaders {
	import kc.api.ILoader;

	import flash.net.URLLoaderDataFormat;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class BinaryTextLoader extends TextLoader implements ILoader {
		
		// @constructor
		
		public function BinaryTextLoader() {
			super();
		}
		
		// @override
		
		override public function get dataFormat():String {
			return URLLoaderDataFormat.BINARY;			
		}
		
	}
	
}
