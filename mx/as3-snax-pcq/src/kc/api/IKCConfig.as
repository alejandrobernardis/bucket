
package kc.api {

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public interface IKCConfig extends IXMLLoader {
	
		// @properties (rw)
	
		function get dependenciesCache():Boolean;
		function set dependenciesCache( value:Boolean ):void;
		
		// @properties (r)
		
		function get dependencies():IMap;
		function get dataCopy():XML;
		
		// @allowDomain
		
		function allowDomain( value:* ):Boolean;
		
		// @values
		
		function info( value:String ):String;
		function path( value:String, dependecy:Boolean = true ):String;
		function datalayer( value:String, dependecy:Boolean = true ):String;		function asset( value:String, dependecy:Boolean = true ):String;
		function getValueAndResolveDependency( node:String ):String;
		
		// @lists
		
		function allowDomainsList():IMap;
		function pathsList( dependecy:Boolean = true ):IMap;
		function datalayersList( dependecy:Boolean = true ):IMap;		function assetsList( dependecy:Boolean = true ):IMap;
	
	}
	
}
