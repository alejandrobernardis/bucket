package activia.simon.shooter.ui.assets {
	import activia.simon.shooter.core.Localization;

	import pq.ui.UIComponent;

	import flash.events.Event;
	
	
	public class ScorePanel extends UIComponent {
		
		private static var $instance:ScorePanel;
		
		public function ScorePanel() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {
			$instance = this;
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		public function get content():Localization {
			return Localization( this.getChildByName( "mcLocale" ) );
		}
		
		public override function purge( ...rest ):void {
			$instance = null;
			super.purge();
		}
		
		/**
		 * @Helpers
		 */
		
		public static function get instance():ScorePanel {
			return ScorePanel.$instance;
		}		
		
	}
	
}