package activia.simon.path.components{
	import kc.logging.SimpleLog;
	import flash.events.MouseEvent;
	import flash.display.MovieClip;
	import kc.api.IBasicButton;
	import kc.core.KCComponent;
	import kc.loaders.AssetLoader;
	import kc.utils.ClassUtil;
	import kc.utils.StringUtil;

	import flash.display.Sprite;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.SecurityErrorEvent;

	/**
	 * @author bernardisa
	 */
	public class PromptDetail extends KCComponent{
		private var _image:String;
		private var _image_container:Sprite;
		private var _background:PromptDetailBackground;
		private var _button_close:IBasicButton;
		private var _preloader:PreloaderItem;

		public function PromptDetail(data:XML = null, autorelease:Boolean = true){
			_background = new PromptDetailBackground();
			addChild(_background);
			_button_close = ClassUtil.getClassInstance("CloseXButton");
			_button_close.addEventListener(MouseEvent.CLICK, CloseHandler);
			addChild(_button_close as MovieClip);
			super(data, autorelease);
		}
		
		
		override public function purge(...rest):void{
			super.purge(rest);
			_button_close.removeEventListener(MouseEvent.CLICK, CloseHandler);
		}

		private function CloseHandler(event:MouseEvent):void{
			parent.removeChild(this);
			dispatchEvent(new Event(Event.CLOSE));	
		}
			
		override protected function $config(e:Event):void{
			super.$config(e);
			if(x == 0) x = (750-bg_width)/2;
			if(y == 0) y = (550-bg_height)/2;
			_button_close.x = (bg_width - _button_close.width) - 24;
			_button_close.y = 8; 
		}

		public function get image():String{
			return _image;
		}

		public function set image(value:String):void{
			if(!_image_container){
				_image_container = new Sprite();
				addChild(_image_container);
			}

			if(!value || StringUtil.isEmpty(value)){
				while(_image_container.numChildren){
					_image_container.removeChildAt(0);
				}
				value = null;
			}

			_image = value;
			
			if(image){
				var item:AssetLoader = new AssetLoader();
				item.addEventListener(Event.COMPLETE, ImageCompleteHandler);
				item.addEventListener(IOErrorEvent.IO_ERROR, ImageErrorHandler);
				item.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ImageErrorHandler);
				item.load(image);
				
				_preloader = new PreloaderItem();
				_preloader.position(bg_width/2, bg_height/2);
				addChild(_preloader);
				setChildIndex(_preloader, numChildren-1);
			}
		}

		private function ImageClearHandlers(value:AssetLoader):void{
			if(_preloader){
				
				removeChild(_preloader);
				_preloader = null;
			}
			value.removeEventListener(Event.COMPLETE, ImageCompleteHandler);
			value.removeEventListener(IOErrorEvent.IO_ERROR, ImageErrorHandler);
			value.removeEventListener(SecurityErrorEvent.SECURITY_ERROR, ImageErrorHandler);
			value = null;
		}

		private function ImageErrorHandler(event:ErrorEvent):void{
			ImageClearHandlers(event.target as AssetLoader);
		}

		private function ImageCompleteHandler(event:Event):void{
			SimpleLog.dump(event);
			while(_image_container.numChildren){_image_container.removeChildAt(0);}
			_image_container.addChild(event.target.content);
			ImageClearHandlers(event.target as AssetLoader);
			dispatchEvent(new Event(Event.COMPLETE));
			setChildIndex(_image_container, numChildren-1);
		}

		//
		
		private var _bg_width:Number;

		public function set bg_width(value:Number):void{
			_bg_width = value;
			_background.width = value;
		}

		public function get bg_width():Number{
			return _bg_width;
		}

		private var _bg_height:Number;

		public function set bg_height(value:Number):void{
			_bg_height = value;
			_background.height = value;
		}

		public function get bg_height():Number{
			return _bg_height;
		}

	}
}
