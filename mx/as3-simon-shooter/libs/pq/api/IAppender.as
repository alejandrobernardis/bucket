
package pq.api {
	
	import pq.log.Appender;
	
	public interface IAppender {
		
		function send( value:Appender ):void;
		function serialize( value:*, depth:uint = 0, ...rest ):String;
		function toString():String;
		
	}
	
}