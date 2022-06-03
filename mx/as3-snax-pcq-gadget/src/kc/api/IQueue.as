
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IQueue extends ICollection {
		
		// @methods
		
		function element():*;
		function peek():*;
		function enqueue( value:* ):Boolean;
		function dequeue():*;
	
	}
	
}
