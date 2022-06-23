package activia.simon.shooter.ui.assets {
	import pq.ui.UIComponent;

	import flash.events.Event;
	import flash.events.MouseEvent;
	
	
	public class Pointer extends UIComponent {
		
		public function Pointer() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {
			this.stage.addEventListener( MouseEvent.MOUSE_DOWN, Handler );
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function Handler(e:MouseEvent):void {
			this.play();
		}
		
		public override function purge(...rest):void {
			this.stage.removeEventListener( MouseEvent.MOUSE_DOWN, Handler );
			super.purge();
		}
		
	}

}