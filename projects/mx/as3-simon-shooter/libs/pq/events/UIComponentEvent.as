
package pq.events {
	
	import flash.events.Event;

	public class UIComponentEvent extends Event {
		
		public static const ENABLED:String 		= "enabled";
		public static const CHANGE_DATA:String 	= "changeData";
		
		public function UIComponentEvent( type:String, bubbles:Boolean=false, cancelable:Boolean=false ) {
			super( type, bubbles, cancelable );
		}
		
	}
	
}