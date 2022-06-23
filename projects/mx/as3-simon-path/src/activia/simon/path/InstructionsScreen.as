package activia.simon.path{
	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;

	import flash.events.MouseEvent;


	/**
	 * @author bernardisa
	 */
	public class InstructionsScreen extends BaseScreen{

		public function InstructionsScreen(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}
		
		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "CloseButton":
					KCDataLayer.scope.content.rScreen();
				break;
			}
		}
		
	}
}
