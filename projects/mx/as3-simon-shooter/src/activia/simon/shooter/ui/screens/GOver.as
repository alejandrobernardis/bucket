package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.ui.AbstractScreen;

	import flash.events.MouseEvent;
	
	public class GOver extends AbstractScreen {
		
		public function GOver() {		
			super();
		}
		
		protected override function ButtonsManager( e:MouseEvent ):void {
			
			this.RemoveActions();
			
			switch( e.target.name ) {
				
				case "btSendScore": 	
					//DataLayer.SCREEN.sScoreRegiste();
					DataLayer.SCREEN.sHome();
					break;
					
				case "btPlayAgain": 	
					DataLayer.SCREEN.sGame();
					break;
					
			}
			
		}
		
	}
	
}