package activia.simon.shooter.ui.assets {
	import pq.ui.UIComponent;

	import flash.display.MovieClip;
	import flash.events.Event;
	
	
	public class SymptomsBar extends UIComponent {
		
		public static var $instance:SymptomsBar;
		
		public function SymptomsBar() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}        
		
		private function $config( e:Event ):void {
			$instance = this;
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		public function Level1():void { this.toPercentage( .25 ); }
		public function Level2():void { this.toPercentage( .50 ); }
		public function Level3():void { this.toPercentage( .75 ); }
		
		public function Level( value:uint ):void { 
			switch(value) {
				case 1: Level1(); break;
				case 2: Level2(); break;
				case 3: Level3(); break;
			}
		}
		
		public function empty():void { this.toPercentage( 0 ); }
		public function full():void  { this.toPercentage( 1 ); }                                                                                                                                                                  
		
		public function toPercentage( value:Number ):void {
			MovieClip(this.getChildByName("mcBar")).scaleX = value;
		}
		
		public override function purge( ...rest ):void {
			$instance = null;
			super.purge();
		}
		
		/**
		 * @Helpers
		 */
		
		public static function get instance():SymptomsBar {
			return SymptomsBar.$instance;
		}
		
	}
	
}