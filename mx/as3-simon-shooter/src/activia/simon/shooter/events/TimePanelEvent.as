package activia.simon.shooter.events {
	import flash.events.Event;
	
	
	public class TimePanelEvent extends Event {
		
		public static const START:String = "start";
		public static const RESTART:String = "restart";
		public static const PAUSE:String = "pause";
		public static const RESUME:String = "resume";
		public static const STOP:String = "stop";
		public static const CHANGE_LEVEL:String = "changeLevel";
		
		public function TimePanelEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false) { 
			super(type, bubbles, cancelable);
		} 
		
		public override function clone():Event { 
			return new TimePanelEvent(type, bubbles, cancelable);
		} 
		
		public override function toString():String { 
			return formatToString("TimePanelEvent", "type", "bubbles", "cancelable", "eventPhase"); 
		}
		
	}
	
}