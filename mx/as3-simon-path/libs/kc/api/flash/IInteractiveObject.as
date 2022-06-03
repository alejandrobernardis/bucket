
package kc.api.flash {
	
	public interface IInteractiveObject extends IDisplayObject {
	
		function get tabEnabled():Boolean;
		function set tabEnabled(enabled:Boolean):void;
		function get tabIndex():int;
		function set tabIndex(index:int):void;
		function get focusRect():Object; 
		function set focusRect(focusRect:Object):void;
		function get mouseEnabled():Boolean;
		function set mouseEnabled(enabled:Boolean):void;
		function get doubleClickEnabled():Boolean;
		function set doubleClickEnabled(enabled:Boolean):void;
	
	}
	
}
