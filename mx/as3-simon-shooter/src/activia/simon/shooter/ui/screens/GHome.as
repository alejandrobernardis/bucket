package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.ui.AbstractScreen;

	import flash.events.MouseEvent;
	
	
	public class GHome extends AbstractScreen {
		
		public function GHome() {
			super();
		}
		
		protected override function ButtonsManager( e:MouseEvent ):void {
			
			this.RemoveActions();
			
			switch( e.target.name ) {
				
				case "btPlayTheGame" : 	
					DataLayer.SCREEN.sGame(); 			
					break;
					
				case "btInstructions": 	
					DataLayer.SCREEN.sInstructions(); 	
					break;
					
				case "btMap":			
					DataLayer.SCREEN.exit();
					break;
					
			}
			
		}
		
	}
	
}