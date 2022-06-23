package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.ui.AbstractScreen;

	import pq.ui.BasicButton;

	import flash.events.MouseEvent;
	
	public class GInstructions extends AbstractScreen {
		
		public function GInstructions() {
			super();
		}
		
		protected override function ApplyActions():void {
			
			if ( this.index == this.size ) {
				var bPrev:BasicButton = BasicButton( this.getChildByName( "btPrev" ) );
				var bPlay:BasicButton = BasicButton( this.getChildByName( "btPlay" ) );
				bPrev.x = ( ! DataLayer.SCREEN.isPlaying ) ? ( bPlay.x - ( bPrev.width + 8 ) ) : bPlay.x;
			}
			
			super.ApplyActions();
			
		}
		
		protected override function ButtonsManager( e:MouseEvent ):void {			
			
			super.RemoveActions();
			
			switch( e.target.name ) {
				case "btClose"	: 
					if ( ! DataLayer.SCREEN.isPlaying ) {
						DataLayer.SCREEN.sHome(); 			
					} else {
						DataLayer.SCREEN.sInstructions(-1);
					}
					break;
				case "btPlay"	: DataLayer.SCREEN.sGame(); 			break;
				case "btNext"	: DataLayer.SCREEN.content.nextStep(); 	break;
				case "btPrev"	: DataLayer.SCREEN.content.prevStep(); 	break;
			}
			
		}
		
	}
	
}