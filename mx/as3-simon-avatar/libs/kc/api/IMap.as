
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IMap extends IIterable, IPurger {
		
		// @properties (r)
		
		function get capacity():int;
		function get availableCapacity():int;
		
		// @methods
		
		function add( key:*, value:* ):Boolean;
		function addAll( value:IMap ):Boolean;
		function containsKey( key:* ):Boolean;
		function containsValue( value:* ):Boolean;
		function clear():void;
		function isEmpty():Boolean;
		function iteratorKeys():IIterator;
		function iteratorValues():IIterator;
		function key( value:* ):*;
		function keys():Array;
		function remove( key:* ):*;
		function removeAll( value:IMap ):Boolean;
		function size():int;
		function toArray():Array;
		function update( key:*, value:* ):Boolean;
		function value( key:* ):*;
		function values():Array;
		
	}
	
}
