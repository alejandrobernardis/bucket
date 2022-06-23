
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface ICollection extends IIterable, IPurger {
		
		// @properties (r)
		
		function get capacity():int;
		function get availableCapacity():int;
		
		// @methods
		
		function add( value:* ):Boolean;
		function addAll( value:ICollection ):Boolean;
		function clear():void;
		function contains( value:* ):int;
		function containsAll( value:ICollection ):Boolean;
		function copy():ICollection;
		function isEmpty():Boolean;
		function remove( value:* ):Boolean;
		function removeAll( value:ICollection ):Boolean;
		function retainAll( value:ICollection ):Boolean;
		function size():uint;
		function toArray():Array;
		
			
	}
	
}
