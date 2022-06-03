package activia.simon.avatar{
	import activia.simon.avatar.components.Simon;

	import kc.core.KCDataLayer;
	import kc.utils.ClassUtil;
	import kc.utils.RegExpUtil;
	import kc.utils.StringUtil;

	import com.adobe.images.PNGEncoder;

	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.net.FileReference;

	/**
	 * @author bernardisa
	 */
	public class Step4Screen extends BaseScreen {
		
		private var _simon:Simon;
		private var _file:FileReference;

		public function Step4Screen(data : XML = null, autorelease : Boolean = true) {
			super(data, autorelease);
		}
		
		
		override protected function $config(e:Event):void{
			super.$config(e);
			KCDataLayer.scope.content.menu.user_name = KCDataLayer.collection.value("AVATAR_NAME");
			
			_simon = new Simon();
			_simon.name = "mcSimon";
			_simon.position(300, 104);
			addChild(_simon);
		}
		
		override protected function ButtonsManager(e:MouseEvent):void {
			var name:String = Helpers.ResolveButtonName(e.target);
			GoogleAnalytics.hit(ClassUtil.shortName(this), name);
			switch(name){
				case "DownloadButton":
					download();
				break;
				case "DownloadIMButton":
					download(0, 250);
				break;
				case "SendToFriendButton":
					
				break;
				case "PrevButton":
					KCDataLayer.scope.content.cScreen("step3");
				break;
				case "NextButton":
					KCDataLayer.scope.content.cScreen("step5");
				break;
			}
		}

		private function download(vw:int=0, vh:int=0):void {
			var user_name:String = String(
				KCDataLayer.collection.value("AVATAR_NAME")
			).replace(RegExpUtil.PATTERN_WHITE_SPACE, "_");
			
			var image_name:String = (vw == 0 && vh == 0) 
				? "{1}_{2}.png" 
				: "{1}_im_{2}.png";
			
			_file = new FileReference();
			_file.save(
				PNGEncoder.encode(
					_simon.draw(vw, vh).bitmapData
				), 
				StringUtil.substitute(
					image_name, 
					StringUtil.isEmpty(user_name) ? "image" : user_name, 
					new Date().getTime().toString()
				)
			);
		} 
		
	}
}
