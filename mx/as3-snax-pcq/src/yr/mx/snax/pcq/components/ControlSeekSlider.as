package yr.mx.snax.pcq.components {
	import flash.display.MovieClip;
	import kc.api.IBasicButton;
	import kc.api.IKCComponent;
	import kc.core.KCComponent;

	public class ControlSeekSlider extends KCComponent implements IKCComponent {
		
		public function ControlSeekSlider(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		public function get button_drag():IBasicButton {
			return getChildByName("btDrag") as IBasicButton;
		}
		
		public function get mc_progress():MovieClip {
			return getChildByName("mcProgress") as MovieClip;
		}
		
		public function get mc_progress_load():MovieClip {
			return getChildByName("mcProgressLoad") as MovieClip;
		}
		
	}
	
}
