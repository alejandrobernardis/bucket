package activia.simon.shooter.ui.assets {
	import flash.display.MovieClip;
	import flash.events.Event;
	
	
	public class ThreatsIcons extends MovieClip {
		
		public function ThreatsIcons() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {
			
			this.gotoAndStop(
				Math.round( 
					1 + Math.random() * this.totalFrames - 1 
				)
			);
			
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
			
		}
		
	}
	
}