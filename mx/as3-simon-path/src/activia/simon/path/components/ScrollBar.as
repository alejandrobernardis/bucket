package activia.simon.path.components{
	import caurina.transitions.Tweener;

	import kc.core.KCComponent;

	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Rectangle;



	/**
	 * @author Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
	 */
	public class ScrollBar extends KCComponent {
		private var sd:Number;
		private var sr:Number;
		private var cd:Number;
		private var cr:Number;
		private var new_y:Number;
		private var _ref:Sprite;
		private var _ref_y:int;
		private var _ref_mask:Shape;
		private var _ref_height:int;
		private var _friction:uint;
		private var _scroll_bar:Sprite;
		
		public function ScrollBar(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
			
		override public function purge(...rest):void {
			events(false);
			_ref = null;
			_ref_mask = null;
			_scroll_bar = null;
			super.purge(rest);
		}
		
		public function init(o:Sprite, m:Shape, h:int=0, f:uint=0.50):void {
			_ref = o;
			_ref_y = _ref.y;
			_ref_mask = m;
			_ref_height = (h > 0) ? h : _ref_mask.height;
			_friction = f;
			
			x = _ref_mask.width + 8;
			
			if(_ref.height > _ref_height){
				create();
			}
		}

		private function create():void {
			var background:Shape = new Shape();
			background.graphics.beginFill(0x000000, 0.8);
			background.graphics.drawRect(0, 0, 8, _ref_height);
			background.graphics.endFill();
			addChild(background);
			
			sr = _ref_mask.height / _ref.height;
			
			var bar:Shape = new Shape();
			bar.graphics.beginFill(0xFAE815);
			bar.graphics.drawRect(0, 0, 8, _ref_mask.height*sr);
			bar.graphics.endFill();
			
			_scroll_bar = new Sprite();
			_scroll_bar.alpha = 0.8;
			_scroll_bar.addChild(bar);
			addChild(_scroll_bar);
			
			sd = this.height - _scroll_bar.height;
			cd = _ref.height - _ref_mask.height;
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
			new_y = _ref_mask.y + this.y * cr - _scroll_bar.y * cr;
			_ref.y = new_y - _ref.y * _friction;
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
			_scroll_bar.startDrag(false, new Rectangle(_scroll_bar.x, 0, 0, this.height - _scroll_bar.height));
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
