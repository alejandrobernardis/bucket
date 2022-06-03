package kc.api {

	public interface IKCQueueLoaderItem extends IPurger {
		
		// @properties (r)
		
		function get uid():String;		function get key():String;
		function get url():String;
		function get loader():ILoader;
		
		// @methods
		
		function isValid():Boolean;
		
	}
	
}
