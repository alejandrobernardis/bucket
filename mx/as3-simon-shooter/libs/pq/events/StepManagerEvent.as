package pq.events {
	
	import flash.events.Event;

	public class StepManagerEvent extends Event {
		
		public static const BEFORE_CHANGE:String = "beforeChange";
		public static const AFTER_CHANGE:String = "afterChange";
		public static const INTRO_BEGINS:String = "introBegins";
		public static const INTRO_FINISHED:String = "introFinished";
		public static const OUTRO_BEGINS:String = "outroBegins";
		public static const OUTRO_FINISHED:String = "outroFinished";
		
		public function StepManagerEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false) {
			super(type, bubbles, cancelable);
		}
		
	}
	
}