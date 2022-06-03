package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.events.ExitEvent;
	import activia.simon.shooter.ui.AbstractScreen;

	import flash.events.MouseEvent;
	
	
	public class GExit extends AbstractScreen {
		
		public function GExit() {
			super();
		}
		
		protected override function ButtonsManager( e:MouseEvent ):void {
			
			this.RemoveActions();
			
			if ( e.target.name == "btYes" ) {
				this.dispatchEvent( new ExitEvent( ExitEvent.YES ) );				
			}else{			
				this.dispatchEvent( new ExitEvent( ExitEvent.NO ) );
			}
			
		}
		
	}
	
}