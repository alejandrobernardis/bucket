package activia.simon.shooter {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.core.Localization;

	import pq.core.Config;
	import pq.log.Debugger;
	import pq.utils.StringUtil;

	import flash.display.MovieClip;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	
	
	public class GameContent extends MovieClip {
		
		private var _init:Boolean = false;
		
		public function GameContent() {
			
			super();
			
			if ( ! this.stage ) {
				this.addEventListener( Event.ADDED_TO_STAGE, $config );
			}else {
				this.$config();
			}
			
		}
		
		public function init( ...rest ):void {
			
			if ( ! this._init ) return;
			
			DataLayer.initialize( this );
			DataLayer.getInstance().addEventListener( Event.COMPLETE, CompleteHandler );
			
		}
		
		private function $config( e:Event = null ):void {
			
			this._init = true;
			
			if ( e != null ) {
				this.removeEventListener( Event.ADDED_TO_STAGE, $config );
			}
			
			this.init();
			
		}
		
		///////////////////////////////////////////////////////////////////////////////////
		
		/*
		 * @localization 
		 */
		
		public function CompleteHandler( e:Event = null ):void {
			
			if ( ! StringUtil.isEmpty( DataLayer.CONFIG_GAME..localization.text() ) ) {
				// if( ! DataLayer.isFacebook() ) {
					var localization:Config = new Config();
					localization.addEventListener( Event.COMPLETE, CompleteLocalization );
					localization.addEventListener( ErrorEvent.ERROR, ErrorLocalization );
					localization.load( DataLayer.CONFIG.dependency( DataLayer.CONFIG_GAME..localization.text() ) );
					Debugger.INFO( this, DataLayer.CONFIG.dependency( DataLayer.CONFIG_GAME..localization.text() ) );
				/* } else {
					Localization.data( FacebookXMLHelper.XML_LOCALIZATION );
					CompleteLocalization();
				} */
				
			} else {
				this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR, false, false, "No existe la ruta del archivo de localización." ) );
			}	
			
			DataLayer.getInstance().removeEventListener( Event.COMPLETE, CompleteHandler );
			
		}
		
		private function ClearLocalization( e:Event ):void {
			e.target.removeEventListener( Event.COMPLETE, CompleteLocalization );
			e.target.removeEventListener( ErrorEvent.ERROR, ErrorLocalization );
		}
		
		private function ErrorLocalization( e:ErrorEvent ):void {
			this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR, false, false, "El XML de localización del juego no pudo ser cargado." ) );
			ClearLocalization(e);
		}
		
		private function CompleteLocalization( e:Event = null ):void {
			
			if ( e != null ) {
				Localization.data( e.target.data );
				e.target.purge();
				ClearLocalization(e);
			}
			
			for ( var a:uint = 0; a < this.currentLabels.length; a++ ) {
				switch( this.currentLabels[a].name.toLowerCase() ) {
					case "content": this.addFrameScript( this.currentLabels[a].frame, FirstScreen ); break;
				}
			}
			
			this.gotoAndPlay( "init" );
			Debugger.DEBUG( this, "Complete Extrernal Data." );
			
		}
		
		private function FirstScreen():void {
			DataLayer.SCREEN.sHome();	
		}
		
		///////////////////////////////////////////////////////////////////////////////////
		
		/**
		 * @api
		 */
	 	
		public function GameHome():void {} 
		public function GameInstructions():void {}
		public function GamePlay():void {} 
		public function GamePause():void {} 
		public function GameRestart():void {}
		public function GameExit():void {}
		public function GameRanking():void { }
		
		protected function ResolveReset():void {			
			DataLayer.collection.update( "score_value", 0 );
		}
		
	}
	
}