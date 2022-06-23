
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IStack extends ICollection {
		
		// @methods
		
		function element():*;
		function peek():*;
		function push( value:* ):Boolean;
		function pop():*;
		
	}
	
}
