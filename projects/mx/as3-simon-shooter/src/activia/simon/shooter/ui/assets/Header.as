package activia.simon.shooter.ui.assets {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.events.ExitEvent;
	import activia.simon.shooter.events.ScreenFactoryEvent;
	import activia.simon.shooter.ui.Screen;

	import pq.events.StepManagerEvent;
	import pq.log.Debugger;
	import pq.ui.BasicButton;
	import pq.ui.StepManager;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.utils.describeType;
	
	public class Header extends StepManager {
		
		private static var $instance:Header;
		
		private static const BT_EXIT:String 			= "btExit";
		private static const BTWO_SYMPTOMS_BAR:String 	= "mcSymptomsBar";
		private static const BTWO_TIME:String 			= "mcTime";
		private static const BTWO_SCORE:String 			= "mcScore";		
		private static const BTWO_INSTRUCTIONS:String 	= "btInstructions";
		private static const BTHR_PLAY_AGAIN:String 	= "btPlayAgain";
		
		private var _exit:Boolean;
		private var _block:Boolean;
		
		public function Header() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {
			$instance = this;
			this.tween = true;
			this.addStepScript( "Step2", ApplyActions );
			this.addStepScript( "Step3", ApplyActions );
			this.addStepScript( "Step4", ApplyActions );
			this.addEventListener( StepManagerEvent.BEFORE_CHANGE, RemoveActions );
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		/* GAME-BAR */
		
		public function get symptomsBar():SymptomsBar {  
			return GameBar( BTWO_SYMPTOMS_BAR );
		}

		public function get time():TimePanel {  
			return GameBar( BTWO_TIME );
		}
		
	   	public function get score():ScorePanel {  
			return GameBar( BTWO_SCORE );
		}
		
		public function get exit():BasicButton {  
			return ResolveExitButton();
		}
		
		public function get instructions():BasicButton {  
			return GameBar( BTWO_INSTRUCTIONS );
		}
		
		public static function get instance():Header {
			return $instance;
		}
		
		public function blockButtonsActions( value:Boolean = false ):void {
			this._block = value;
		}
		
		public override function purge(...rest):void {
			this.RemoveActions();
			super.purge();	
		}
		
		/**
		 * @Helpers
		 */
		
		private function ApplyActions():void {
			this._exit = false;
			this._block = true;
			var mc:MovieClip = this.ResolveStepAsMoviClip(); 
			if ( mc == null ) return;
			for ( var a:uint = 0; a < mc.numChildren; a++ ) {
				if( mc.getChildAt(a) is BasicButton ) BasicButton( mc.getChildAt(a) ).addEventListener( MouseEvent.CLICK, ButtonsManager );
			}
		}
		
		private function RemoveActions(e:StepManagerEvent = null):void {			
			var mc:MovieClip = this.ResolveStepAsMoviClip(); 
			if ( mc == null ) return;
			for ( var a:uint = 0; a < mc.numChildren; a++ ) {
				if( mc.getChildAt(a) is BasicButton ) BasicButton( mc.getChildAt(a) ).removeEventListener( MouseEvent.CLICK, ButtonsManager );
			}			
		}	
		
		private function ButtonsManager( e:MouseEvent ):void {
			
			if ( this.index != 2 ) {
				
				switch( e.target.name )	{
					
					case BT_EXIT:
						this.ResolveEvents();
						this._exit = true;
						DataLayer.SCREEN.sGameExit(1);
						break;
						
					case BTHR_PLAY_AGAIN:
						DataLayer.SCREEN.sGame();
						RemoveActions();
						break;					
					
				}
				
				return;
				
			}
			
			if( this._block ) return;
			
			if ( DataLayer.SCREEN.isPlaying && ! time.isPaused() ) {				
				time.resumeClock();
				this.ResolveEvents();			
			}
			
			switch( e.target.name )	{
				
				case BTWO_INSTRUCTIONS:
					if ( ! this.ResolveValidateClass( "instructions", DataLayer.SCREEN.content ) ) {
						DataLayer.SCREEN.sInstructions(1);
					} else {
						DataLayer.SCREEN.sInstructions(-1);						
					}
					break;
					
				case BT_EXIT:
					this._exit = true;
					DataLayer.SCREEN.sGameExit(1);
					break;
				
			}
			
		}
		
		private function ScreenManagerHandler( e:ScreenFactoryEvent ):void {
			
			var screen:Screen = e.target.content as Screen;
			
			if ( e.type == ScreenFactoryEvent.ADD_SCREEN && ResolveValidateClass( "gameexit", screen ) ) {
				
				this.ResolveDecideEvents( screen );
				
				Debugger.DEBUG( this, "Add Exit" );
				
			} else if ( e.type == ScreenFactoryEvent.REMOVE_SCREEN ) {
				
				if ( ResolveValidateClass( "gameexit", screen ) ) {
					
					this._exit = false;
					this.ResolveDecideEvents( screen, true );					
					
					Debugger.DEBUG( this, "Remove Exit" );
					
				} else if ( ResolveValidateClass( "instructions", screen ) && ! this._exit ) {
					
					time.resumeClock();
					this.ResolveEvents( true );
					
					Debugger.INFO( this, "Remove Instructions + Resume Clock" );
					
				} else {
					
					Debugger.DEBUG( this, "Remove Instructions" );
					
				}
				
			} else {
				
				Debugger.DEBUG( this, "Add Instructions" );
				
			}
			
		}
		
		private function DecideHandler( e:ExitEvent ):void {
			
			DataLayer.SCREEN.sGameExit(-1);
			this.ResolveEvents( true );
			
			if ( this.index != 2 ) {
				if ( e.type == ExitEvent.YES ) {				
					DataLayer.SCREEN.sHome();				
				} else {				
					DataLayer.SCREEN.sGameOver(1);
				} return;	
			}
			
			if ( e.type == ExitEvent.YES ) {				
				time.stopClock();
				DataLayer.SCREEN.sHome();				
			} else {				
				time.resumeClock();
				Debugger.INFO( this, "Resume Clock" );				
			}
			
		}
		
		private function ResolveDecideEvents( ref:Screen, remove:Boolean = false ):void {
			
			if ( ! remove ) {
				ref.addEventListener( ExitEvent.NO, DecideHandler );
				ref.addEventListener( ExitEvent.YES, DecideHandler );
			}else{
				ref.removeEventListener( ExitEvent.NO, DecideHandler );
				ref.removeEventListener( ExitEvent.YES, DecideHandler );
			}
			
		}
		
		private function ResolveEvents( remove:Boolean = false ):void {
			
			if ( ! remove ) {
				DataLayer.SCREEN.addEventListener( ScreenFactoryEvent.ADD_SCREEN, ScreenManagerHandler );
				DataLayer.SCREEN.addEventListener( ScreenFactoryEvent.REMOVE_SCREEN, ScreenManagerHandler );
			}else {
				DataLayer.SCREEN.removeEventListener( ScreenFactoryEvent.ADD_SCREEN, ScreenManagerHandler );
				DataLayer.SCREEN.removeEventListener( ScreenFactoryEvent.REMOVE_SCREEN, ScreenManagerHandler );
			}
			
		}
		
		private function ResolveValidateClass( controller:String, ref:Screen ):Boolean {			
			return ( DataLayer.CONFIG_GAME..screens.screen.( @id == controller ).@controller == describeType( ref ).@name );
		}
		
		private function RankingBar( value:String ):* {
			
			if ( this.index != 4 ) return null;
			
			var mc:* = ResolveStepAsMoviClip().getChildByName( value );
			
			switch( value ) {
				
				case BT_EXIT:
				case BTHR_PLAY_AGAIN:
					return BasicButton( mc );
				
			}
			
		}
		
		private function GameBar( value:String ):* {
			
			if ( this.index != 2 ) return null;
			
			var mc:* = ResolveStepAsMoviClip().getChildByName( value );
			
			switch( value ) {
				
				case BTWO_SYMPTOMS_BAR: 	
					return SymptomsBar( mc ); 
					
				case BTWO_TIME: 			
					return TimePanel( mc ); 
					
				case BTWO_SCORE:
					return ScorePanel( mc ); 
					
				case BT_EXIT:
				case BTWO_INSTRUCTIONS:
					return BasicButton( mc ); 
				
			}
			
		}
		
		private function ResolveExitButton():BasicButton {
			
			switch( this.index ) {
				case 2:
					return GameBar( BT_EXIT );
				case 3:
					return BasicButton( ResolveStepAsMoviClip().getChildByName( BT_EXIT ) );
				case 4:
					return RankingBar( BT_EXIT );
				default:
					return null;
			}			
			
		}
		
		private function ResolveStepAsName():String {
			switch( this.index ) {
				case 2: return new String("mcGameBar");
				case 3: return new String("mcExitBar");
				case 4: return new String("mcRankingBar");
				default: return null;
			}
		}
		
		private function ResolveStepAsMoviClip():MovieClip {
			switch( this.index ) {
				case 2: 
				case 3: 
				case 4: 
					return MovieClip( this.getChildByName( this.ResolveStepAsName() ) );
				default:
					return null;
			}
		}
		
	}
	
}