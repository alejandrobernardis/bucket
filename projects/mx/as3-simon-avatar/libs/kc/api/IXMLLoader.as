
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IXMLLoader extends ILoader {
	
		// @methods
	
		function getValue( node:String ):String;
		function resolveAsMap( node:String, attribute:String ):IMap;
		function resolveAsArrayList( node:String, attribute:String = null ):Array;
		function resolveSimplePath( value:String ):XMLList;
	
	}
	
}
