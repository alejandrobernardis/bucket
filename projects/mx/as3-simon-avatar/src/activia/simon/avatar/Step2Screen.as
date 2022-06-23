package activia.simon.avatar{
	import kc.events.KCQueueLoaderEvent;
	import activia.simon.avatar.components.ItemsSelector;
	import activia.simon.avatar.components.Simon;

	import kc.core.KCConfig;
	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;

	import flash.events.Event;
	import flash.events.MouseEvent;

	/**
	 * @author bernardisa
	 */
	public class Step2Screen extends BaseScreen{

		private var _simon:Simon;
		private var _queue:Array;

		public function Step2Screen(data:XML = null, autorelease:Boolean = true){
			data = KCDataLayer.collection.value("AVATAR_DATA_LOAD") as XML; 
			super(data, autorelease);
		}

		override protected function $config(e:Event):void{
			super.$config(e);
			
			KCDataLayer.scope.content.menu.user_name = KCDataLayer.collection.value("AVATAR_NAME");
			_queue = new Array();
			
			var list:Array = new Array("hair", "tshirt", "pants");
			var category:String;
			var selector:ItemsSelector;
			var base_path:String = KCConfig.ResolveDependency(data.@path.toString(), KCDataLayer.config.content);
			
			for each(var i:XML in data.items){
				category = i.@category.toString();
				if(list.indexOf(category) > -1){
					selector = new ItemsSelector();
					selector.name = category;
					selector.key = i.@key.toString();
					selector.data = new XML(i.toXMLString());
					selector.base_path = base_path;
					selector.position(int(i.@x.toString()), int(i.@y.toString()));
					selector.addEventListener(KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteQueue);
					_queue.push(selector);
					addChild(selector);
				}
			}
			
			_simon = new Simon();
			_simon.name = "mcSimon";
			_simon.position(300, 104);
			addChild(_simon);
			
			if(_queue.length) CompleteQueue();
		}

		private function CompleteQueue(event:KCQueueLoaderEvent=null):void{
			var selector:ItemsSelector;
			
			if(event){
				selector = event.target as ItemsSelector;
				selector.addEventListener(KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteQueue);
			}
			
			if(_queue.length){
				selector = _queue.pop();
				selector.startup();
			}
		}

		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "PrevButton":
					KCDataLayer.scope.content.cScreen("step1");
					break;
				case "NextButton":
					KCDataLayer.scope.content.cScreen("step3");
					break;
			}
		}
		
	}
	
}
