package activia.simon.avatar{
	import kc.api.IBasicButton;
	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;
	import kc.utils.StringUtil;

	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.text.TextField;

	/**
	 * @author bernardisa
	 */
	public class Step1Screen extends BaseScreen{

		private var _data_sex:XML;
		private var _error_text:String;

		public function Step1Screen(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		override protected function $config(e:Event):void{
			super.$config(e);
			KCDataLayer.scope.content.menu.user_name = null;

			// user name
			tx_user_name.addEventListener(Event.CHANGE, onNameChange);
			tx_user_name.text = user_name();

			// user sex and skin
			var item:IBasicButton;
			var item_name:String;
			var sex:String = user_sex();
			var sex_value:String = "Sex" + StringUtil.ucFirstChar(sex) + "Button";
			var skin:int = user_skin();
			var skin_value:String = "Skin0" + StringUtil.ucFirstChar(skin.toString()) + "Button";

			for(var a:int = 0; a < numChildren; a++){
				if(getChildAt(a) is IBasicButton){
					item = getChildAt(a) as IBasicButton;
					item_name = ClassUtil.shortName(item);
					if((!StringUtil.isEmpty(sex) && item_name == sex_value) || (skin > 0 && item_name == skin_value)){
						item.enabled = false;
					} else{
						item.enabled = true;
					}
				}
			}

			tx_error.text = "";
			
			_data_sex = KCDataLayer.collection.value("applicationAssets") as XML;
			_error_text = null;
		}

		private function set_button(prefix:String, value:String):void{
			var item:*;
			var item_name:String;
			for(var a:int = 0; a < numChildren; a++){
				item = getChildAt(a);
				item_name = ClassUtil.shortName(item);
				if(item_name.indexOf(prefix) > -1){
					item.enabled = !(item is IBasicButton && item_name == value);
				}
			}
		}

		override public function purge(...rest):void{
			try{
				_data_sex = null;
				_error_text = null;
				tx_user_name.removeEventListener(Event.CHANGE, onNameChange);
			}catch(e:*){}
			super.purge(rest);
		}

		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "SexMaleButton":
				case "SexFemaleButton":
					set_button("Sex", name);
					user_sex(name.replace(/sex|button/gi, "").toLowerCase());
					break;
				case "Skin01Button":
				case "Skin02Button":
				case "Skin03Button":
				case "Skin04Button":
					set_button("Skin", name);
					user_skin(int(name.replace(/skin|button|0/gi, "")));
					break;
				case "PrevButton":
					KCDataLayer.scope.content.cScreen("home");
					break;
				case "NextButton":
					if(validate_status()){
						KCDataLayer.scope.content.cScreen("step2");
					}else{
						tx_error.text = _error_text;
					}
					break;
			}
		}
		
		override public function validate_status():Boolean{
			if(validate_step()){
				return true;
			} tx_error.text = _error_text;
			return false;
		}

		private function validate_step():Boolean{
			_error_text = null;
			if(StringUtil.isEmpty(user_name())){
				_error_text = "¡Ups! ¡Olvidaste escribir tu nombre!";
			} else  if(StringUtil.isEmpty(user_sex())){
				_error_text = "¿Eres niño o niña?";
			} else if(user_skin() < 1){
				_error_text = "¿Cual es tu color de piel?";
			}
			return (!_error_text);
		}

		public function get tx_error():TextField{
			return getTextField("txError");
		}

		public function get tx_user_name():TextField{
			return getTextField("txName");
		}

		public function user_name(value:String = null):String{
			if(value)
				KCDataLayer.collection.update("AVATAR_NAME", value);
			return KCDataLayer.collection.value("AVATAR_NAME");
		}

		public function user_sex(value:String = null):String{
			if(value){
				ApplicationContent.reset_avatar_config();
				KCDataLayer.collection.update("AVATAR_SEX", value);
				KCDataLayer.collection.update("AVATAR_DATA_LOAD", 
					new XML(_data_sex.assets.(@sex==value).toXMLString()));
			} return KCDataLayer.collection.value("AVATAR_SEX");
		}

		public function user_skin(value:int = -1):int{
			if(value > -1)
				KCDataLayer.collection.update("AVATAR_SKIN", value);
			return KCDataLayer.collection.value("AVATAR_SKIN");
		}

		private function onNameChange(e:Event):void{
			user_name(tx_user_name.text);
		}
	}
}
