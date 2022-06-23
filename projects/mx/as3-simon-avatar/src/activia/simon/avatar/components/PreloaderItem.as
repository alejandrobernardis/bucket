package activia.simon.avatar.components {
	import flash.events.Event;
	import kc.core.KCComponent;

	/**
	 * @author Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
	 */
	public class PreloaderItem extends KCComponent {
		
		public function PreloaderItem(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			play();
		}
		
	}
	
}
