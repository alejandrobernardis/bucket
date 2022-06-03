
package kc.loaders {

	import kc.api.ILoader;
	import kc.core.KCDataLayer;
	import kc.utils.ExceptionUtil;

	import flash.display.Loader;
	import flash.events.Event;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class AssetLoader extends AbstractLoader implements ILoader {

		// @constructor

		public function AssetLoader() {
			super();
		}

		// @override

		override public function get dataFormat():String {
			throw ExceptionUtil.PropertyIsNotAvailable( "dataFromat" );
		}

		override public function set dataFormat(value:String):void {
			throw ExceptionUtil.PropertyIsNotAvailable( "dataFromat" );
		}

		override protected function ResolveConexion(action:String, url:String = null, method:String = null):void {

			if( action != AbstractLoader.LOAD ){
				throw ExceptionUtil.MethodIsNotAvailable( action );
			}

			super.ResolveConexion( action, url, method );
					
			_loader = new Loader();
			_eventsTarget = _loader.contentLoaderInfo;
			ResolveEvents();

			_loader.load( _request, KCDataLayer.scope.context );

		}

		override protected function CompleteHandler(e:Event):void {
			_content = _loader.content;
			super.CompleteHandler(e);
		}

	}

}
