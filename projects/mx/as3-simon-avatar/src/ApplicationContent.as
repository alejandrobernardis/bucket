package {
	import caurina.transitions.Tweener;

	import kc.api.IMap;
	import kc.api.IScreen;
	import kc.api.IScreenContainer;
	import kc.core.KCClassFactory;
	import kc.core.KCDataLayer;
	import kc.logging.SimpleLog;
	import kc.tda.SimpleMap;
	import kc.ui.screens.ScreenContainer;
	import kc.utils.ClassUtil;
	import kc.utils.StringUtil;

	import flash.display.MovieClip;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.net.URLRequest;
	import flash.net.navigateToURL;
	import flash.system.ApplicationDomain;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class ApplicationContent extends Sprite {

		// @variables

		protected static var $screensHelper:IMap;
		
		protected var _isInitialized:Boolean;
		protected var _isHomePage:Boolean;
		
		protected var _uiScreens:IScreenContainer;
		protected var _uiMenu:ApplicationMenu;
		protected var _uiFooter:ApplicationFooter;
		protected var _uiBackground:ApplicationBackground;
		
		protected var _events_list:IMap;

		// @constructor

		public function ApplicationContent() {

			super();

			// !~

			$screensHelper = new SimpleMap( 32 );
			$screensHelper.add("appmenu","Menu");
			$screensHelper.add("appfooter","Footer");
			$screensHelper.add("appbackground","Background");
			
			// --
			
			$screensHelper.add("home","HomeScreen");
			$screensHelper.add("exit","ExitScreen");
			$screensHelper.add("instructions","InstructionsScreen");
			$screensHelper.add("step1","Step1Screen");
			$screensHelper.add("step2","Step2Screen");
			$screensHelper.add("step3","Step3Screen");
			$screensHelper.add("step4","Step4Screen");
			$screensHelper.add("step5","Step5Screen");
			
			// Extras!
			
			$screensHelper.add("camera","CameraScreen");
			
			// !~
			
			GoogleAnalytics.BlackList = new Array("");
			
			// Misc
			
			KCDataLayer.collection.add("SESSION", false);
			KCDataLayer.collection.add("SESSION_DATA", new XML());
			KCDataLayer.collection.add("SESSION_PAGE", "");
			KCDataLayer.collection.add("SESSION_XSRF", KCDataLayer.getFlashVar("ref")||"");
			KCDataLayer.collection.add("FBUID", KCDataLayer.getFlashVar("fbUid")||1469798294);
			KCDataLayer.collection.add("FBUSERNAME", KCDataLayer.getFlashVar("fbUsername")||"");
			KCDataLayer.collection.add("FBFULLNAME", KCDataLayer.getFlashVar("fbFullname")||"Alejandro M. Bernardis");
			KCDataLayer.collection.add("AVAILABLE", int(KCDataLayer.getFlashVar("available"))||0);
			KCDataLayer.collection.add("COUNT", int(KCDataLayer.getFlashVar("count"))||0);
			
			// Avatar
			
			KCDataLayer.collection.add("AVATAR_NAME", "");
			KCDataLayer.collection.add("AVATAR_SEX", "");
			KCDataLayer.collection.add("AVATAR_SKIN", 0);
			KCDataLayer.collection.add("AVATAR_HAIR", "");
			KCDataLayer.collection.add("AVATAR_TSHIRT", "");
			KCDataLayer.collection.add("AVATAR_PANTS", "");
			KCDataLayer.collection.add("AVATAR_ACCESSORY_HAIR", "");
			KCDataLayer.collection.add("AVATAR_ACCESSORY_BODY", "");
			KCDataLayer.collection.add("AVATAR_ACCESSORY_FOOT", "");
		
			KCDataLayer.collection.add("AVATAR_DATA_LOAD", "");
			KCDataLayer.collection.add("AVATAR_DATA_CONFIG", new SimpleMap());
			
			// Callback			

			KCDataLayer.collection.add("callback", "");
			clearCallback();
			
			// !~

			if(!stage){
				addEventListener(Event.ADDED_TO_STAGE, init);
			}else{
				init();
			}

		}
		
		public static function reset_avatar_data():void {
			KCDataLayer.collection.update("AVATAR_NAME", "");
			KCDataLayer.collection.update("AVATAR_SEX", "");
			KCDataLayer.collection.update("AVATAR_SKIN", 0);
			reset_avatar_config();
		}
		
		public static function reset_avatar_config():void {
			KCDataLayer.collection.update("AVATAR_HAIR", "");
			KCDataLayer.collection.update("AVATAR_TSHIRT", "");
			KCDataLayer.collection.update("AVATAR_PANTS", "");
			KCDataLayer.collection.update("AVATAR_ACCESSORY_HAIR", "");
			KCDataLayer.collection.update("AVATAR_ACCESSORY_BODY", "");
			KCDataLayer.collection.update("AVATAR_ACCESSORY_FOOT", "");
			KCDataLayer.collection.update("AVATAR_DATA_LOAD", "");
			KCDataLayer.collection.update("AVATAR_DATA_CONFIG", new SimpleMap());
		}

		// @prepertie (r)

		public static function get screensHelper():IMap {
			return $screensHelper;
		}

		public static function getScreens(value:String):* {

			value = value.toLowerCase();

			if( ! $screensHelper.containsKey(value) ) {
				return null;
			}

			return new KCClassFactory(
				ClassUtil.getClass(
					$screensHelper.value(value),
					ApplicationDomain.currentDomain
				)
			).newInstance();

		}

		public function get isInitialized():Boolean {
			return _isInitialized;
		}

		public function get screen():IScreen {
			return _uiScreens.content;
		}

		public function get screens():IScreenContainer {
			return _uiScreens;
		}
		
		public function get menu():ApplicationMenu {
			return _uiMenu;
		}

		public function get background():ApplicationBackground {
			return _uiBackground;
		}

		// @methods

		public function init(...rest):void {

			if( _isInitialized ) return;
			_isInitialized = true;

			SimpleLog.print( "ApplicationContent: initialized." );
			
			_uiBackground = getScreens("appbackground");
			addChild(_uiBackground);
			_uiBackground.change();
			
			_uiMenu = getScreens("appmenu");
			_uiMenu.y = -100;
			_uiMenu.alpha = 0;
			addChild(_uiMenu);
			
			_uiScreens = new ScreenContainer(4);
			addChild(_uiScreens as MovieClip);
			
			_uiFooter = getScreens("appfooter");
			_uiFooter.alpha = 1;
			addChild(_uiFooter);
		
			_isHomePage = true;
			animate_menu();
			
			if( rest[0] is Event ){
				removeEventListener(Event.ADDED_TO_STAGE, init);
			}
			
			SimpleLog.debuger = true;
			_uiMenu.ButtonDispatch("btHome");
			
		}
		
		private function animate_menu():void{
			if(_isHomePage){
				Tweener.addTween(
					_uiMenu,
					{
						y:0,
						time: 1.5,
						transition: "easeOutQuint"
					}
				);
				Tweener.addTween(
					_uiMenu,
					{
						alpha:1,
						time: 1.5,
						transition: "easeOutQuint"
					}
				);
			}
			_isHomePage = false;
		}
		

		public function destroy():void {
			if( ! _isInitialized ) return;
			_isInitialized = false;
		}
		
		public function shareFacebook(sShareTitle:String = "", sURLToShare:String = ""):void {
			var url:URLRequest = new URLRequest("http://www.facebook.com/sharer.php?u=" + sURLToShare + "&t=" + sShareTitle);
			navigateToURL(url, "_blank");
		}

		public function shareTwitter( sShareTitle:String = "", sURLToShare:String = "" ):void {
			var url:URLRequest = new URLRequest("https://twitter.com/?status=" + sShareTitle + " " + sURLToShare);
			navigateToURL(url, "_blank");
		}
		
		public function share2Twitter( sText:String, sURL:String="", sVia:String="" ):void {
			sURL = (StringUtil.isEmpty(sURL)) ? "" : "&url=" + sURL;
			sVia = (StringUtil.isEmpty(sVia)) ? "" : "&via=" + sVia;
			var url:URLRequest = new URLRequest("http://twitter.com/intent/tweet?text=" + sText + sURL + sVia);
			navigateToURL(url, "_blank");
		}
		
		
		public function clearCallback():void {
			KCDataLayer.collection.update("callback", function():void {trace("Callback");});
		}
		
		public function setCallback(ref:*, value:String, args:Array):void {
			KCDataLayer.collection.update("callback", [ref, value, args]);
		}
		
		public function applyCallback():void {
			var ref:Array = KCDataLayer.collection.value("callback");
			var s:* = ref[0];
			var f:String = ref[1];
			var a:Array = ref[2];
			s[f].apply(s, a);
		}
		
		public function AddEvents(key:String, events:Array=null):void{
			if(! events) return;
			if(! _events_list) _events_list = new SimpleMap();
			
			_events_list.add(key, events);
			
			for(var a:int=0; a<events.length; a++) 
				_uiScreens.content.addEventListener(events[a].type, events[a].listener);
		}
		
		public function RemoveEvents(value:String):void{
			if(StringUtil.isEmpty(value) || ! _events_list) return;
			var key:String = $screensHelper.key(value);
			
			if (key){
				var events:Array = _events_list.value(key) as Array;
				
				for(var a:int=0; a<events.length; a++)
					_uiScreens.content.addEventListener(events[a].type, events[a].listener);
					
				_events_list.remove(key);
			}
		}
		
		public function aScreen(value:String, events:Array=null):void {			
			
			if(_uiScreens.quantity > 0){
				_uiScreens.content.enabled = false;
			}
			
			_uiScreens.add(getScreens(value));
			_uiScreens.content.visible=true;
			_uiScreens.content.alpha=0;
			
			AddEvents(value, events);
			
			Tweener.addTween(
				_uiScreens.content,
				{
					alpha:1,
					time: 1.5,
					transition: "easeOutQuint"
				}
			);
			
		}

		public function cScreen(value:String, events:Array=null):void {
			
			if(_uiScreens.content){
				_uiScreens.content.enabled = true;
			}
			
			_uiScreens.replace(getScreens(value));
			_uiScreens.content.visible = true;
			_uiScreens.content.alpha = 0;
			_uiScreens.content.y = _uiScreens.content.height;
			_uiScreens.content.filters = [];
			
			AddEvents(value, events);
			
			Tweener.addTween(
				_uiScreens.content,
				{
					y:0,
					time: 1.5,
					transition: "easeOutQuint"
				}
			);
			
			Tweener.addTween(
				_uiScreens.content,
				{
					alpha:1,
					time: 1.5,
					transition: "easeOutQuint"
				}
			);
			
		}

		public function rScreen():void {
			RemoveEvents(ClassUtil.shortName(_uiScreens.content));
			
			_uiScreens.remove();
			
			if(_uiScreens.content){
				_uiScreens.content.enabled = true;
			}
			
		}

	}

}
