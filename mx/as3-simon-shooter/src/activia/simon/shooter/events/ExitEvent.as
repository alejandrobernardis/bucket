package activia.simon.shooter.events {
	import flash.events.Event;
	
	
	public class ExitEvent extends Event {
	
		public static const YES:String = "yes";
		public static const NO:String = "no";
		
		public function ExitEvent(type:String, bubbles:Boolean=false, cancelable:Boolean=false) { 
			super(type, bubbles, cancelable);			
		} 
		
		public override function clone():Event { 
			return new ExitEvent(type, bubbles, cancelable);
		} 
		
		public override function toString():String { 
			return formatToString("Exit", "type", "bubbles", "cancelable", "eventPhase"); 
		}
		
	}
	
}