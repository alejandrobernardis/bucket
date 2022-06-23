
package kc.api {
	import flash.events.IEventDispatcher;

	public interface IKCQueueLoader extends IEventDispatcher, IPurger {
		
		// @properties (wr)
		
		function get verbose():Boolean;
		function set verbose( value:Boolean ):void;
		function get catchExceptions():Boolean;
		function set catchExceptions( value:Boolean ):void;

		// @properties (r)
		
		function get index():int;
		function get capacity():int;
		function get availableCapacity():int;
		function get itemsLoaded():int;
		function get itemsFailed():int;
		function get itemsFailedList():Array;
		
		// @queue
		
		function add( url:String, properties:Object = null ):Boolean;
		function remove( url:String ):Boolean;
		function contains( url:String ):int;
		function clear():void;
		function isEmpty():Boolean;
		function size():int;
		function toArray():Array;
		function dump():void;

		// @content 
		
		function getContent( url:String, remove:Boolean = false ):*;
		function getContentAt( index:int, remove:Boolean = false ):*;
				function getContentAs( url:String, type:*, remove:Boolean = false ):*;		function getContentAsAt( index:int, type:*, remove:Boolean = false ):*;
 
   		// @loader
		
		function start( catchExceptions:Boolean = false, verbose:Boolean = false ):void;
    	function stop():void;
    	function isRunning():Boolean;
    	function isLoaded():Boolean; 
		
	}
	
}
