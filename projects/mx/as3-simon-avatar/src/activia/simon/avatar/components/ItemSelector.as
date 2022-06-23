package activia.simon.avatar.components{
	import flash.display.Bitmap;
	import kc.core.KCComponent;

	import flash.display.DisplayObject;
	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;

	/**
	 * @author bernardisa
	 */
	public class ItemSelector extends KCComponent{

		private var _container:Sprite;
		private var _mask:Shape;

		public function ItemSelector(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		override public function purge(...rest):void{
			while(_container.numChildren) _container.removeChildAt(0);
			while(numChildren) removeChildAt(0);
			_container = null;
			_mask = null;
			super.purge(rest);
		}

		override protected function $config(e:Event):void{
			super.$config(e);
			_container = new Sprite();
			_container.x = 0;
			_container.y = 0;
			super.addChild(_container);
			_mask = new Shape();
			_mask.graphics.beginFill(0x00ff00, 1);
			_mask.graphics.drawRect(0, 0, 120, 120);
			_mask.graphics.endFill();
			_mask.x = 0;
			_mask.y = 0;
			super.addChild(_mask);
			_container.mask = _mask;
		}

		override public function addChild(child:DisplayObject):DisplayObject{
			if(!_container || !child) return null;
			while(_container.numChildren) _container.removeChildAt(0);
			if(child is Bitmap) child = new Bitmap(Bitmap(child).bitmapData);
			if(child.width > 120 && child.width > child.height){
				child.height = (child.height * 100) / child.width;
				child.width = 100;
			} else if(child.height > 120){
				child.width = (child.width * 100) / child.height;
				child.height = 100;
			}
			child.x = (this.width - child.width) / 2;
			child.y = (this.height - child.height) / 2;
			_container.addChild(child);
			return this;
		}
	}
}
