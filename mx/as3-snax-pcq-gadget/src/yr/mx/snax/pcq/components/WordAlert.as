package yr.mx.snax.pcq.components {
	import kc.core.KCComponent;

	import flash.display.MovieClip;
	import flash.display.SimpleButton;
	import flash.events.Event;
	import flash.text.TextField;

	public class WordAlert extends KCComponent {
		
		private var _text:String; 
		
		public function WordAlert(word:String=null, data:XML=null, autorelease:Boolean=true){
			super(data, autorelease);
			_text = word;
			mouseChildren = false;
			mouseEnabled = true;
			buttonMode = true;
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			word = _text;
		}
		
		public function set word(value:String):void {
			tx_word.text = value || _text || "";	
		}
		
		public function get tx_word():TextField {
			var mc:MovieClip = getChildByName("mcWord") as MovieClip; 
			return mc.getChildByName("txWord") as TextField;
		}
		
		public function get bt_blose():SimpleButton {
			return getChildByName("btClose") as SimpleButton;
		}
		
	}
	
}
