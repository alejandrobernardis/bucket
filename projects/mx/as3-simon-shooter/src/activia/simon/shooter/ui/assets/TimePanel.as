package activia.simon.shooter.ui.assets {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.core.Localization;
	import activia.simon.shooter.events.TimePanelEvent;

	import pq.ui.UIComponent;
	import pq.utils.StringUtil;

	import flash.events.Event;
	import flash.events.TimerEvent;
	import flash.utils.Timer;
	
	public class TimePanel extends UIComponent {
		
		private static var $instance:TimePanel;
		
		private static const MAX_VALUE:uint 	= 360000;
		private static const MINUTE:uint 		= 60000;
		private static const SECOND:uint 		= 1000;
		private static const DELAY:uint 		= 1000;
		
		private var _isRunning:Boolean;
		private var _isPaused:Boolean;
		
		private var _minutes:uint;
		private var _seconds:uint;
		
		private var _max:uint;
		private var _delay:uint;
		private var _count:uint;
		private var _timer:Timer;
		private var _pattern:String;
		private var _levels:uint;
		
		public function TimePanel() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event = null ):void {
			
			$instance = this;
			
			//if ( ! DataLayer.collection.contain( "score_minutes" ) ) DataLayer.collection.add( "score_minutes", 0 );
			//if ( ! DataLayer.collection.contain( "score_seconds" ) ) DataLayer.collection.add( "score_seconds", 0 );
			
			this._pattern = Localization( this.getChildByName( "mcLocale" ) ).data..label.text();
			
			var max:Number = Number( DataLayer.CONFIG_GAME.config.time.text() || TimePanel.MAX_VALUE );
			var delay:Number = Number( DataLayer.CONFIG_GAME.config.delay.text() || TimePanel.DELAY );
			
			this._max = ( max < TimePanel.MINUTE ) ? TimePanel.MINUTE : max;
			this._delay = ( TimePanel.DELAY < 0 ) ? TimePanel.DELAY : delay;
			this._count = Math.floor( this._max / TimePanel.SECOND );
			this._levels = Math.ceil( ( max / 3 ) / MINUTE );
			
			this._timer = new Timer( this._delay, this._count );
			this._timer.addEventListener( TimerEvent.TIMER, update );
			this._timer.addEventListener( TimerEvent.TIMER_COMPLETE, stopClock );			
			
			this.reset();
			
			if ( e != null ) {
				this.removeEventListener( Event.ADDED_TO_STAGE, $config );
			}
			
		}
		
		
		
		public function isRunning():Boolean {
			return ( this._isRunning && ! this._isPaused );
		}
		
		public function isPaused():Boolean {
			return ( this._isRunning && this._isPaused );
		}
		
		public function get minutes():uint {
			return this._minutes;
		}
		
		public function get seconds():uint {
			return this._seconds;
		}
		
		
		
		public function restartClock(...rest):void {			
			
			if ( this.isRunning() ) this.stopClock();
			
			this.reset();
			this.startClock();		
			
		}
		
		public function startClock(...rest):void {			
			
			if ( this.isRunning() || this._timer.currentCount == this._count ) return;
			
			this._isRunning = true;
			
			this._timer.start();			
			this.dispatchEvent( new TimePanelEvent( TimePanelEvent.START ) );
			
		}
		
		public function stopClock(...rest):void {
			
			if ( ! this.isRunning() ) return;			
			
			this._isRunning = false;	
			this._minutes = 0;
			this._seconds = 0;
			
			this.print();
			this._timer.stop();
			this.dispatchEvent( new TimePanelEvent( TimePanelEvent.STOP ) );
			
		}
		
		public function resumeClock(...rest):void {
			if ( ! this.isPaused() ) {
				this._isPaused = true;
				this._timer.stop();
				this.dispatchEvent( new TimePanelEvent( TimePanelEvent.PAUSE ) );
			}else {				
				this._isPaused = false;
				this._timer.start();
				this.dispatchEvent( new TimePanelEvent( TimePanelEvent.RESUME ) );
			}			
		}
		
		
		
		public override function purge( ...rest ):void {
			
			if( this._timer != null ){
				this._timer.stop();
				this._timer.removeEventListener( TimerEvent.TIMER, update );
				this._timer.removeEventListener( TimerEvent.TIMER_COMPLETE, stopClock );
				this._timer = null;
			}
			
			this._isRunning = undefined;
			this._isPaused = undefined;
			this._minutes = undefined;
			this._seconds = undefined;			
			this._max = undefined;
			this._pattern = null;
			
			TimePanel.$instance = null;
			
			super.purge();
			
		}
		
		/**
		 * @Helpers
		 */
		
		public static function get instance():TimePanel {
			return TimePanel.$instance;
		}
		
		
		private function print():void {			
			
			DataLayer.collection.update( "score_minutes", this._minutes );
			DataLayer.collection.update( "score_seconds", this._seconds );
			
			Localization( this.getChildByName( "mcLocale" ) ).labelForce ( 
				"label", 
				StringUtil.substitute( 
					this._pattern, 
					( this._minutes < 10 ) ? "0" + this._minutes : this._minutes, 
					( this._seconds < 10 ) ? "0" + this._seconds : this._seconds
				)
			);
			
		}
		
		private function reset():void {			
			
			this._isRunning = false;
			this._isPaused = false;
			this._minutes = Math.floor( this._max / TimePanel.MINUTE );
			this._seconds = 0;
			
			this._timer.reset();			
			this.print();
			
		}
		
		private function update( e:TimerEvent ):void {
			
			if ( this._seconds < 1 ) {
				this._minutes --;
				this._seconds = 59;
				if( this._minutes % this._levels == 0 ){
					this.dispatchEvent( new TimePanelEvent( TimePanelEvent.CHANGE_LEVEL ) );
				}
			}else{
				this._seconds --;
			}
			
			this.print();
			
		}
		
	}
	
}