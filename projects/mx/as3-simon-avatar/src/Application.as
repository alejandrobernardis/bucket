
package {

	import flash.display.StageAlign;
	import flash.display.StageScaleMode;
	import kc.api.IApplication;
	import kc.api.IIterator;
	import kc.api.IKCQueueLoader;
	import kc.api.ILoader;
	import kc.api.IMap;
	import kc.core.KCDataLayer;
	import kc.core.KCQueueLoader;
	import kc.events.KCQueueLoaderEvent;
	import kc.loaders.AssetLoader;
	import kc.logging.SimpleLog;
	import kc.tda.SimpleMap;
	import kc.utils.ExceptionUtil;

	import com.facebook.graph.Facebook;

	import flash.display.Bitmap;
	import flash.display.Sprite;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.external.ExternalInterface;
	import flash.media.Sound;
	import flash.system.ApplicationDomain;
	import flash.system.LoaderContext;
	import flash.system.Security;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class Application extends Sprite implements IApplication {

		// @variables

		private var _preloader:ApplicationPreloader;
		
		protected var _content:ApplicationContent;
		protected var _context:LoaderContext;

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

		public function get content():ApplicationContent {
			return _content;
		}

		public function get context():LoaderContext {
			return _context;
		}

		// @handlers

		private function AddedToStageHandler(event:Event = null):void {
			
			stage.scaleMode = StageScaleMode.NO_SCALE;
			stage.align = StageAlign.TOP;

			SimpleLog.breakpoint("KC Application v1.0");
			SimpleLog.print("Project: ASA.");
			SimpleLog.print("Application: Initialized.");

			_context = new LoaderContext(
				true,
				ApplicationDomain.currentDomain
			); 

			_preloader = new ApplicationPreloader();
			_preloader.scaleMode = "scaleY";
			_preloader.x = stage.stageWidth / 2;
			_preloader.y = ( stage.stageHeight / 2 );

			addChild( _preloader );
			
			Security.allowDomain("*");
			Security.allowDomain("*.facebook.com");
			Security.allowDomain("*.fbcdn.net");
			
			var kcdata:KCDataLayer = KCDataLayer.getInstance();
			kcdata.addEventListener( Event.COMPLETE, CompleteDataLayerHandler );
			kcdata.addEventListener( ErrorEvent.ERROR, ErrorDataLayerHandler );
			kcdata.addEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, ProgressHandler );

			KCDataLayer.init(this);
			_preloader.label("Datos", "Cargando:");
			
			SimpleLog.dump("FlashVars", KCDataLayer.flashVars);

			if(event){
				removeEventListener( Event.ADDED_TO_STAGE, AddedToStageHandler );
			}

		}
		
		// @facebook
		
		protected function FBLogin():void {
			var premissions:Array = ['publish_stream'];
			Facebook.login(FBLoginHandler, {perms: premissions.join(',')});
		}

		private function FBLoginHandler(response:Object, fail:Object) : void {
			if (response==null) {
				SimpleLog.dump(response, fail);
				ExternalInterface.call('redirect');
				return;
			} else{
				SimpleLog.print("FB Init: ",response);
			}
		}

		private function FBInitHandler(response:Object, fail:Object) : void {
			return;
			if (response==null) {
				SimpleLog.dump(response, fail);
				ExternalInterface.call('redirect');
				return;
			} else{
				SimpleLog.print("FB Init: ",response);
			}
		}

		// @datalayer

		protected function ClearDataLayerHandlers():void {
			var kcdata:KCDataLayer = KCDataLayer.getInstance();
			kcdata.removeEventListener( Event.COMPLETE, CompleteDataLayerHandler );
			kcdata.removeEventListener( ErrorEvent.ERROR, ErrorDataLayerHandler );
			kcdata.removeEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, ProgressHandler );
		}

		protected function CompleteDataLayerHandler(e:Event):void {
			
			ClearDataLayerHandlers();
			
			// Facebook
			
			try{
				Security.allowDomain("*");
				Facebook.init("1469798294", FBInitHandler);
			}catch(e:Error){SimpleLog.dump("FB Error", e);}
			
			// DataLayer
			
			var notComplete:Boolean;
			var list:IMap = KCDataLayer.config.assetsList();
			
			if( list ){

				var mapping:IIterator = list.iterator();

				if( mapping.size() ) {

					var qloader:IKCQueueLoader = new KCQueueLoader();
					qloader.addEventListener( KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteAssetsHandler );
					qloader.addEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, ProgressHandler );
					qloader.addEventListener( IOErrorEvent.IO_ERROR, ErrorAssetsHandler );
					qloader.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorAssetsHandler );
					//qloader.verbose = true;

					while( mapping.hasNext() ) {
						mapping.next();
						qloader.add(
							mapping.value()[1],
							{
								key: mapping.value()[0],
								context: _context
							}
						);
					}
					
					qloader.dump();
					qloader.start();
					notComplete = true;
					_preloader.label("...");

				}

				mapping.purge();

			}

			list.purge();

			if( ! notComplete )
				qloader.dispatchEvent(
					new KCQueueLoaderEvent(
						KCQueueLoaderEvent.QUEUE_COMPLETE
					)
				);
				
			SimpleLog.print("Application Data Layer: OK.");

		}

		protected function ErrorDataLayerHandler(e:ErrorEvent):void {
			ClearDataLayerHandlers();
			ExceptionUtil.ViewError(e);
		}

		// @assets

		protected function ClearAssetsHandlers(value:IKCQueueLoader):void {
			value.removeEventListener( KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteAssetsHandler );
			value.removeEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, ProgressHandler );
			value.removeEventListener( IOErrorEvent.IO_ERROR, ErrorAssetsHandler );
			value.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorAssetsHandler);
			value.purge();
		}

		protected function CompleteAssetsHandler(e:KCQueueLoaderEvent):void {

			// #I linda hardcodeadita! ^_^

			var qloader:IKCQueueLoader = e.target as IKCQueueLoader;
			var list:IMap = KCDataLayer.config.assetsList();

			if( list ){

				var mapping:IIterator = list.iterator();

				if( mapping.size() ) {

					var map:IMap = new SimpleMap(32);
					var mapImg:IMap = new SimpleMap(128);
					var mapVec:IMap = new SimpleMap(128);

					while( mapping.hasNext() ) {
						mapping.next();
						if( mapping.value()[0].search(/^bg[A-Z]\w*$/) != -1 ) {
							map.add(
								mapping.value()[0].toLowerCase(),
								qloader.getContentAs(
									mapping.value()[1],
									Bitmap
								)
							);
						}else if( mapping.value()[0].search(/^(img|bm)[A-Z]\w*$/) != -1 ) {
							mapImg.add(
								mapping.value()[0].toLowerCase(),
								qloader.getContentAs(
									mapping.value()[1],
									Bitmap
								)
							);
						}else if( mapping.value()[0].search(/^(vt|vc)[A-Z]\w*$/) != -1 ) {
							mapVec.add(
								mapping.value()[0].toLowerCase(),
								qloader.getContent(
									mapping.value()[1]
								)
							);
						}else if( mapping.value()[0] == "music" ){
							KCDataLayer.collection.add(
								"music",
								qloader.getContentAs(
									mapping.value()[1],
									Sound
								)
							);
						}
					}

					KCDataLayer.collection.add("backgrounds", map);
					KCDataLayer.collection.add("images", mapImg);
					KCDataLayer.collection.add("vectors", mapVec);
					
				}

				mapping.purge();

			}

			list.purge();

			// #E linda hardcodeadita! ^_^

			ClearAssetsHandlers(qloader);

			if( KCDataLayer.collection.containsKey("tracking") ){
				var data:XML = KCDataLayer.collection.value("tracking") as XML;
				GoogleAnalytics.initialize(data, data.base.text().toString());
			}

			var url:String = KCDataLayer.basePath + (
				KCDataLayer.getFlashVar( "cfgApplicationContent" )
				|| "application_content.swf"
			);

			var appContent:ILoader = new AssetLoader();
			appContent.addEventListener( Event.COMPLETE, CompleteAppContentHandler );
			appContent.addEventListener( ProgressEvent.PROGRESS, ProgressHandler );
			appContent.addEventListener( IOErrorEvent.IO_ERROR, ErrorAppContentHandler );
			appContent.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorAppContentHandler );
			appContent.context = _context;

			appContent.load(
				KCDataLayer.config.getValueAndResolveDependency("applicationContent")
				|| url
			);

			_preloader.label("Contenido");
			
			SimpleLog.print("Application Assets: OK.");

		}

		protected function ErrorAssetsHandler(e:ErrorEvent):void {
			ExceptionUtil.ViewError(e);
			ClearAssetsHandlers( e.target as IKCQueueLoader );
		}

		// @application

		protected function ClearAppContentHandlers(value:ILoader):void {
			value.removeEventListener( Event.COMPLETE, CompleteAppContentHandler );
			value.removeEventListener( ProgressEvent.PROGRESS, ProgressHandler );
			value.removeEventListener( IOErrorEvent.IO_ERROR, ErrorAppContentHandler );
			value.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorAppContentHandler );
			value.purge();
		}

		protected function CompleteAppContentHandler(e:Event):void {

			var appContent:ILoader = e.target as ILoader;

			removeChild(_preloader);
			_preloader = null;

			_content = appContent.content as ApplicationContent;
			addChild( _content );

			ClearAppContentHandlers( appContent );
			
			SimpleLog.print("Application Content: OK.");

		}

		protected function ErrorAppContentHandler(e:ErrorEvent):void {
			ExceptionUtil.ViewError(e);
			ClearAppContentHandlers(e.target as ILoader);
		}

		// @progress

		protected function ProgressHandler(e:Event):void {
			_preloader.progressEvent(e);
		}

	}

}
