package yr.mx.snax.pcq {
	import kc.utils.NumberUtil;
	import caurina.transitions.Tweener;

	import kc.api.IBasicButton;
	import kc.api.IKCComponent;
	import kc.core.KCComponent;
	import kc.loaders.TextLoader;
	import kc.logging.SimpleLog;
	import kc.utils.ClassUtil;
	import kc.utils.PurgerUtil;
	import kc.utils.TypeUtil;

	import yr.mx.snax.pcq.components.ControlSeekSlider;
	import yr.mx.snax.pcq.components.VideoControlBar;

	import com.adobe.serialization.json.JSON;
	import com.google.analytics.AnalyticsTracker;
	import com.google.analytics.GATracker;
	import com.google.analytics.core.TrackerMode;

	import flash.display.DisplayObject;
	import flash.display.Loader;
	import flash.display.MovieClip;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.IOErrorEvent;
	import flash.events.MouseEvent;
	import flash.events.SecurityErrorEvent;
	import flash.net.URLRequest;
	import flash.system.ApplicationDomain;
	import flash.system.LoaderContext;
	import flash.system.Security;
	
	public class VideoApplication extends KCComponent implements IKCComponent {
		
		/* Application */
		
		private static const DATA_PATH:String = "./common/data/new_database.txt";
		
		//private static const STATE_UNSTARTED:int = -1;
		private static const STATE_ENDED:int = 0;
		private static const STATE_PLAYING:int = 1;
		private static const STATE_PAUSED:int = 2;
		//private static const STATE_BUFFERING:int = 3;
		//private static const STATE_CUED:int = 5;
		
		private var _player:Object;
		private var _yt_loader:Loader;
		private var _context:LoaderContext;
		private var _external_data:Object;
		private var _current_data:Object;

		private var _video_holder:MovieClip;
		private var _video_loader:IKCComponent;
		private var _video_play_button:IBasicButton;
		private var _video_control_bar:VideoControlBar;
		private var _video_control_bar_status:Boolean;
		
		/* GoogleAnalytics */
		
		private const GA_ID:String = "UA-29364035-2";
		private var _tracker:AnalyticsTracker;
		private var _tracker_list:Array;
		
		/* Application */
		
		public function VideoApplication(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			Security.allowDomain("*");
			Security.allowDomain("*.youtube.com");
			Security.allowDomain("*.ytimg.com");
			Security.allowDomain("localhost");
			
			_context = new LoaderContext(
				true, 
				ApplicationDomain.currentDomain
			);
			
			GoogleAnalyticsCreate();
			
			_video_loader = ClassUtil.getClassInstance("VideoLoader", context.applicationDomain);
			_video_loader.position(stage.stageWidth/2, stage.stageHeight/2);
			_video_loader.play();
			addChild(_video_loader as DisplayObject);
			
			var db_loader:TextLoader = new TextLoader();
			db_loader.url = flash_vars.json_path || DATA_PATH;
			db_loader.method = "GET";
			db_loader.addEventListener(Event.COMPLETE, CompleteDataHandler);
			db_loader.addEventListener(IOErrorEvent.IO_ERROR, ErrorDataHandler);
			db_loader.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorDataHandler);
			db_loader.load();
			
			SimpleLog.dump(flash_vars);
		}

		private function ClearDataHandler(e:*=null):void {
			var t:* = e.target;
			t.addEventListener(Event.COMPLETE, CompleteDataHandler);
			t.addEventListener(IOErrorEvent.IO_ERROR, ErrorDataHandler);
			t.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorDataHandler);
			t.purge();
			t = null;
		}

		private function ErrorDataHandler(e:ErrorEvent):void {
			SimpleLog.log("ERROR", "La estructura de datos no pudo ser cargada.");
			ClearDataHandler(e);
		}
		
		private function RandomElement(coef:Number=4, min:Number=0, max:Number=3):Number {
			var value:Number = Math.floor(Math.random()*coef);
			return NumberUtil.limits(value, 0, 3);
		}
		
		private function RandomList():Array {
			//var letters:Array = [0,"A","B"];
			//letters[RandomElement(3, 0, 2)],
			var letters:Array = ["A","B"];
			var numbres:Array = [0,"i1","i2","i3"];
			return [
				letters[RandomElement(2, 0, 1)],
				numbres[RandomElement(4, 1, 3)],
				numbres[RandomElement()],
				numbres[RandomElement()],
			];
		}

		private function CompleteDataHandler(e:Event):void {
			_external_data = JSON.decode(e.target.content);
			if(_external_data.hasOwnProperty("E")) {
				var list:Array = RandomList();
				if(!_current_data){
					_current_data = _external_data.E;
				} for each (var a:* in list){
					if(a == 0){
						break;
					} _tracker_list.push(a);
					_current_data = _current_data[a];
				} SimpleLog.print('LIST', list);
				create_player();
			} else {
				SimpleLog.log("ERROR", "La estructura de datos no es correcta.");
			}
			ClearDataHandler(e);
			GAHit("data", "load");
		}
		
		/* GoogleAnalytics */
		
		private function GoogleAnalyticsCreate():void {
			_tracker_list = new Array();
			if(!TypeUtil.isBoolean(flash_vars.analytics)) return;
			GATracker.autobuild = false;
			_tracker = new GATracker(this, GA_ID, TrackerMode.BRIDGE);
			_tracker.config.sessionTimeout = 60;
			_tracker.config.conversionTimeout = 180;
			GATracker(_tracker).build();
		}
		
		private function GAHit(level:String, value:String, context:String = "snax-application"):void {
			SimpleLog.log("DEBUG", context, level, value);
			if(!TypeUtil.isBoolean(flash_vars.analytics)) return;
			_tracker.trackEvent(context, level, value);
		}
		
		/* Properties */
		
		public function get context():LoaderContext {
			return _context;
		}
		
		public function get flash_vars():Object {
			if( ! this ) 
				return null;
			if( ! this.stage.loaderInfo.parameters )
				return new Object();
			return this.stage.loaderInfo.parameters;
		}
		
		/* Player */
		
		private function create_player():void {
			_yt_loader = new Loader();
			_yt_loader.contentLoaderInfo.addEventListener(Event.INIT, CompleteYTPlayerHandler);
			_yt_loader.contentLoaderInfo.addEventListener(IOErrorEvent.IO_ERROR, ErrorYTPlayerHandler);
			_yt_loader.contentLoaderInfo.addEventListener(SecurityErrorEvent.SECURITY_ERROR, ErrorYTPlayerHandler);
			_yt_loader.load(new URLRequest("http://www.youtube.com/apiplayer?version=3"));
		}
		
		private function ErrorYTPlayerHandler(e:ErrorEvent):void {
			SimpleLog.log("ERROR", "La estructura de datos no pudo ser cargada.");
		}

		private function CompleteYTPlayerHandler(e:Event):void {
			removeChild(_video_loader as DisplayObject);
			_video_loader = null;
			
			addChild(_yt_loader);
			_yt_loader.content.addEventListener("onReady", PlayerReadyHandler);
			_yt_loader.content.addEventListener("onError", PlayerErrorHandler);
			_yt_loader.content.addEventListener("onStateChange", PlayerStateChangeHandler);
			_yt_loader.content.addEventListener("onPlaybackQualityChange", PlayerVideoPlaybackQualityChangeHandler);
			
			GAHit("player", "api-load");
		}
		
		// ---------------------------------------------------------------------

		private function PurgeButtonOptions():void {
			while(_video_holder.numChildren > 0){
				var _bt:DisplayObject = _video_holder.removeChildAt(0);
				if(_bt.hasEventListener(MouseEvent.CLICK)) 
					_bt.removeEventListener(MouseEvent.CLICK, ClickButtonOptionsHandler);
			}
		}

		private function CreateButtonOptionsHandler(e:Event):void {
			if(!_player) return;
			try{
				if(_player.getCurrentTime() >= _current_data.second_init){
					removeEventListener(Event.ENTER_FRAME, CreateButtonOptionsHandler);
					
					PurgeButtonOptions();
								
					var len:int = -1;
					
					if (_current_data.hasOwnProperty("A") 
						 || _current_data.hasOwnProperty("B")) {
						len = 2;
					} else if (_current_data.hasOwnProperty("i1") 
								|| _current_data.hasOwnProperty("i2") 
								|| _current_data.hasOwnProperty("i3")) {
						len = 3;
					}
					
					function set_button(_data:Object, _len:int):void {
						for (var a:int = 1; a < _len + 1; a++) {
							var _tmp_id:String = (len < 3) ? ((a < 2) ? "A" : "B") : "i" + a;
							try{
								var _tmp:Object = _data[_tmp_id];
								var _button:MovieClip = new MovieClip();
								_button.name = _tmp_id;
								_button.useHandCursor = true;
								_button.buttonMode = true;
								_button.alpha = (flash_vars.buttonsview || _external_data.E.buttonsview) ? 0.1 : 0;
								_button.graphics.beginFill(0xFF0000);
								_button.graphics.drawRect(0, 0, _tmp.w, _tmp.h);
								_button.graphics.endFill();
								_button.x = _tmp.x;
								_button.y = _tmp.y;
								_button.addEventListener(MouseEvent.CLICK, ClickButtonOptionsHandler);
								_video_holder.addChild(_button);
							}catch(error:Error){}
							SimpleLog.print("\tData:", _tmp_id, _tmp.vid);
						}
					} 
					
					if(_current_data.hasOwnProperty("arrows_show") 
						&& _current_data.arrows_show) {
						var arrow_top_left:MovieClip = ClassUtil.getClassInstance("ArrowTopLeft", context.applicationDomain);
						arrow_top_left.x = 275;
						arrow_top_left.y = 65;
						arrow_top_left.play();
						_video_holder.addChild(arrow_top_left);
						var arrow_top_right:MovieClip = ClassUtil.getClassInstance("ArrowTopRight", context.applicationDomain);
						arrow_top_right.x = 712;
						arrow_top_right.y = 65;
						arrow_top_right.play();
						_video_holder.addChild(arrow_top_right);
					}
					
					set_button((len > -1) ? _current_data : _external_data.E, 
							   (len > -1) ? len : 2);
							   
					if (len == -1) {
						_current_data = _external_data.E;
						PurgerUtil.cleanCollection(_tracker_list);
						_tracker_list = new Array();
					}
				}
			}catch(error:Error){}
		}

		private function ClickButtonOptionsHandler(e:MouseEvent):void {
			PurgeButtonOptions();
			removeEventListener(Event.ENTER_FRAME, PlayerProgressHandler);
			
			_current_data = _current_data[e.target.name];
			_player.stopVideo();
			_player.cueVideoById(_current_data.vid);
			
			_video_control_bar.playVideo();
			
			try{
				_tracker_list.push(e.target.name);
				GAHit(e.type, _tracker_list.join("_"));
			}catch(error:Error){ SimpleLog.print("GA", error.message); }
		}
		
		// ---------------------------------------------------------------------
		
		private function MouseMoveHandler(e:MouseEvent):void {
			if(_player.getPlayerState() < STATE_PLAYING) 
				return;
			else if(e.localY < 500 && _video_control_bar_status)
				ControlBarShow(false);
			else if(e.localY > 500 && e.localX < 920 && !_video_control_bar_status)
				ControlBarShow();
		}

		private function ControlBarShow(show:Boolean=true):void {
			_video_control_bar_status = show;
			var value:Number = (show) 
					? stage.stageHeight - _video_control_bar.height
					: stage.stageHeight + 5; 
			Tweener.addTween(
				_video_control_bar, {
					y: value,
					time: 1,
					transition: "easeOutQuint"
				}
			);
		}
		
		private function ControlBarPlayHandler(e:Event):void {
			_video_play_button.visible = false;
			_player.playVideo();
			addEventListener(Event.ENTER_FRAME, CreateButtonOptionsHandler);
			addEventListener(Event.ENTER_FRAME, PlayerProgressHandler);
		}
		
		private function ControlBarPauseHandler(e:Event):void {
			_video_play_button.visible = true;
			_player.pauseVideo();
			ControlBarShow(false);
		}
		
		private function ControlBarMuteHandler(e:Event):void {
			_player.mute();
			_video_control_bar.mc_volumen_bar.enabled = false;
		}
		
		private function ControlBarUnmuteHandler(e:Event):void {
			_player.unMute();
			_video_control_bar.mc_volumen_bar.enabled = true;
		}
		
		private function ControlBarVolumenChangeHandler(e:Event):void {
			try{
				_player.setVolume(_video_control_bar.mc_volumen_bar.volumen);
			}catch(error:Error){}
		}
		
		// ---------------------------------------------------------------------
		
		private function PlayerClickHandler(e:MouseEvent):void {
			switch(_player.getPlayerState()){
				case STATE_PLAYING:
					_video_control_bar.pauseVideo();
				break;
				case STATE_PAUSED:
					_video_control_bar.playVideo();
				break;
			}
		}
		
		private function PlayerReadyHandler(e:Event=null):void {
			stage.addEventListener(Event.MOUSE_LEAVE, function(e:Event):void {
				ControlBarShow(false);
			});
			
			_video_control_bar = new VideoControlBar();
			_video_control_bar.y = stage.stageHeight + 5;
			_video_control_bar.addEventListener("play", ControlBarPlayHandler);
			_video_control_bar.addEventListener("pause", ControlBarPauseHandler);
			_video_control_bar.addEventListener("mute", ControlBarMuteHandler);
			_video_control_bar.addEventListener("unmute", ControlBarUnmuteHandler);
			_video_control_bar.addEventListener("change", ControlBarVolumenChangeHandler);
			addChild(_video_control_bar);
			
			_video_holder = new MovieClip();
			addChild(_video_holder);
			
			_video_play_button = ClassUtil.getClassInstance("VideoPlayButton", context.applicationDomain);
			_video_play_button.visible = false;
			_video_play_button.addEventListener(MouseEvent.CLICK, PlayerClickHandler);
			addChild(_video_play_button as DisplayObject);
			
			var yt:Boolean = TypeUtil.isBoolean(flash_vars.youtube);
			var w:Number = (!yt) ? 970 : 966;
			var h:Number = Math.ceil(w * 9 / 16);
			
			_player = _yt_loader.content;
			_player.addEventListener(MouseEvent.MOUSE_MOVE, MouseMoveHandler);
			_player.addEventListener(MouseEvent.CLICK, PlayerClickHandler);
			_player.setSize(w, h);
			_player.cueVideoById(_current_data.vid);
			
			if(yt){
				_player.x = (stage.stageWidth - w) / 2;
				_player.y = (stage.stageHeight - h) / 2;
				
				var mc_frame:MovieClip = ClassUtil.getClassInstance("VideoFrame", context.applicationDomain) as MovieClip;
				mc_frame.x = stage.stageWidth / 2;
				mc_frame.y = stage.stageHeight / 2;
				addChild(mc_frame);
			}
			
			_video_control_bar.mc_volumen_bar.volumen = _player.getVolume();
			_video_control_bar.playVideo();
			SimpleLog.print("PlayerReadyHandler", _player);
			GAHit("player", "ready");
			
			try{
				//SimpleLog.print("TEST GA", _tracker_list.join("_"));
				GAHit('click', _tracker_list.join("_"));
			}catch(error:Error){ SimpleLog.print("GA", error.message); }
			
		}

		private function PlayerProgressHandler(e:Event=null):void {
			if(!_player) return;
			try{
				var area:int = 437;
				var seek:ControlSeekSlider = _video_control_bar.mc_seek_bar;
				var loaded:Number = _player.getVideoBytesLoaded();
				var total:Number = _player.getVideoBytesTotal();
				var p_loaded:Number = Math.ceil((loaded / total) * 100);
				seek.mc_progress_load.width = Number((area * p_loaded) / 100);
				var current_time:Number = _player.getCurrentTime();
				var duration:Number = _player.getDuration();
				var p_progress:Number = Math.ceil((current_time / duration) * 100);
				seek.mc_progress.width = (area * p_progress) / 100;
				seek.button_drag.x = seek.mc_progress.width;
				if(p_loaded > 99 && p_progress > 99)
					removeEventListener(Event.ENTER_FRAME, PlayerProgressHandler);
			}catch(error:Error){}
		}
		
		private function PlayerStateChangeHandler(e:Event=null):void {
			var action:Number = Number(e["data"]); 
			switch(action){
				case STATE_ENDED: 
					ControlBarShow(false);
					_player.seekTo(_player.getDuration() - _external_data.E.loop);
				break;
			} //SimpleLog.print("PlayerStateChangeHandler", action);
		}
		
		private function PlayerErrorHandler(e:Event=null):void {
			SimpleLog.print("PlayerErrorHandler", e);
		}
		
		private function PlayerVideoPlaybackQualityChangeHandler(e:Event=null):void {
			SimpleLog.print("PlayerVideoPlaybackQualityChangeHandler", e);
		}
		
	}
	
}
