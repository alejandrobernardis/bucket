package activia.simon.shooter.ui.screens {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.events.TimePanelEvent;
	import activia.simon.shooter.ui.AbstractScreen;
	import activia.simon.shooter.ui.actors.ActorFactory;
	import activia.simon.shooter.ui.assets.Countdown;
	import activia.simon.shooter.ui.assets.Header;

	import pq.log.Debugger;
	import pq.ui.Size;

	import flash.events.TimerEvent;
	import flash.system.System;
	import flash.ui.Mouse;
	import flash.utils.Timer;

	public class GContainer extends AbstractScreen {
		
		private static var $frameRateCache:Number;
		
		private var _countdown:Countdown;
		private var _countdown_count:uint;
		private var _actorFactory:ActorFactory;
		private var _isInit:Boolean;
		
		public function GContainer() {
			super();
			this._isInit = false;
		}
		
		public override function init():void {
			
			if ( this._status ) return;
			super.init();
			
			$frameRateCache = DataLayer.SCOPE.stage.frameRate;
			
			this.restart();
			this._isInit = true;
			
		}
		
		public function restart():void {
			
			var size:Size = new Size( DataLayer.CONFIG_GAME.config.canvas.size.text() );
			
			this._countdown = new Countdown();
			this._countdown.align( size.width / 2, size.height / 2 );
			this.addChild( this._countdown );
			
			this._countdown_count = uint(  DataLayer.CONFIG_GAME.config.countdown.text() ) + 1;
			
			var time:Timer = new Timer( 600 );
			time.addEventListener( TimerEvent.TIMER, TimerHandler );
			time.start();		
			
		}
		
		public override function destroy():void {
			
			if ( ! this._status ) return;
			super.destroy();
			
		}
		
		public override function purge(...rest):void {
			
			this._countdown = null;
			this._countdown_count = undefined;
			this._isInit = undefined;
			this._actorFactory = null;
			
			DataLayer.SCOPE.stage.frameRate = GContainer.$frameRateCache;
			GContainer.$frameRateCache = undefined;
			super.purge();
			
			System.gc();
			
		}
		
		private function TimerHandler(e:TimerEvent):void {
			
			this._countdown_count--;
			
			if ( this._countdown_count > 0 ) {				
				
				this._countdown.label = String( this._countdown_count );				
				
			}else {				
				
				this.removeChild( this._countdown );
				this._countdown = null;
				this._countdown_count = undefined;				
				
				e.target.stop();
				e.target.removeEventListener( TimerEvent.TIMER, TimerHandler );
				e = null;
				
				Debugger.INFO( this, "Game Initialize." );				
				this.ResolveElements();				
				
			}			
			
		}
		
		private function ResolveElements():void {
			
			DataLayer.collection.update( "score_value", 0 );
			
			var header:Header = Header.instance;
			Debugger.DEBUG( this, header );
			
			header.symptomsBar.Level1();
			header.score.content.update();
			
			this._actorFactory = new ActorFactory();
			this._actorFactory.data = XML( DataLayer.CONFIG_GAME.actors.toString() );
			this._actorFactory.forceFrameRate();
			this._actorFactory.init();
			this.addChild( this._actorFactory );
			
			header.time.restartClock();			
			header.time.addEventListener( TimePanelEvent.PAUSE, Handler );
			header.time.addEventListener( TimePanelEvent.RESUME, Handler );
			header.time.addEventListener( TimePanelEvent.STOP, FinishedHandler );
			header.time.addEventListener( TimePanelEvent.CHANGE_LEVEL, LevelHandler );
			
			header.blockButtonsActions( false );
		
		}
		
		
		private function Handler(e:TimePanelEvent):void {	
			if( e.type != TimePanelEvent.RESUME ){
				this._actorFactory.pauseAllMotion();
			}else{
				this._actorFactory.resumeAllMotion();
			}
		}
		
		private function LevelHandler(e:TimePanelEvent):void {
			if( this._actorFactory.level < 3 ) {
				this._actorFactory.level ++;
				Header.instance.symptomsBar.Level( this._actorFactory.level );
			}
		}
		
		private function FinishedHandler(e:TimePanelEvent):void {
			
			var header:Header = Header.instance;
			
			header.symptomsBar.full();
			header.time.removeEventListener( TimePanelEvent.PAUSE, Handler );
			header.time.removeEventListener( TimePanelEvent.RESUME, Handler );
			header.time.removeEventListener( TimePanelEvent.STOP, FinishedHandler );
			header.time.removeEventListener( TimePanelEvent.CHANGE_LEVEL, LevelHandler );
			
			this._actorFactory.finished();
			Mouse.show();
			//DataLayer.SCREEN.sGameOver();
			
		}
		
		public static function get frameRateCache():Number { 
			return $frameRateCache; 
		}
		
	}
	
}