
package kc.loaders {

	import kc.api.ILoader;
	import kc.utils.ExceptionUtil;

	import flash.events.Event;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLLoader;
	import flash.net.sendToURL;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class TextLoader extends AbstractLoader implements ILoader {

		// @constructor

		public function TextLoader() {
			super();
		}

		// @override

		override public function set dataFormat(value:String):void {
			throw ExceptionUtil.PropertyIsNotAvailable( "dataFormat", 1 );
		}

		override protected function ResolveConexion(action:String, url:String = null, method:String = null):void {

			super.ResolveConexion( action, url, method );

			if( action == AbstractLoader.SEND ){
				try {
					sendToURL( _request );
				}catch( e:Error ){
					ErrorHandler(
						new SecurityErrorEvent(
							SecurityErrorEvent.SECURITY_ERROR,
							false,
							false,
							e.message
						)
					);
				} super.CompleteHandler( new Event( Event.COMPLETE ) );
			} else {
				_loader = new URLLoader();
				_loader.dataFormat = this.dataFormat;
				ResolveEvents();
				_loader.load( _request );
			}
		}

		override protected function CompleteHandler(e:Event):void {
			_content = _loader.data;
			super.CompleteHandler(e);
		}

	}

}
