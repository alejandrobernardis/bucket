
package kc.api {
	import kc.api.flash.ISprite;

	import flash.system.LoaderContext;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IApplication extends ISprite {
		
		function get content():ApplicationContent;
		function get context():LoaderContext;
		
	}
	
}
