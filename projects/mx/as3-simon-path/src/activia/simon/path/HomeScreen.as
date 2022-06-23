
package activia.simon.path {

	import caurina.transitions.Tweener;
	import kc.core.KCDataLayer;
	import kc.events.KCComponentStepsEvent;
	import kc.utils.ClassUtil;

	import flash.display.MovieClip;
	import flash.events.Event;
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
		}

		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "InstructionsHomeButton":
					KCDataLayer.scope.content.aScreen("instructions");
				break;
				case "BeginButton":
					Tweener.addTween(getButton("btInstructions"), {alpha: 0, time: 0.8, transition: "easeOutQuint"});
					Tweener.addTween(getButton("btBegin"), {alpha: 0, time: 0.8, transition: "easeOutQuint"});
					addEventListener(KCComponentStepsEvent.OUTRO_FINISHED, onOutro);
					MovieClip(getChildByName("mcSimon")).play();
				break;
			}
		}

		private function onOutro(event:KCComponentStepsEvent):void{
			removeEventListener(KCComponentStepsEvent.OUTRO_FINISHED, onOutro);
			KCDataLayer.scope.content.cScreen("step1");
		}
		
	}
	
}
