
package kc.api {

	public interface IScreen extends IKCComponentSteps, IUIElement {
		
		// @prepertie (rw)
		
		function get ignoreUIElements():Boolean;
		function set ignoreUIElements(value:Boolean):void;
		
		// @prepertie (r)
		
		function get isInitialized():Boolean;
		
		// @methods
		
		function init(...rest):void;
		function destroy():void;
		function validate_status():Boolean;		
		
	}
	
}
