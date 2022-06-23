
package pq.api {
	
	import flash.display.DisplayObject;
	import flash.display.DisplayObjectContainer;
	import flash.display.Sprite;
	import flash.display.Stage;
	import flash.events.IEventDispatcher;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.media.SoundTransform;
	
	public interface IUIComponent extends IEventDispatcher, IAlign, IData, IPurger, IScale {
		
		/**
		 * Identificador Unico del Componente. UID Class.
		 */
		function get uid():String;
		
		/**
		 * Disponibilidad del Componente.
		 */
		function get enabled():Boolean;
		function set enabled( value:Boolean ):void;
		
		/**
		 * Objeto creador o contenedor (parent) del Componente.
		 */
		function get owner():DisplayObject;
		function set owner( value:DisplayObject ):void;
		
		/**
		 * Valida si el elemento existe dentro del componente.
		 */
		function isChild( value:String ):Boolean;
		
		
		/**
		 * @IMovieClip 
		 */
		
		function get alpha ():Number;
		function set alpha (value:Number):void;
		function get height ():Number;
		function set height (value:Number):void;
		function get mask ():DisplayObject;
		function set mask (value:DisplayObject):void;
		function get mouseX ():Number;
		function get mouseY ():Number;
		function get name ():String;
		function set name (value:String):void;
		function get parent ():DisplayObjectContainer;
		function get root ():DisplayObject;
		function get rotation ():Number;
		function set rotation (value:Number):void;
		function get scaleX ():Number;
		function set scaleX (value:Number):void;
		function get scaleY ():Number;
		function set scaleY (value:Number):void;
		function get stage ():Stage;
		function get width ():Number;
		function set width (value:Number):void;
		function get visible ():Boolean;
		function set visible (value:Boolean):void;
		function get x ():Number;
		function set x (value:Number):void;
		function get y ():Number;
		function set y (value:Number):void;
		
		function get doubleClickEnabled ():Boolean;
		function set doubleClickEnabled (enabled:Boolean):void;
		function get focusRect ():Object;
		function set focusRect (focusRect:Object):void;
		
		
		
		function get tabEnabled ():Boolean;
		function set tabEnabled (enabled:Boolean):void;
		function get tabIndex ():int;
		function set tabIndex (index:int):void;
		
		
		
		function get tabChildren ():Boolean;
		function set tabChildren (enable:Boolean):void;
		function get dropTarget ():DisplayObject;
		
		function get soundTransform ():SoundTransform;
		function set soundTransform (sndTransform:SoundTransform):void;
		
		function getBounds (targetCoordinateSpace:DisplayObject):Rectangle;
		function getRect (targetCoordinateSpace:DisplayObject):Rectangle;
		function globalToLocal (point:Point):Point;
		function hitTestObject (obj:DisplayObject):Boolean;
		function hitTestPoint (x:Number, y:Number, shapeFlag:Boolean = false):Boolean;
		function localToGlobal (point:Point):Point;
		function addChild (child:DisplayObject):DisplayObject;
		function getChildAt (index:int):DisplayObject;
		function getChildByName (name:String):DisplayObject;
		function getChildIndex (child:DisplayObject):int;
		function removeChild (child:DisplayObject):DisplayObject;
		function removeChildAt (index:int):DisplayObject;
		function setChildIndex (child:DisplayObject, index:int):void;
		function swapChildren (child1:DisplayObject, child2:DisplayObject):void;
		function swapChildrenAt (index1:int, index2:int):void;
		function startDrag (lockCenter:Boolean = false, bounds:Rectangle = null):void;
		function stopDrag ():void;
		
	}
	
}