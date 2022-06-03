
package activia.simon.path {

	import kc.utils.PurgerUtil;
	import activia.simon.path.components.Actor;
	import activia.simon.path.components.PromptDetail;

	import caurina.transitions.Tweener;

	import kc.core.KCConfig;
	import kc.core.KCDataLayer;
	import kc.logging.SimpleLog;
	import kc.utils.ClassUtil;
	import kc.utils.StringUtil;

	import flash.display.MovieClip;
	import flash.events.Event;
	import flash.events.MouseEvent;


	/**
	 * @author bernardisa
	 */
	public class Step1Screen extends BaseScreen{
		
		private var _time_line:MovieClip;
		private var _actor:Actor;
		private var _actors_list:Array;
		private var _prompt_detail:PromptDetail;

		public function Step1Screen(data:XML = null, autorelease:Boolean = true){
			super(data, autorelease);
		}

		override protected function $config(e:Event):void{
			super.$config(e);
			ApplicationContent(KCDataLayer.scope.content).animate_ui();
			
			_time_line = ClassUtil.getClassInstance("AssetTimeLine");
			
			addChild(_time_line);
			setChildIndex(_time_line, 1);
			
			var actor:Actor;
			var actor_item:*;
			var actor_data:*;
			var actor_param:String = "name";
			_actors_list = new Array();
			
			var data_xml:XML = new XML(KCDataLayer.collection.value("applicationAssets").items.toXMLString());
			var data_base_path:String = KCConfig.ResolveDependency(data_xml.@path.toString(), KCDataLayer.config.content);
			
			for(var a:int=0; a<_time_line.numChildren; a++){
				actor_item = _time_line.getChildAt(a);
				actor_data = data_xml.item.(@[actor_param]==String(actor_item.name.toString()));
				if(actor_item is MovieClip && !StringUtil.isEmpty(actor_data.toXMLString())){
					actor = new Actor();
					actor.data = new XML(actor_data.toXMLString());
					actor.base_path = data_base_path;
					actor.source = actor_item;
					actor.addEventListener("clickAction", ButtonManagerAssets);
					_actors_list.push(actor);
				}
			}			
		}

		private function ButtonManagerAssets(event:MouseEvent):void{
			
			SimpleLog.dump(event.target);
			
			if(_actor) 
				_actor.reset();
			
			_actor = event.target as Actor;
			
			if(_prompt_detail){
				removeChild(_prompt_detail);
				_prompt_detail.removeEventListener(Event.CLOSE, CloseHandler);
				_prompt_detail = null;
			}
				
			_prompt_detail = new PromptDetail();
			_prompt_detail.addEventListener(Event.CLOSE, CloseHandler);
			_prompt_detail.bg_width = _actor.data_w;
			_prompt_detail.bg_height = _actor.data_h;
			_prompt_detail.x = _actor.data_x;
			_prompt_detail.y = _actor.data_y;
			_prompt_detail.image = _actor.data_src;
			
			addChild(_prompt_detail);
			
		}

		private function CloseHandler(event:Event):void{
			if(_actor) {
				_actor.reset();
				_actor = null;
			}
			
			if(_prompt_detail){
				_prompt_detail.removeEventListener(Event.CLOSE, CloseHandler);
				_prompt_detail = null;
			}
		}

		override public function purge(...rest):void{
			try{
				PurgerUtil.cleanCollection(_actors_list);
				_time_line = null;;
				_actor = null;
				_actors_list = null;
				_prompt_detail = null;
			}catch(e:*){}
			super.purge(rest);
		}

		override protected function ButtonsManager(e:MouseEvent):void{
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "InstructionsButton": 
					KCDataLayer.scope.content.aScreen("instructions"); 
				break;
				case "ExitButton": 
					KCDataLayer.scope.content.aScreen("exit"); 
				break;
				case "NextButton":
					var ww:Number = (_time_line.width-25); 
					var next_x:int = ((_time_line.x-(ww/6))<(750-ww))
						? -1764
						: _time_line.x-(ww/6);
					Tweener.addTween(
						_time_line, {
							x: next_x,
							time: 1.5,
							transition: "easeOutQuint"
						}
					);
					
				break;
				case "PrevButton":
					var prev_x:int = ((_time_line.x+(_time_line.width/6
					))>0)
						? 0 
						: _time_line.x+(_time_line.width/6);
					Tweener.addTween(
						_time_line, {
							x:prev_x,
							time: 1.5,
							transition: "easeOutQuint"
						}
					);
				break;
			}
		}
		
	}
}



