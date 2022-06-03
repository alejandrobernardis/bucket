package yr.mx.snax.pcq.components {
	import kc.api.IBasicButton;
	import kc.api.IKCComponent;
	import kc.core.KCComponent;
	import kc.utils.ClassUtil;

	import flash.display.SimpleButton;
	import flash.events.Event;
	import flash.events.IEventDispatcher;
	import flash.events.MouseEvent;

	public class VideoControlBar extends KCComponent implements IKCComponent {
		
		public function VideoControlBar(data:XML = null, autorelease:Boolean = true) {
			super(data, autorelease);
		}
		
		override protected function $config(e:Event):void {
			super.$config(e);
			ResolveActions();
			button_play.visible = true;
			button_volumen_on.visible = true;
			mc_volumen_bar.addEventListener("change", function(e:Event):void{
				dispatchEvent(e);
			});
		}
		
		override public function purge(...rest):void {
			ResolveActions(true);
			super.purge(rest);
		}
		
		/* Actions */
		
		public function playVideo():void{
			button_play.visible = false;
			button_pause.visible = true;
			dispatchEvent(new Event("play"));
		}
		
		public function pauseVideo():void{
			button_play.visible = true;
			button_pause.visible = false;
			dispatchEvent(new Event("pause"));
		}
		
		public function muteVideo():void{
			button_volumen_on.visible = !button_volumen_on.visible;
			button_volumen_off.visible = !button_volumen_off.visible;
			dispatchEvent(new Event( button_volumen_on.visible ? "unmute" : "mute" ));
		}
		
		/* Helpers */
		
		private function ResolveActions( remove:Boolean = false  ):void {
			
			var element:IEventDispatcher;

			var f:String = ( ! remove )
				? "addEventListener"
				: "removeEventListener";

			for ( var a:uint = 0; a < numChildren; a++ ) {
				if( getChildAt(a) is SimpleButton || getChildAt(a) is  IBasicButton ){
					element = getChildAt(a) as IEventDispatcher;
					element["visible"] = false;
					element[f].apply(
						this,
						[MouseEvent.CLICK, ButtonManager]
					); 
				}
			}
			
		}
		
		private function ResolveButtonName(target:*):String {
			return ( target is SimpleButton ) 
				? target.name 
				: ClassUtil.shortName(target);
		}
		
		private function ButtonManager(e:MouseEvent=null):void {
			var action:String = ResolveButtonName(e.target);
			switch(action){
				case "ControlPlayButton": playVideo(); break;
				case "ControlPauseButton": pauseVideo(); break;
				case "ControlVolumenOnButton": muteVideo(); break;
				case "ControlVolumenOffButton": muteVideo(); break;
			}
		}
		
		/* Properties */
		
		public function get button_play():IBasicButton {
			return getChildByName("btPlay") as IBasicButton;
		}
		
		public function get button_pause():IBasicButton {
			return getChildByName("btPause") as IBasicButton;
		}
		
		public function get button_volumen_on():IBasicButton {
			return getChildByName("btVolumenOn") as IBasicButton;
		}
		
		public function get button_volumen_off():IBasicButton {
			return getChildByName("btVolumenOff") as IBasicButton;
		}
		
		public function get mc_seek_bar():ControlSeekSlider {
			return getChildByName("mcSeekBar") as ControlSeekSlider;
		}
		
		public function get mc_volumen_bar():ControlVolumenSlider {
			return getChildByName("mcVolumenBar") as ControlVolumenSlider; 
		}
		
	}
	
}
