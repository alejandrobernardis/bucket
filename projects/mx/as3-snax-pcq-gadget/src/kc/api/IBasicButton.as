
package kc.api {

	public interface IBasicButton extends IKCComponent, IUIElement {
		
		// @properties (rw)
		
		function set label( value:String ):void;
		function get label():String;
		function get tweening():Boolean;
		function set tweening( value:Boolean ):void;
			
	}
	
}