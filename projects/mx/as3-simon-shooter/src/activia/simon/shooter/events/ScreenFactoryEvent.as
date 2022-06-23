package activia.simon.shooter.events {
	import flash.events.Event;
	
	
	public class ScreenFactoryEvent extends Event {
		
		public static const ADD_SCREEN:String = "addScreen";
		public static const REMOVE_SCREEN:String = "removeScreen";
		public static const REPLACE_SCREEN:String = "replaceScreen";
		
		public function ScreenFactoryEvent( type:String, bubbles:Boolean = false, cancelable:Boolean = false ) { 
			super( type, bubbles, cancelable );
		} 
		
		public override function clone():Event { 
			return new ScreenFactoryEvent( type, bubbles, cancelable );
		} 
		
		public override function toString():String { 
			return formatToString( "ScreenFactoryEvent", "type", "bubbles", "cancelable", "eventPhase" ); 
		}
		
	}
	
}