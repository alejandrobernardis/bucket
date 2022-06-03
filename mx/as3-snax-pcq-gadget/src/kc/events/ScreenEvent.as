
package kc.events {
	import flash.events.Event;

	public class ScreenEvent extends Event {

		// @const
		
		public static const ADD_SCREEN:String = "addScreen";
		public static const REPLACE_SCREEN:String = "replaceScreen";
		public static const REMOVE_SCREEN:String = "removeScreen";
		
		// @constructor
		
		public function ScreenEvent( type:String, bubbles:Boolean=false, cancelable:Boolean=false ) {
			super( type, bubbles, cancelable );
		}
		
		// @override
		
		override public function clone():Event {
			return new ScreenEvent( this.type, this.bubbles, this.cancelable );
		} 
		
		override public function toString():String {
			return this.formatToString( "ScreenEvent", "type", "bubbles", "cancelable", "eventPhase" ); 
		} 
		
	}
	
}
