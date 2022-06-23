
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IHistory extends ICollection {
		
		// @poperties (rw)
		
		function get index():int;
		function set index(value:int):void;

		// @methods
		
		function element():*;
		function back():*;
		function forward():*;
		function seek(value:int):*;
		function seekFirst():*;
		function seekLast():*;
		
		// @helper
		
		function hasBack():Boolean;
		function hasForward():Boolean;
			
	}
	
}
