
package pq.api {
	
	import flash.events.IEventDispatcher;
	
	public interface IConfig extends IEventDispatcher, IPurger {
		
		function get data():XML;
		function get action():String;
		function set action( value:String ):void;		
		function get url():String;
		function set url( value:String ):void;
		function dependency( value:String ):String;
		function load( url:String = null ):void;
		
	}
	
}