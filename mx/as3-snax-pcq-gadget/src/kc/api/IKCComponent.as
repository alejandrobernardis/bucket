
package kc.api {
	import kc.api.flash.IMovieClip;

	import flash.display.DisplayObject;
	import flash.display.DisplayObjectContainer;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IKCComponent extends IData, IMovieClip, IPosition, IPurger, IResizable, IScalable {
		
		// @properties (rw)
		
		function get autorelease():Boolean;
		function set autorelease( value:Boolean ):void;
		function get owner():DisplayObjectContainer;
		function set owner( value:DisplayObjectContainer ):void;
		
		// @properties (r)
		
		function get uid():String;
		
		// @methods
		
		function owns( value:DisplayObject ):Boolean;
		function applyToAllChildren( action:String, ...rest ):void; 
				
	}
	
}
