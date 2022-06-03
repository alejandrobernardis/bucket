package {
	import yr.mx.snax.pcq.VideoInteractive;
	import kc.api.IApplication;
	import kc.api.ILoader;
	import kc.api.flash.IMovieClip;
	import kc.loaders.AssetLoader;
	import kc.logging.SimpleLog;
	import kc.utils.ExceptionUtil;

	import flash.display.Sprite;
	import flash.display.StageAlign;
	import flash.display.StageScaleMode;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.system.ApplicationDomain;
	import flash.system.LoaderContext;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class Application extends Sprite implements IApplication {

		// @variables

		private var _preloader:ApplicationPreloader;
		
		protected var _content:IMovieClip;
		protected var _context:LoaderContext;
		
		public static var $ref:IApplication;

		// @constructor

		public function Application() {

			super();
			
			if( !stage ) {
				addEventListener( Event.ADDED_TO_STAGE, AddedToStageHandler );
			} else {
				AddedToStageHandler();
			}

		}
		
		// @properties (r)

		public function get content():IMovieClip {
			return _content;
		}

		public function get context():LoaderContext {
			return _context;
		}
		
		public function get flash_vars():Object {
			if( ! this ) 
				return null;
			if( ! this.stage.loaderInfo.parameters )
				return new Object();
			return this.stage.loaderInfo.parameters;
		}

		// @handlers

		private function AddedToStageHandler(e:Event = null):void {
			
			SimpleLog.breakpoint("{KC} v1.0.0");
			SimpleLog.print("Project: PCQ.");
			SimpleLog.print("Application: Initialized.");
			
			if(!$ref){
				$ref = this;
			}else{SimpleLog.print("El valor ya fue asignado.");}
			
			stage.scaleMode = StageScaleMode.NO_SCALE;
			stage.align = StageAlign.TOP;
			
			_context = new LoaderContext(
				true, 
				ApplicationDomain.currentDomain
			);
			
			_preloader = new ApplicationPreloader();
			_preloader.position(this.stage.stageWidth/2, this.stage.stageHeight/2);
			addChild(_preloader);
			
			var aloader:ILoader = new AssetLoader();
			aloader.addEventListener(Event.COMPLETE, CompleteAssetsHandler);
			aloader.addEventListener(ProgressEvent.PROGRESS, ProgressHandler);
			aloader.addEventListener(IOErrorEvent.IO_ERROR, ErrorAssetsHandler);
			aloader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorAssetsHandler);
			aloader.context = _context;
			aloader.load(flash_vars.app_path || './application.swf');
					
			if(e){
				removeEventListener(Event.ADDED_TO_STAGE, AddedToStageHandler);
			}

		}
		
		protected function ClearAssetsHandlers(value:ILoader):void {
			value.addEventListener(Event.COMPLETE, CompleteAssetsHandler);
			value.addEventListener(ProgressEvent.PROGRESS, ProgressHandler);
			value.removeEventListener(IOErrorEvent.IO_ERROR, ErrorAssetsHandler);
			value.removeEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorAssetsHandler);
			value.purge();
		}
		
		protected function CompleteAssetsHandler(e:Event):void {
			addChild(e.target.content as VideoInteractive);
			removeChild(_preloader);
			ClearAssetsHandlers(e.target as ILoader);
		}

		protected function ErrorAssetsHandler(e:ErrorEvent):void {
			ExceptionUtil.ViewError(e, true);
			ClearAssetsHandlers(e.target as ILoader);
		}
		
		protected function ProgressHandler(e:Event):void {
			_preloader.progressEvent(e);
		}

	}

}
