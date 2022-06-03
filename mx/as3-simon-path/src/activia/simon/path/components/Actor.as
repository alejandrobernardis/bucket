
package activia.simon.path.components {

	import flash.events.Event;
	import caurina.transitions.Tweener;
	import caurina.transitions.properties.FilterShortcuts;

	import kc.core.KCComponent;

	import flash.display.MovieClip;
	import flash.events.MouseEvent;

	/**
	 * @author bernardisa
	 */
	public class Actor extends KCComponent{

		private var _base_path:String;
		private var _source:MovieClip;

		public function Actor(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
			FilterShortcuts.init();
		}
		
		
		override protected function $config(e:Event):void {
			super.$config(e);
		}

		public function get source():MovieClip{
			return _source;
		}

		public function set source(value:MovieClip):void{
			if(!value) return;
			_source = value;
			_source.buttonMode = true;
			_source.useHandCursor = true;
			_source.mouseEnabled = true;
			reset();
		}

		private function events(remove:Boolean = false):void{
			if(!_source) return;
			if(!remove){
				_source.addEventListener(MouseEvent.CLICK, MouseManager);
				_source.addEventListener(MouseEvent.ROLL_OUT, MouseManager);
				_source.addEventListener(MouseEvent.ROLL_OVER, MouseManager);
			} else{
				_source.removeEventListener(MouseEvent.CLICK, MouseManager);
				_source.removeEventListener(MouseEvent.ROLL_OUT, MouseManager);
				_source.removeEventListener(MouseEvent.ROLL_OVER, MouseManager);
			}
		}
		
		// xml data
		
		public function get data_src():String {
			return base_path + data.@src.toString();
		}
		
		public function get data_id():String {
			return data.@id.toString();
		}
		
		public function get data_name():String {
			return data.@name.toString();
		}
		
		public function get data_x():Number {
			return Number(data.@canvas_x.toString()) || 0;
		}
		
		public function get data_y():Number {
			return Number(data.@canvas_y.toString()) || 0;
		}
		
		public function get data_w():Number {
			var r:Number = Number(data.@canvas_w.toString());
			return (r > 0) ? r : 550;
		}
		
		public function get data_h():Number {
			var r:Number = Number(data.@canvas_h.toString());
			return (r > 0) ? r : 450;
		}
		
		public function reset():void{
			events();
			_source.play();
			Tweener.addTween(_source, {
				_Glow_color:0xff9933,	 
				_Glow_alpha:1,	 
				_Glow_blurX:4,	 
				_Glow_blurY:4,	 
				_Glow_strength:255,	 
				time:.8
			});
		}

		private function MouseManager(event:MouseEvent):void{
			if(event.type == MouseEvent.CLICK){
				events(true);
				_source.stop();
				Tweener.addTween(_source, {
					_Glow_color:0x1de3f8,	 
					_Glow_alpha:1,	 
					_Glow_blurX:8,	 
					_Glow_blurY:8,	 
					_Glow_strength:255,	 
					time:.8
				});
				dispatchEvent(new MouseEvent("clickAction"));
			}else if(event.type == MouseEvent.ROLL_OVER){
				_source.stop();
			}else if(event.type == MouseEvent.ROLL_OUT){
				_source.play();
			}
		}

		public function get base_path():String{
			return _base_path || ""; 
		}

		public function set base_path(value:String):void{
			_base_path = value;
		}
		
	}
	
}
