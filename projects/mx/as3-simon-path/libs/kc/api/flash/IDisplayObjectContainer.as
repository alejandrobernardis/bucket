
package kc.api.flash {
	import flash.display.DisplayObject;
	import flash.geom.Point;
	import flash.text.TextSnapshot;

	public interface IDisplayObjectContainer extends IInteractiveObject {
		
		function get numChildren():int;
		function get textSnapshot():TextSnapshot;
		function get tabChildren():Boolean;
		function set tabChildren(enable:Boolean):void;
		function get mouseChildren():Boolean;
		function set mouseChildren(enable:Boolean):void;
		function addChild(child:DisplayObject):DisplayObject;
		function addChildAt(child:DisplayObject, index:int):DisplayObject;
		function removeChild(child:DisplayObject):DisplayObject;
		function removeChildAt(index:int):DisplayObject;
		function getChildIndex(child:DisplayObject):int;
		function setChildIndex(child:DisplayObject, index:int):void;
		function getChildAt(index:int):DisplayObject;
		function getChildByName(name:String):DisplayObject;
		function getObjectsUnderPoint(point:Point):Array;
		function areInaccessibleObjectsUnderPoint(point:Point):Boolean;
		function contains(child:DisplayObject):Boolean;
		function swapChildrenAt(index1:int, index2:int):void;
		function swapChildren(child1:DisplayObject, child2:DisplayObject):void;
		
	}
	
}
