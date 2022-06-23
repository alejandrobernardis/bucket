package activia.simon.shooter.ui.actors {
	import activia.simon.shooter.core.DataLayer;

	import org.goasap.PlayStates;

	import flash.events.Event;
	
	
	public class Acid extends AbstractActor implements Actor {
		
		public function Acid() {
			super();			
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {
			this.init();
			this.play();
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		/* METHODS */
		
		public override function startMotion():void {
			
			if ( this._actorTween == null ) {				
				this._actorTween = new ActorTween( this, Number( XML( DataLayer.CONFIG_GAME.tween.toString() ).duration.text() ) );		
				this._actorTween.addEventListener( Event.COMPLETE, CompleteHandler );
			}
			
			if( this._actorTween.state == PlayStates.PAUSED || this._actorTween.state == PlayStates.STOPPED ) {
				this._actorTween.start();
			}
			
		}
		
		public override function resumeMotion():void {
			
			if( this._actorTween.state == PlayStates.PLAYING || this._actorTween.state == PlayStates.PLAYING_DELAY ) {
				this._actorTween.pause();
			} else {
				this._actorTween.resume();
			}
			
		}
		
		public override function stopMotion():void {
			
			if ( this._actorTween.state != PlayStates.STOPPED ) {
				this._actorTween.stop();
			}
			
		}
		
		/* PRIVATE */
		
		private function CompleteHandler( e:Event ):void {
			this._actorTween.removeEventListener( Event.COMPLETE, CompleteHandler );
			this.destroy();
		}
		
	}

}