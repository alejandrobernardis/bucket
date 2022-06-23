package activia.simon.avatar {
	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;

	import flash.events.MouseEvent;

	/**
	 * @author bernardisa
	 */
	public class Step5Screen extends BaseScreen {

		public function Step5Screen(data : XML = null, autorelease : Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function ButtonsManager(e:MouseEvent):void {
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "PrevButton":
					KCDataLayer.scope.content.cScreen("step4");
				break;
				case "NextButton":
					
				break;
			}
		}
	}
}
