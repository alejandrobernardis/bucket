
package kc.api {
	import kc.api.flash.ISprite;
	import kc.api.flash.IMovieClip;

	import flash.system.LoaderContext;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IApplication extends ISprite {
		
		function get content():IMovieClip;
		function get context():LoaderContext;
		function get flash_vars():Object;
		
		
	}
	
}
