
package kc.loaders {
	import kc.api.ILoader;
	import kc.utils.ExceptionUtil;

	import flash.events.Event;
	import flash.media.Sound;
	import flash.media.SoundLoaderContext;
	import flash.system.LoaderContext;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SoundLoader extends AbstractLoader implements ILoader {

		// @variables

		protected var _soundLoaderContext:SoundLoaderContext;

		// @constructor

		public function SoundLoader() {
			super();
		}

		// @override

		// TODO: Mejorar este tema! se me paso por alto... @.@

		override public function set context(value:LoaderContext):void {
			super.context = value;
			_soundLoaderContext = new SoundLoaderContext( 1000, false );
		}

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

			_loader = new Sound();
			ResolveEvents();

			_loader.load( _request, _soundLoaderContext );

		}

		override protected function CompleteHandler(e:Event):void {
			_content = Sound( _loader );
			super.CompleteHandler(e);
		}

	}

}
