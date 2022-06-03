package activia.simon.shooter.ui.actors {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.core.SoundManager;
	import activia.simon.shooter.ui.assets.Header;
	import activia.simon.shooter.ui.assets.LabelPoint;

	import org.goasap.PlayStates;

	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.geom.Point;
	
	
	
	
	
	public class AbstractBomb extends AbstractActorComplex implements Bomb {
		
		public function AbstractBomb() {			
			super();			
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {			
			
			this.init();
			
			this.buttonMode = true;
			this.useHandCursor = false;
			this.mouseEnabled = true;
			this.mouseChildren = false;
			
			this.addEventListener( MouseEvent.MOUSE_DOWN, MouseHandler );
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
			
		}
		
		/* METHODS */
		
		public override function destroy():void {
			
			if ( this._actorTween != null ) {
				this._actorTween.removeEventListener( Event.COMPLETE, CompleteHandler );
			}
			
			ActorFactory.instance.decrement();			
			super.destroy();
			
		}
		
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
		
		/* PRIVATE/PROTECTED */
		
		public function updateScore():void {
			if( this.index < this.size ){
				var score:Number = Number( DataLayer.collection.value( "score_value" ) );
				DataLayer.collection.update( "score_value", Number( score + Number( this.points ) ) );
				Header.instance.score.content.update();
				this.nextStep(); 
			}
		}
		
		protected function MouseHandler( e:MouseEvent ):void {
			
			var p:Point = new Point();
			p.x = this.owner.stage.mouseX;
			p.y = this.owner.stage.mouseY; 
			
			if( this.type == "protons" || this.type == "threats" ){ 
				
				if(  this.owner.hitTestPoint( p.x, p.y ) ){
					
					updateScore();
					
					var point:LabelPoint = new LabelPoint();
					point.point = this.points;
					point.align( this.x+8, this.y );
					
					Sprite( this.owner ).addChild( point );
					
				}
				
			}else{
				
				ActorFactory.instance.applyWildcard();
				this.nextStep();
				
			}
			
			if ( this.sound != null ) {
				SoundManager.getInstance().hit( this.sound, 1 );
			}
			
			//ActorFactory.instance.pointer.play();
			this.removeEventListener( MouseEvent.MOUSE_DOWN, MouseHandler );
			
		}
		
		private function CompleteHandler( e:Event ):void {
			this.destroy();
		}
		
	}

}