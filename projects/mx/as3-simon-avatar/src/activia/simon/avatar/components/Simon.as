package activia.simon.avatar.components{
	import kc.api.IMap;
	import kc.core.KCComponent;
	import kc.core.KCDataLayer;
	import kc.utils.StringUtil;

	import flash.display.Bitmap;
	import flash.display.BitmapData;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.geom.Matrix;
	import flash.geom.Rectangle;

	/**
	 * @author bernardisa
	 */
	public class Simon extends KCComponent{
		
		private var _body:Sprite;
		private var _body_hand:Sprite;
		
		private var _body_hair:Sprite;
		private var _body_hair_mask:Sprite;
		private var _body_tshirt:Sprite;
		private var _body_tshirt_mask:Sprite;
		private var _body_accessory_body_mask:Sprite;
		private var _body_pants:Sprite;
		private var _body_pants_mask:Sprite;
		
		private var _body_accessory_hair:Sprite;
		private var _body_accessory_body:Sprite;
		private var _body_accessory_foot:Sprite;

		public function Simon(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		override protected function $config(e:Event):void{
			super.$config(e);
			
			_body = new Sprite();
			_body_hand = new Sprite();
			
			_body_hair = new Sprite(); 
			_body_tshirt = new Sprite();
			_body_pants = new Sprite();
			
			_body_accessory_hair = new Sprite();
			_body_accessory_body = new Sprite();
			_body_accessory_foot = new Sprite();
			
			_body_hair_mask = new Sprite();
			_body_tshirt_mask = new Sprite();
			_body_accessory_body_mask = new Sprite();
			_body_pants_mask = new Sprite();
			
			var list:Array = new Array(
				_body, 
				_body_hair,
				_body_hair_mask,
				_body_pants,
				_body_pants_mask,
				_body_tshirt,
				_body_tshirt_mask,
				_body_accessory_hair, 
				_body_accessory_body, 
				_body_accessory_body_mask,
				_body_accessory_foot, 
				_body_hand
			);
			
			var container:Sprite;
			
			while(list.length){
				container = list.shift() as Sprite;
				addChild(container);
			}
			
			// !~
			onChange();
			
		}

		private function clear(ref:Sprite=null):void {
			var list:Array = (!ref) 
				? new Array(
					_body, 
					_body_hair,
					_body_tshirt, 
					_body_pants,
					_body_accessory_hair, 
					_body_accessory_body, 
					_body_accessory_foot, 
					_body_hand
				) : new Array(ref);
			while(list.length){
				ref = list.shift();
				while(ref.numChildren){
					ref.removeChildAt(0);
				} ref = null;
			}
		}

		private function onChange():void{
			var cfg:XML = new XML(KCDataLayer.collection.value("application").config.simon.toXMLString());
			var item:Bitmap;
			var item_data:*;
			
			var map:IMap = KCDataLayer.collection.value("images") as IMap;
			var sex:String = (KCDataLayer.collection.value("AVATAR_SEX") != "female") ? "male" : "female";
			var skin:int = KCDataLayer.collection.value("AVATAR_SKIN");
			
			var body_value:String = StringUtil.substitute("bm{1}skin0{2}", sex, skin.toString());
			
			if(map.containsKey(body_value.toLowerCase())){
				_body.addChild(map.value(body_value.toLowerCase()) as Bitmap);	
			} 
			
			var hand_value:String = StringUtil.substitute("bmhand0{1}", skin.toString());
			
			if(map.containsKey(hand_value.toLowerCase())){
				item_data = cfg.item.(@id=="hand");
				item = map.value(hand_value.toLowerCase()) as Bitmap;
				item.x = Number(item_data.@x.toString());
				item.y = Number(item_data.@y.toString());
				_body_hand.addChild(item);	
			}
			
			var list:Array = new Array(
				[_body_hair, "AVATAR_HAIR"], 
				[_body_tshirt, "AVATAR_TSHIRT"], 
				[_body_pants, "AVATAR_PANTS"],
				[_body_accessory_hair, "AVATAR_ACCESSORY_HAIR"], 
				[_body_accessory_body, "AVATAR_ACCESSORY_BODY"], 
				[_body_accessory_foot, "AVATAR_ACCESSORY_FOOT"]
			);
			
			var list_item:Array;
			while(list.length){
				list_item = list.shift();
				setElement(list_item[0], list_item[1]);
			}
		}
		
		private function setElement(ref:Sprite, datalayer:String):void {
			try{
				var item:Item = (KCDataLayer.collection.value(datalayer) is Item) 
					? KCDataLayer.collection.value(datalayer)
					: null;
					
				clear(ref);
				
				if(item.size_w != 0) item.source.width = item.size_w;
				if(item.size_h != 0) item.source.height = item.size_h;
				item.source.x = item.position_x;
				item.source.y = item.position_y;
				
				try{
					var container:ItemContainer = ResolveContainerMask(datalayer);
					if(isAccessory(datalayer)){
						clear(container.maskara);
						if(item.mask_name && !item.mask_is_up){
							container.maskara.addChild(item.mask_name);
							container.maskara.x = (item.mask_x != 0) ? item.mask_x : 0; 
							container.maskara.y = (item.mask_y != 0) ? item.mask_y : 0;
							container.container.mask = container.maskara;
						}else{
							container.container.mask = null;
							container.maskara.x = 0; 
							container.maskara.y = 0;
						}
						if(container.maskara_up){
							clear(container.maskara_up);
							if(item.mask_is_up && item.mask_name){
								container.maskara_up.addChild(item.mask_name);
								container.maskara_up.x = (item.mask_x != 0) ? item.mask_x : 0; 
								container.maskara_up.y = (item.mask_y != 0) ? item.mask_y : 0;
								container.container_up.mask = container.maskara_up;
							}else{
								container.container_up.mask = null;
								container.maskara_up.x = 0; 
								container.maskara_up.y = 0;
							}
						}
					}
				}catch(e:*){}
				
				ref.addChild(item.source);
			}catch(e:*){}
		}
		
		private function isAccessory(value:String):Boolean {
			switch(value){
				case "AVATAR_ACCESSORY_HAIR":
				case "AVATAR_ACCESSORY_BODY":
				case "AVATAR_ACCESSORY_FOOT":
					return true;
			} return false;
		}
		
		private function ResolveContainerMask(value:String):ItemContainer {
			switch(value){
				case "AVATAR_ACCESSORY_HAIR": return new ItemContainer(_body_hair, _body_hair_mask);
				case "AVATAR_ACCESSORY_BODY": return new ItemContainer(_body_tshirt, _body_tshirt_mask, _body_accessory_body, _body_accessory_body_mask);
				case "AVATAR_ACCESSORY_FOOT": return new ItemContainer(_body_pants, _body_pants_mask);
			} return null;
		}

		public function refresh():void{
			onChange();
		}
		
		public function draw(vw:int=0, vh:int=0):Bitmap {
			var bounds:Rectangle = this.getBounds( this );
			bounds.width = (vw == 0) ? bounds.width : vw;
			bounds.height = (vh == 0) ? bounds.height : vh;
			var bitmap:BitmapData = new BitmapData( int( bounds.width + 0.5 ), int( bounds.height + 0.5 ), true, 0 );
			bitmap.draw( this, new Matrix(1,0,0,1,-bounds.x,-bounds.y) );
			return new Bitmap(bitmap);
		}
		
	}
	
}


import flash.display.Sprite;

internal class ItemContainer{

	private var _container:Sprite;
	private var _maskara:Sprite;
	private var _container_up:Sprite;
	private var _maskara_up:Sprite;

	public function ItemContainer(container:Sprite, maskara:Sprite, container_up:Sprite=null, maskara_up:Sprite=null){
		_container = container;
		_maskara = maskara;
		_container_up = container_up;
		_maskara_up = maskara_up;
	}

	public function get container():Sprite{
		return _container;
	}

	public function get maskara():Sprite{
		return _maskara;
	}
	
	public function get container_up():Sprite{
		return _container_up;
	}
	
	public function get maskara_up():Sprite{
		return _maskara_up;
	}
	
}
