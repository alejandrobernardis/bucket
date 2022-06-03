package activia.simon.path.components{
	import caurina.transitions.Tweener;

	import kc.core.KCComponent;

	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Rectangle;

	/**
	 * @author bernardisa
	 */
	public class ScrollBarH extends KCComponent{
		
		private var sd:Number;
		private var sr:Number;
		private var cd:Number;
		private var cr:Number;
		private var new_x:Number;
		private var _ref:Sprite;
		private var _ref_x:int;
		private var _ref_mask:Shape;
		private var _ref_width:int;
		private var _friction:uint;
		private var _scroll_bar:Sprite;
		
		public function ScrollBarH(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
			
		override public function purge(...rest):void {
			events(false);
			_ref = null;
			_ref_mask = null;
			_scroll_bar = null;
			super.purge(rest);
		}
		
		public function init(o:Sprite, m:Shape, w:int=0, f:uint=0.50):void {
			_ref = o;
			_ref_x = _ref.x;
			_ref_mask = m;
			_ref_width = (w > 0) ? w : _ref_mask.width;
			_friction = f;
			
			if(_ref.width > _ref_width){
				create();
			}
		}

		private function create():void {
			var background:Shape = new Shape();
			background.graphics.beginFill(0x000000, 0.8);
			background.graphics.drawRect(0, 0, _ref_width, 8);
			background.graphics.endFill();
			addChild(background);
			
			sr = _ref_mask.width / _ref.width;
			
			var bar:Shape = new Shape();
			bar.graphics.beginFill(0xFAE815);
			bar.graphics.drawRect(0, 0, _ref_mask.width*sr, 8);
			bar.graphics.endFill();
			
			_scroll_bar = new Sprite();
			_scroll_bar.alpha = 0.8;
			_scroll_bar.addChild(bar);
			addChild(_scroll_bar);
			
			sd = this.width - _scroll_bar.width;
			cd = _ref.width - _ref_mask.width;
			cr = cd / sd * 1.01;
			
			events();
		}
		
		private function events(add:Boolean=true):void {
			if(!_scroll_bar) return;
			if(add){
				_scroll_bar.addEventListener(MouseEvent.ROLL_OVER, FadeInHandler);
				_scroll_bar.addEventListener(MouseEvent.ROLL_OUT, FadeInHandler);
				_scroll_bar.addEventListener(MouseEvent.MOUSE_DOWN, StartDragHandler);
				_scroll_bar.addEventListener(MouseEvent.MOUSE_UP, StopDragHandler);
				this.addEventListener(Event.ENTER_FRAME, ScrollHandler);
			}else{
				_scroll_bar.removeEventListener(MouseEvent.ROLL_OVER, FadeInHandler);
				_scroll_bar.removeEventListener(MouseEvent.ROLL_OUT, FadeInHandler);
				_scroll_bar.removeEventListener(MouseEvent.MOUSE_DOWN, StartDragHandler);
				_scroll_bar.removeEventListener(MouseEvent.MOUSE_UP, StopDragHandler);
				this.removeEventListener(Event.ENTER_FRAME, ScrollHandler);
			}
		}
		
		private function ScrollHandler(e:Event):void {
			new_x = _ref_mask.x + this.x * cr - _scroll_bar.x * cr;
			_ref.x = new_x - _ref.x * _friction;
		}
		
		private function FadeInHandler(e:Event):void {
			Tweener.addTween(
				e.target,
				{
					alpha: (e.type == "rollOver") ? 1 : 0.8,
					time: 1.5,
					transition: "easeOutQuint"
				}
			);
		}
		
		private function StartDragHandler(e:Event):void {
			_scroll_bar.startDrag(false, new Rectangle(_scroll_bar.x, 0, 0, this.width - _scroll_bar.width));
			StopDragOutSideHandler();
		}
		
		private function StopDragHandler(e:Event):void {
			_scroll_bar.stage.removeEventListener(MouseEvent.MOUSE_UP, StopDragHandler);
			_scroll_bar.stopDrag();
		}
		
		private function StopDragOutSideHandler():void {
			_scroll_bar.stage.addEventListener(MouseEvent.MOUSE_UP, StopDragHandler);
		}
				
	}
	
}
