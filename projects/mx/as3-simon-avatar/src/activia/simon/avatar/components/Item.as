package activia.simon.avatar.components{
	import kc.api.IMap;
	import kc.core.KCComponent;
	import kc.core.KCDataLayer;
	import kc.logging.SimpleLog;

	import flash.display.Bitmap;

	/**
	 * @author bernardisa
	 */
	public class Item extends KCComponent{

		private var _base_path:String;
		private var _source:*;

		public function Item(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		public function get source():*{
			return _source;
		}

		public function set source(value:*):void{
			if(value is Bitmap) value = new Bitmap(Bitmap(value).bitmapData);
			_source = value;
		}

		public function get base_path():String{
			return _base_path;
		}

		public function set base_path(value:String):void{
			_base_path = value;
		}

		public function get position_x():int{
			return int(data.item.@x.toString() || 0);
		}

		public function get position_y():int{
			return int(data.item.@y.toString() || 0);
		}
		
		public function get size_w():int{
			return int(data.item.@w.toString() || 0);
		}

		public function get size_h():int{
			return int(data.item.@h.toString() || 0);
		}
		
		public function get mask_id():String {
			return data.item.@mask.toString() || null;
		}
		
		public function get mask_is_up():Boolean {
			if(!mask_id) return false;
			return mask_id.search(/maskup/i) > -1;
		}
		
		public function get mask_name():*{
			var map:IMap = KCDataLayer.collection.value("vectors") as IMap;
			if(mask_id && (map.containsKey(mask_id.toLowerCase()))){
				return map.value(mask_id.toLowerCase());
			} return null; 
		}
		
		public function get mask_x():int{
			return int(data.item.@mask_x.toString() || 0);
		}
		
		public function get mask_y():int {
			return int(data.item.@mask_y.toString() || 0);
		}
		
		override public function toString():String{
			return SimpleLog.string(source, position_x, position_y);
		}
		
	}
	
}
