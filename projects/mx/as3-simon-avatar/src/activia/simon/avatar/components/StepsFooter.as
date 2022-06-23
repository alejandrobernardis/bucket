package activia.simon.avatar.components{
	import kc.core.KCDataLayer;
	import kc.api.IScreen;
	import kc.api.IBasicButton;
	import kc.core.KCComponent;
	import kc.utils.ClassUtil;

	import flash.events.Event;
	import flash.events.MouseEvent;

	/**
	 * @author bernardisa
	 */
	public class StepsFooter extends KCComponent{

		public function StepsFooter(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		override protected function $config(e:Event):void{
			super.$config(e);
			Helpers.ResolveActions(this, ButtonsManager);
			var own:String = ClassUtil.shortName(this.parent).replace(/[a-z]/gi, "");
			button_step(int(own));
		}

		override public function purge(...rest):void{
			Helpers.ResolveActions(this, ButtonsManager, true);
			super.purge(rest);
		}

		protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			var screen:IScreen = owner as IScreen;
			if(!screen.validate_status()) return;
			switch(name){
				case "Step1Button":
				case "Step2Button":
				case "Step3Button":
				case "Step4Button":
					KCDataLayer.scope.content.cScreen(name.replace(/button/gi, "").toLowerCase());
					break;
			}
		}

		public function button_step(value:int = 0):void{
			var button:IBasicButton;
			var button_name:String = value > 0 ? "Step" + value.toString() + "Button" : null;
			for(var a:int = 0; a < numChildren; a++){
				if(getChildAt(a) is IBasicButton){
					button = getChildAt(a) as IBasicButton;
					button.enabled = !(button_name && ClassUtil.shortName(button) == button_name);
				}
			}
		}
	}
}
