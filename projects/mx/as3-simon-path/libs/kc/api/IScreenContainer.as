
package kc.api {

	public interface IScreenContainer extends IKCComponent, IUIElement {
	
		// @properties (r)
		
		function get content():IScreen;
		function get screens():IStack;
		function get capacity():uint;
		function get availableCapacity():uint;
		function get quantity():uint;
		
		// @methods
		
		function add( value:IScreen, properties:Object = null ):void;
		function replace( value:IScreen, properties:Object = null ):void;
		function remove():void;
		function clear():void;
		
	}
	
}
