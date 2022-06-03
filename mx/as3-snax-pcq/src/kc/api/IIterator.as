
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IIterator extends IPurger {
		
		// @properties (r)
		
		function get index():int;
		
		// @methods
	
		function hasNext():Boolean;
		function next():*;
		function peek():*;
		function remove():void;					function reset():void;			
		function size():int;
		function value():*;
		
		function toArray():Array;
		
	}
	
}
