package activia.simon.avatar{
	import kc.api.IBasicButton;
	import kc.api.IKCComponent;
	import kc.api.IScreen;
	import kc.core.KCDataLayer;
	import kc.ui.screens.AbstractScreen;
	import kc.utils.ClassUtil;

	import flash.display.SimpleButton;
	import flash.events.Event;
	import flash.text.TextField;

	/**
	 * @author Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
	 */
	public class BaseScreen extends AbstractScreen implements IScreen{

		protected var _notTracking:Boolean;

		public function BaseScreen(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		override protected function $config(e:Event):void{
			super.$config(e);

			if( _available ){
				init();
				content();
				if(!notTracking){
					GoogleAnalytics.hit(ClassUtil.shortName(this));
				}
			}
		}

		public function get notTracking():Boolean{
			return _notTracking;
		}

		public function set notTracking(value:Boolean):void{
			_notTracking = value;
		}
		
		public function getComponent(value:String):IKCComponent{
			return this.getChildByName(value) as IKCComponent;
		}

		public function getButton(value:String):IBasicButton{
			return this.getChildByName(value) as IBasicButton;
		}

		public function getSButton(value:String):SimpleButton{
			return this.getChildByName(value) as SimpleButton;
		}

		public function getTextField(value:String):TextField{
			return this.getChildByName(value) as TextField;
		}

		public function getFatalError():String{
			return KCDataLayer.collection.value("application").formErrors.common.item.(@id == "fatal").text();
		}
	}
}