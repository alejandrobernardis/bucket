package activia.simon.avatar{
	import flash.events.Event;
	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;

	import flash.events.MouseEvent;

	/**
	 * @author Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
	 */
	public class HomeScreen extends BaseScreen{

		public function HomeScreen(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}
		
		
		override protected function $config(e:Event):void{
			super.$config(e);
			KCDataLayer.scope.content.menu.user_name = null;
			KCDataLayer.scope.content.menu.enabled_menu = false;
		}

		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "BeginButton":
					KCDataLayer.scope.content.cScreen("step1");
					KCDataLayer.scope.content.menu.enabled_menu = true;
					break;
			}
		}
		
	}
	
}
