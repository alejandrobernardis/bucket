package yr.mx.snax.pcq.components {
	import flash.geom.Rectangle;
	import kc.api.IBasicButton;
	import kc.api.IKCComponent;
	import kc.core.KCComponent;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;

	public class ControlVolumenSlider extends KCComponent implements IKCComponent {
		
		public function ControlVolumenSlider(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			MouseMoveHandler();
			button_drag.addEventListener(MouseEvent.MOUSE_DOWN, MouseDownHandler);
			button_drag.addEventListener(MouseEvent.MOUSE_UP, MouseUpHandler);
		}		
		
		override public function purge(...rest):void {
			super.purge(rest);
			button_drag.removeEventListener(MouseEvent.MOUSE_DOWN, MouseDownHandler);
			button_drag.removeEventListener(MouseEvent.MOUSE_UP, MouseUpHandler);
		}
		
		override public function set enabled(value:Boolean):void {
			super.enabled = value;
			button_drag.enabled = value;
		}
		
		public function get volumen():Number {
			return (118 * button_drag.x) / 100;
		}
		
		public function set volumen(value:Number):void {
			button_drag.x = (value * 100) / 118;
			mc_bar.width = button_drag.x;
		}

		private function MouseDownHandler(e:MouseEvent):void {
			if(!enabled) return;
			button_drag.startDrag(true, new Rectangle(0,0, 119, 0));
			button_drag.addEventListener(MouseEvent.MOUSE_MOVE, MouseMoveHandler);
		}
		
		private function MouseUpHandler(e:MouseEvent):void {
			if(!enabled) return;
			button_drag.stopDrag();
			button_drag.removeEventListener(MouseEvent.MOUSE_MOVE, MouseMoveHandler);
		}
		
		private function MouseMoveHandler(e:MouseEvent=null):void {
			if(!enabled) return;
			mc_bar.width = button_drag.x;
			dispatchEvent(new Event(Event.CHANGE));
		}
		
		public function get button_drag():IBasicButton {
			return getChildByName("btDrag") as IBasicButton;
		}
		
		public function get mc_bar():MovieClip {
			return getChildByName("mcBar") as MovieClip;
		}
		
	}
	
}
