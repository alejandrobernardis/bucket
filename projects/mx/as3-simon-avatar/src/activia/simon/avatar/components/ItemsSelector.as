package activia.simon.avatar.components{
	import kc.api.IMap;
	import kc.api.IBasicButton;
	import kc.core.KCComponent;
	import kc.core.KCDataLayer;
	import kc.core.KCQueueLoader;
	import kc.events.KCQueueLoaderEvent;
	import kc.logging.SimpleLog;
	import kc.utils.ClassUtil;
	import kc.utils.ExceptionUtil;

	import flash.display.MovieClip;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.MouseEvent;
	import flash.events.SecurityErrorEvent;
	import flash.text.TextField;

	/**
	 * @author bernardisa
	 */
	public class ItemsSelector extends KCComponent{
		
		private var _key:String;
		private var _base_path:String;
		private var _items:SimpleCircularQueue;
		private var _items_list:KCQueueLoader;
		private var _item_left:ItemSelector;
		private var _item_right:ItemSelector;
		
		public function ItemsSelector(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}
		
		override public function purge(...rest):void{
			try{
				
				if(_items_list.isRunning()){
					_items_list.stop();
				}
				
				Helpers.ResolveActions(this, ButtonsManager, true);
				_items_list.purge();
				_base_path = null;
				_items_list = null;
				_item_left = null;
				_item_right = null;
			}catch(e:*){}
			super.purge(rest);
		}
			
		override protected function $config(e:Event):void{
			super.$config(e);
			Helpers.ResolveActions(this, ButtonsManager);
			
			ButtonsEnabled(false);
			
			_item_left = new ItemSelector();
			_item_left.position(78, -38);
			addChild(_item_left);
			
			_item_right = new ItemSelector();
			_item_right.position(508, -38);
			addChild(_item_right);
			
		}
		
		public function startup():void {
			_items_list = new KCQueueLoader(64);
			_items_list.addEventListener( KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteAssetsHandler );
			_items_list.addEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, ProgressHandler );
			_items_list.addEventListener( IOErrorEvent.IO_ERROR, ErrorAssetsHandler );
			_items_list.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorAssetsHandler );
			
			for each(var i:XML in data.item){
				_items_list.add(
					base_path + i.@src.toString(), {
						key: i.@id.toString(),
						context: KCDataLayer.scope.context
					}
				);
			}
			
			if( _items_list.size() > 0 ){
				_items_list.start();
			}else{
				this.visible = false;
				dispatchEvent(new KCQueueLoaderEvent(KCQueueLoaderEvent.QUEUE_COMPLETE));
				SimpleLog.print(this.name, "Size: ", _items_list.size());
			}
		}
		
		// --
		
		protected function ButtonsEnabled(value:Boolean=true):void {
			for(var a:int=0; a<numChildren; a++){
				if(getChildAt(a) is IBasicButton){
					IBasicButton(getChildAt(a)).visible = value;
				}
			}
		}
		
		protected function ButtonsManager(e:MouseEvent):void {
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "ArrowLeftButton":
					_items.prev;
					AssetsManager();
				break;
				case "ArrowRightButton": 
					_items.next;
					AssetsManager();
				break;
			}
		}
		
		protected function AssetsManager(init:Boolean=false):void {
			try{
				var item:Item;
				var map:IMap = KCDataLayer.collection.value("AVATAR_DATA_CONFIG");
				
				if(init && map.containsKey(key)){
					_items.index = map.value(key);
				}else{
					map.add(key, _items.index);
				}
				
				item = (KCDataLayer.collection.value(key) is Item) 
					? KCDataLayer.collection.value(key) as Item
					: new Item();
				
				item.base_path = _base_path;
				
				if(_items.element is MovieClip){
					item.data = new XML();
					item.source = new MovieClip();
				}else{
					item.data = new XML("<recordset>"+data.item.(@id==_items.element.key).toXMLString()+"</recordset>");
					item.source = _items.element.loader.content;
				}
				
				map.update(key, _items.index);
				KCDataLayer.collection.update("AVATAR_DATA_CONFIG", map);
				KCDataLayer.collection.update(key, item);
				
				try{if(parent.getChildByName("mcSimon") is Simon){
					Simon(parent.getChildByName("mcSimon")).refresh();
				}}catch(e:*){}
				
			}catch(e:*){}
			
			try{_item_left.addChild(
				(_items.prevElement is MovieClip) 
					? _items.prevElement
					: _items.prevElement.loader.content
			);}catch(e:*){}
			
			try{_item_right.addChild(
				(_items.nextElement is MovieClip) 
					? _items.nextElement
					: _items.nextElement.loader.content
			);}catch(e:*){}
			
		}
		
		// --
		
		protected function ProgressHandler(e:*):void {
			if( e is KCQueueLoaderEvent ){
				status.text = "Cargando: " + Math.abs( e.itemIndex ) 
							+" de "+ Math.abs( e.itemsTotal ) 
							+ " : " + e.itemProgress + "%"; 
			}
		}
		
		protected function ClearAssetsHandlers():void {
			if(!_items_list) return;
			_items_list.removeEventListener( KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteAssetsHandler );
			_items_list.removeEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, ProgressHandler );
			_items_list.removeEventListener( IOErrorEvent.IO_ERROR, ErrorAssetsHandler );
			_items_list.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorAssetsHandler);
		}

		protected function CompleteAssetsHandler(e:KCQueueLoaderEvent):void {
			SimpleLog.print(this.name, "complete", 
				_items_list.itemsLoaded, 
				_items_list.itemsFailed, 
				_items_list.itemsFailedList
			); 
			
			dispatchEvent(new KCQueueLoaderEvent(KCQueueLoaderEvent.QUEUE_COMPLETE));
			
			_items = new SimpleCircularQueue(
				new Array(new MovieClip()).concat(_items_list.toArray()));
				
			status.text = "";
			
			AssetsManager(true);
			ButtonsEnabled();
			ClearAssetsHandlers();
		}

		protected function ErrorAssetsHandler(e:ErrorEvent):void {
			ExceptionUtil.ViewError(e);
			ClearAssetsHandlers();
		}
		
		// --

		public function get base_path():String{
			return _base_path;
		}

		public function set base_path(value:String):void{
			_base_path = value;
		}
		
		public function get key():String{
			return _key;
		}

		public function set key(value:String):void{
			_key = value;
		}
		
		public function get status():TextField {
			return TextField(getChildByName("txStatus"));
		}
		
	}
	
}
import kc.tda.SimpleCollection;

internal class SimpleCircularQueue extends SimpleCollection {
	
	private var _index:int;

	public function SimpleCircularQueue( source:Array = null, capacity:int = undefined ){
		super(capacity);
		this.source = source;
	}
	
	public function set source(value:Array):void {
		if(!value) return;
		_records = value;
		_index = 0;
	}

	public function get element():*{
		if( isEmpty() ) return null;
		return _records[_index];
	}

	public function get next():*{
		if(!hasNext()){
			_index = 0;
		}else{
			_index++;
		} return element;
	}
	
	public function get nextElement():*{
		if(!hasNext()){
			return _records[0];
		} return _records[_index+1];
	}
	
	public function get prev():*{
		if(!hasPrev()){
			_index = size()-1;
		}else{
			_index--;
		} return element;
	}

	public function get prevElement():*{
		if(!hasPrev()){
			return _records[size()-1];
		} return _records[_index-1];
	}

	public function get index():int{
		return _index;
	}

	public function set index(value:int):void{
		_index = value;
	}
	
	public function get prevIndex():int{
		if(!hasPrev()){
			return size()-1;
		} return _index-1;
	}

	public function get nextIndex():int{
		if(!hasNext()){
			return 0;
		} return _index+1;
	}
	
	public function seek(value:int):*{
		index = value;
		return element;
	}
	
	public function seekFirst():*{
		return seek(0);
	}
	
	public function seekLast():*{
		return seek(size() - 1);
	} 
	
	public function hasNext():Boolean{
		return (_index < (size() - 1));
	}
	
	public function hasPrev():Boolean{
		return (_index > 0);
	}
	
}

