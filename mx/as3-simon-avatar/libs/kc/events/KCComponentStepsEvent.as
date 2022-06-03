
package kc.events {
	import flash.events.Event;

	public class KCComponentStepsEvent extends Event {

		// @const
		
		public static const BEFORE_CHANGE:String = "beforeChange";
		public static const AFTER_CHANGE:String = "afterChange";
		public static const INTRO_BEGINS:String = "introBegins";
		public static const INTRO_FINISHED:String = "introFinished";
		public static const OUTRO_BEGINS:String = "outroBegins";
		public static const OUTRO_FINISHED:String = "outroFinished";
		public static const AVAILABLE:String = "available";   
		
		// @constructor
		
		public function KCComponentStepsEvent( type:String, bubbles:Boolean=false, cancelable:Boolean=false ) {
			super( type, bubbles, cancelable );
		}
		
		// @override
		
		override public function clone():Event { 
			return new KCComponentStepsEvent( this.type, this.bubbles, this.cancelable );
		} 
		
		override public function toString():String { 
			return this.formatToString( "KCComponentStepsEvent", "type", "bubbles", "cancelable", "eventPhase" ); 
		} 
		
	}

}