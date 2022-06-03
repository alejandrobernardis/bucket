package yr.mx.snax.pcq {
	import flash.net.URLVariables;
	import kc.loaders.TextLoader;
	import kc.logging.SimpleLog;
	import kc.utils.NumberUtil;
	import kc.utils.StringUtil;

	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IEventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.SecurityErrorEvent;
	
	public class VideoWords extends EventDispatcher implements IEventDispatcher {
		
		public static const BLOCK:String = "block";
		public static const UNBLOCK:String = "unblock";
		public static const START:String = "start";
		private const _datetime_url:String = "https://www.resistol.com.mx/snax/rest/service_datetime.py";
		
		private var _views:int;
		private var _count:int;
		private var _word:String;
		
		public function VideoWords() {
			super(this);
			_views = NumberUtil.limits(Math.floor(Math.random()*13), 6, 12);
			_count = 0;
			_word = null;
		}
		
		public function get word():String {
			return _word || "-";
		}

		public function count():void {
			_count++;
			if(_count == _views){
				var db_loader:TextLoader = new TextLoader();
				db_loader.url = _datetime_url;
				db_loader.method = "POST";
				db_loader.variables = new URLVariables();
				db_loader.variables.h = "A!~";
				db_loader.addEventListener(Event.COMPLETE, CompleteDataHandler);
				db_loader.addEventListener(IOErrorEvent.IO_ERROR, ErrorDataHandler);
				db_loader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorDataHandler);
				db_loader.load();
				dispatchEvent(new Event(BLOCK));
			} SimpleLog.print("Views", _count, _views);
		}
		
		private function rdoit(p1:String, p2:String):String {
			var a:int = 0;
			var b:String = new String("");
			var c:String = p1.substring(1);
			for(var d:uint=0; d<(c.length/3); d++){
				var e:uint = d*3;
				var f:String = c.substring(e,e+3);
				b = b + String.fromCharCode(int(f)^p2.charCodeAt(a));
				if(a==p2.length-1){a=0;}else{a++;}
			} return b;
		}

		private function ClearDataHandler(e:*=null):void {
			var t:* = e.target;
			t.addEventListener(Event.COMPLETE, CompleteDataHandler);
			t.addEventListener(IOErrorEvent.IO_ERROR, ErrorDataHandler);
			t.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorDataHandler);
			t.purge();
			t = null;
		}

		private function ErrorDataHandler(e:ErrorEvent):void {
			SimpleLog.log("ERROR", "La estructura de datos no pudo ser cargada.");
			ClearDataHandler(e);
		}
		
		private function CompleteDataHandler(e:Event):void {
			try{
				var a:String = StringUtil.trim(e.target.content);
				SimpleLog.dump(a);
				if(a != "-1"){
					var b:Array = [a.substr(0,1)+a.substr(-36),a.substr(0,a.length-36)];
					_word = rdoit(b[1],rdoit(b[0],b[1]));
					dispatchEvent(new Event(START));
					dispatchEvent(new Event(UNBLOCK));
					SimpleLog.dump(a, b, _word);
				}
			}catch(error:Error){
				SimpleLog.dump(error.errorID, error.name, error.message);
				dispatchEvent(new Event(UNBLOCK));
			} ClearDataHandler(e);
		}

		public function force():void {
			var db_loader:TextLoader = new TextLoader();
			db_loader.url = _datetime_url;
			db_loader.method = "GET";
			db_loader.addEventListener(Event.COMPLETE, CompleteDataHandler);
			db_loader.addEventListener(IOErrorEvent.IO_ERROR, ErrorDataHandler);
			db_loader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorDataHandler);
			db_loader.load();
		}
		
	}
	
}