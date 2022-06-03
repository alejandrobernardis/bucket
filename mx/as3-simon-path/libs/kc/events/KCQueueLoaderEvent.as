
package kc.events {
	import flash.events.Event;

	public class KCQueueLoaderEvent extends Event {

		// @const
		
		public static const QUEUE_START:String = "queueStart";		public static const QUEUE_STOP:String = "queueStop";
		public static const QUEUE_CATCH_ERROR:String = "queueCatchError";
		public static const QUEUE_PROGRESS:String = "queueProgress";
		public static const QUEUE_ITEM_COMPLETE:String = "queueItemComplete";
		public static const QUEUE_COMPLETE:String = "queueComplete";
		
		public static const NOT_FOUND:int = -1;
		
		// @protected
		
		protected var _properties:Object;

		// @constructor
		
		public function KCQueueLoaderEvent( type:String, properties:Object = null, bubbles:Boolean=false, cancelable:Boolean=false ) {
			super( type, bubbles, cancelable );
			_properties = properties || new Object();
		}

		// @override
		
		override public function clone():Event {
			return new KCQueueLoaderEvent( this.type, this.bubbles, this.cancelable );
		} 
		
		override public function toString():String {
			return this.formatToString( "QueueLoaderEvent", "type", "bubbles", "cancelable", "eventPhase" ); 
		} 
		
		// @properties
		
		public function get itemIndex():int {
			return _properties.itemIndex || NOT_FOUND;
		}
		
		public function get itemBytesLoaded():int {
			return _properties.itemBytesLoaded || NOT_FOUND;
		}

		public function get itemBytesTotal():int {
			return _properties.itemBytesTotal || NOT_FOUND;
		}
		
		public function get itemProgress():int {
			return _properties.itemProgress || NOT_FOUND;
		}
				
		public function get itemsLoaded():int {
			return _properties.itemsLoaded || NOT_FOUND;
		}
		
		public function get itemsFailed():int {
			return _properties.itemsFailed || NOT_FOUND;
		}
		
		public function get itemsTotal():int {
			return _properties.itemsTotal || NOT_FOUND;
		}
		
		public function get progress():int {
			return _properties.progress || NOT_FOUND;
		}
		
		public function get error():String {
			return _properties.error || null;
		}
		
	}
	
}
