package activia.simon.shooter {
	import flash.display.Loader;
	import flash.display.LoaderInfo;
	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.net.URLRequest;
	import flash.text.TextField;
	
	
	public class Game extends MovieClip {
		
		private var _preloader:MovieClip;
		
		public function Game() {
			
			super();
			
			if ( ! this.stage ) {
				this.addEventListener( Event.ADDED_TO_STAGE, $config );
			}else {
				this.$config();
			}
			
		}
		
		private function $config( e:Event = null ):void {
			
			this._preloader = MovieClip( this.getChildByName("mcPreloader") );
			
			var path:String = new String(stage.loaderInfo.parameters.cfgPath || "../");
			
			var loader:Loader = new Loader();
			loader.contentLoaderInfo.addEventListener( ProgressEvent.PROGRESS, ProgressHandler );
			loader.contentLoaderInfo.addEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			loader.contentLoaderInfo.addEventListener( Event.COMPLETE, CompleteHandler );
			loader.load( new URLRequest( path + "swf/game_content.swf" ) );
			
			if ( e != null ) {
				this.removeEventListener( Event.ADDED_TO_STAGE, $config );
			}
			
		}
		
		private function ClearHandlers( e:Event ):void {
			var loader:LoaderInfo = LoaderInfo( e.target );
			loader.removeEventListener( ProgressEvent.PROGRESS, ProgressHandler );
			loader.removeEventListener( IOErrorEvent.IO_ERROR, ErrorHandler );
			loader.removeEventListener( Event.COMPLETE, CompleteHandler );
		}
		
		private function ProgressHandler( e:ProgressEvent ):void {
			var value:Number = Math.round( ( e.bytesLoaded * 100 ) / e.bytesTotal );
			MovieClip( this._preloader.getChildByName( "mcBar" ) ).scaleX = value / 100;
			TextField( this._preloader.getChildByName( "txLabel" ) ).text = value + " %";
		}		
		
		private function ErrorHandler( e:IOErrorEvent ):void {
			throw new Error( e.text );
			ClearHandlers(e);
		}
		
		private function CompleteHandler( e:Event ):void {
			this.removeChild( this._preloader );
			this.addChild( e.target.content );
			ClearHandlers(e);
		}
		
	}
	
}