package{
	import caurina.transitions.Tweener;

	import kc.core.KCComponent;
	import kc.core.KCDataLayer;
	import kc.logging.SimpleLog;
	import kc.utils.ExceptionUtil;

	import flash.display.DisplayObject;
	import flash.display.SimpleButton;
	import flash.events.Event;
	import flash.events.MouseEvent;
	import flash.external.ExternalInterface;
	import flash.net.URLRequest;
	import flash.net.navigateToURL;

	/**
	 * @author @project.author@
	 */
 	public class ApplicationMenu extends KCComponent {
 		
		private var _enabled_menu:Boolean; 
 		private var _tracking:Boolean = true;

		public function ApplicationMenu(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			enabled_menu = false;
			var xml:XML = KCDataLayer.collection.value("application") as XML;
			_data = new XML( xml.child("navigation").toXMLString() );
			Helpers.ResolveActions(this, ButtonsManager);
		}
		
		public function get enabled_menu():Boolean{
			return _enabled_menu;
		}
		
		public function set enabled_menu(value:Boolean):void{
			if(enabled_menu == value) return;
			_enabled_menu = value;
			var item:DisplayObject;
			var list:Array = new Array();
			while(list.length){
				item = getChildByName(list.pop());
				if(item){
					Tweener.addTween(
						item,
						{
							alpha:(enabled_menu) ? 1 : 0,
							time: 1.5,
							transition: "easeOutQuint"
						}
					);
				}
			}
		}

		override public function purge(...rest):void {
			super.purge(rest);
			Helpers.ResolveActions(this, ButtonsManager, true);			
		}
		
		protected function ButtonsManager( e:MouseEvent ):void {
			
			var name:String = Helpers.ResolveButtonName(e.target);
			var action:String = _data.item.(@id == Helpers.ResolveButtonName(e.target)).text();
			
			while(KCDataLayer.scope.content.screens.quantity > 1){
				KCDataLayer.scope.content.rScreen();
			}
			
			if(!action) {
				
				SimpleLog.log("error", "Section:", action, name);
				return;
				
			}else if( action.search( /^screen:\w+$/i ) > -1 ){
				
				SimpleLog.print("Goto > Screen", action);
				
				var section:String = action.replace(/^screen:/i, "");
				
				SimpleLog.print("Goto > Screen > Name", section);
				
				if(_tracking) {
					GoogleAnalytics.hit("common", name);
				}
				
				KCDataLayer.scope.content.cScreen(section);
			
			}else if( action.search( /^popup:\w+$/i ) > -1 ){	
			
				SimpleLog.print("Goto > PopUp", action);
				
				var popup:String = action.replace(/^popup:/i, "");
				
				SimpleLog.print("Goto > PopUp > Name", popup);
				
				if(_tracking) {
					GoogleAnalytics.hit("common", name);
				}
				
				KCDataLayer.scope.content.aScreen(popup);
			
			}else if( action.search( /^http(s)?:/i ) > -1 ){
				
				SimpleLog.print("Goto > Url", action);
				
				if(_tracking) {
					GoogleAnalytics.fhit(action);
				}
				
				navigateToURL(new URLRequest(action), "_blank");
				
			}else if( action.search( /^javascript:/i ) > -1 ){
				
				action = action.replace(/^javascript:/i, "");
				
				SimpleLog.print("JavaScript > Action", action);
				
				if(_tracking) {
					GoogleAnalytics.fhit("js:"+action);
				}
				
				ExternalInterface.call(action);
				
			}
			
			_tracking = true;
			
		}
		
		public function ButtonDispatch(value:String):void {
			_tracking = false;
			getButton(value).dispatchEvent(
				new MouseEvent(
					MouseEvent.CLICK
				)
			);
		}
		
		public function getButton(value:String):SimpleButton {
			try{
				return getChildByName(value) as SimpleButton;
			}catch(e:Error){
				ExceptionUtil.ViewError(e, true);
			}
			return new SimpleButton();
		}

	}
	
}
