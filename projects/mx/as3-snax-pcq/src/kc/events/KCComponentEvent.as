
package kc.events {
	import flash.events.Event;

	public class KCComponentEvent extends Event {
		
		// @const
		
		public static const ENABLED:String = "enabled";
		public static const DISABLED:String = "disabled";
		public static const DATA_CHANGE:String = "dataChange";
		
		// @constructor
		
		public function KCComponentEvent( type:String, bubbles:Boolean=false, cancelable:Boolean=false ) {
			super( type, bubbles, cancelable );
		}
		
		// @override
		
		override public function clone():Event {
			return new KCComponentEvent( this.type, this.bubbles, this.cancelable );
		} 
		
		override public function toString():String {
			return this.formatToString( "KCComponentEvent", "type", "bubbles", "cancelable", "eventPhase" ); 
		} 
		
	}
	
}