package activia.simon.avatar{
	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;

	import flash.events.MouseEvent;

	/**
	 * @author bernardisa
	 */
	public class ExitScreen extends BaseScreen {

		public function ExitScreen(data : XML = null, autorelease : Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "CancelButton":
					KCDataLayer.scope.content.rScreen();
				break;
				case "AceptButton":
					ApplicationContent.reset_avatar_data();
					KCDataLayer.scope.content.rScreen();	
					KCDataLayer.scope.content.cScreen("home");
				break;
			}
		}
		
	}
}
