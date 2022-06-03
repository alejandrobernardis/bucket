package{
	import kc.api.IKCComponent;
	import kc.core.KCComponent;
	import kc.events.KCQueueLoaderEvent;
	import kc.utils.NumberUtil;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.ProgressEvent;
	import flash.text.TextField;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class ApplicationPreloader extends KCComponent implements IKCComponent {
		
		private var _scale:String = "scaleX";
		protected var _prefix:String;
		
		public function ApplicationPreloader(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			progress();
		}
		
		public function set scaleMode(value:String):void {
			_scale = ( value != "scaleY" ) ? "scaleX" : "scaleY";
		}
		
		public function label(value:String = "", prefix:String = null):void {
			_prefix = prefix;
			value = (_prefix ? _prefix : "") + value; 
			TextField(getChildByName("txLabel")).htmlText = value;
		}
		
		public function progressEvent(e:*):void {
			if( e is KCQueueLoaderEvent ){
				progress( e.itemProgress );
				label( Math.abs( e.itemIndex ) 
						+ "/" + Math.abs( e.itemsTotal ) 
						+ " - " + NumberUtil.addLeadingZero(e.itemProgress) 
						+ " %");
			}else if( e is ProgressEvent ){
				progress( ( e.bytesLoaded / e.bytesTotal ) * 100 );
			}
		}
		
		public function progress(value:Number = 0):void {
			value = NumberUtil.limits(value, 0, 100, value);
			MovieClip(getChildByName("mcBar"))[_scale] = value / 100;
			label(value.toString(), "cargando... ");
		}
		
	}
}
