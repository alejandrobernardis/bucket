package kc.ui {
	import kc.api.IKCComponent;
	import kc.api.IUIElement;
	import kc.core.KCComponent;

	import flash.display.DisplayObject;
	import flash.display.Stage;
	import flash.geom.Rectangle;

	public class UIElement extends KCComponent implements IUIElement, IKCComponent {
		
		// @protected
		
		protected var _UIElement:Boolean;
		protected var _UIRectangle:Rectangle;
		
		// @constructor
		
		public function UIElement(data:XML = null, autorelease:Boolean = true) {
			super( data, autorelease );
		}
		
		// @override
		
		override public function purge(...rest):void {
			_UIElement = undefined;
			_UIRectangle = null;
			super.purge();
		}

		// @methods
		
		public function isUIElement():Boolean {
			return _UIElement;
		}
		
		public function getUIRectangle():Rectangle {
			return _UIRectangle;	
		}
		
		public function setUIRectangle( ...rest ):void {
			
			if( ! rest.length ){ 
				return;
			}else if( rest[0] is Rectangle ) { 
				_UIRectangle = rest[0];	
			}else if( rest[0] is Stage ) {
				 _UIRectangle = new Rectangle(
					0, 0,
					stage.stageWidth,
					stage.stageHeight
				);			}else if( rest[0] is DisplayObject ) { 
				_UIRectangle = new Rectangle(
					0, 0,
					rest[0].width,
					rest[0].height
				);						
			}else if( rest[0] is Number ) {
				_UIRectangle = new Rectangle(
					rest[0] || 0,
					rest[1] || 0,
					rest[2] || 0,
					rest[3] || 0
				);
			}
			
		}
		
	}
	
}
