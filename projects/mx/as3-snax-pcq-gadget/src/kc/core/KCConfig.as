
package kc.core {
	import kc.api.IIterator;
	import kc.api.IKCConfig;
	import kc.api.IMap;
	import kc.loaders.XMLLoader;
	import kc.tda.SimpleIterator;
	import kc.tda.SimpleMap;
	import kc.utils.ExceptionUtil;
	import kc.utils.RegExpUtil;
	import kc.utils.StringUtil;

	import flash.events.Event;
	import flash.system.Security;

	/**
	 * KCConfig: Configuración externa via XML.
	 * 
 	 * <pre>
 	 * + LISTA DE PATRONES:
 	 * ===============================================================================================================
	 * {node.node.node} = reemplaza por el valor del nodo.
	 * {node.node.node:0} = reemplaza por el valor del nodo en la posici&oacute;n especificada.
	 * {node.node.attribute} = reemplaza por el valor del atributo.
	 * {node.node:0.&#64;attribute} = reemplaza por el valor del atributo en la posici&oacute;n especificada del nodo. 
	 * {node.node.&#64;attribute:value} = reemplaza por el valor del atributo especificado.  
	 * {node.node:0.&#64;.attribute:value} = reemplaza por el valor del atributo y del nodo especificado.
	 * ===============================================================================================================
	 * </pre>
	 * 
	 * TODO: Necesita una revision y una normalización de su estrucutra.
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCConfig extends XMLLoader implements IKCConfig {
		
		// @const
		
		public static const RESOLVE_FUNCTION:String = "dependency";
		public static const NOT_FOUND_LITERAL:String = "@kc-not-found@";
		
		private static const NOT_FOUND:int = -1;
		
		// @variables
		
		protected var _dependencies:IMap;
		protected var _dependenciesCache:Boolean;

		// @constructor
		
		public function KCConfig( data:XML = null, dependenciesCache:Boolean = false ) {
			super();
			_content = data;
			this.dependenciesCache = dependenciesCache;
		}   
		
		// @override
		
		override public function set url( value:String ):void {
			super.url = value.replace( RegExpUtil.PATTERN_CONFIG_URL, "" );
		}
		
		override public function purge(...rest):void {
			_dependencies.purge();
			_dependencies = null;
			_dependenciesCache = undefined;
			super.purge();
		}
		
		override public function toString():String {
			var pattern:String = new String("[KCConfig cache=\"{1}\" url=\"{2}\" method=\"{2}\"]");
			return StringUtil.substitute( pattern, _dependenciesCache, url, method );
		}
		
		override protected function CompleteHandler(e:Event):void {
			if ( String( _loader.data ).search( RegExpUtil.PATTERN_VALIDATE_XML_RESULT ) > NOT_FOUND ) {
				if( ! _dependenciesCache ){
					super.CompleteHandler(e);			
				}else{
					ResolveDependeciesCache(e);
				} 
			}
		}
		
		// @properties (rw)

		public function get dependenciesCache():Boolean {
			return _dependenciesCache;
		}
		
		public function set dependenciesCache( value:Boolean ):void {
			if( value && _content != null && ! _dependenciesCache )
				ResolveDependeciesCache();
			_dependenciesCache = value;						
		}
		
		// @properties (r)
		
		public function get dependencies():IMap {
			if( ! _dependenciesCache || _dependencies == null ) {
				ExceptionUtil.ViewError( 
					"The dependencies chache is not available.", 
					_catchExceptions 
				);
			} return _dependencies;
		}
		
		public function get dataCopy():XML {
			if( ! _content ) return null; 
			return new XML( this.content.toXMLString() );
		}
		
		// @allowDomain
		
		public function allowDomain( value:* ):Boolean {
			return KCConfig.ResolveDomainsAllowed( value, this.content );			
		}
		
		public static function ResolveDomainsAllowed( value:*, domains:XML ):Boolean {
			if ( domains && domains.hasOwnProperty( "allowDomain" ) ) {
				if( ! domains.allowDomain.children().length() )
					Security.allowDomain( domains.allowDomain.@default.toString() );
				for each( var node:XML in domains.allowDomain.children() ) {
					if ( ! value ) {
						Security.allowDomain( node.text().toString() );
					}else {
						value.allowDomain( node.text().toString() );
					}
				} return true;
			} return false;
		}
		
		// @values
		
		public function info( value:String ):String {
			
			var list:XMLList = resolveSimplePath("info");
			var result:String = list.child(value);
			
			return ( result ) ? result.toString() : null;
				
		}
		
		public function debug( value:String ):String {
			
			var list:XMLList = resolveSimplePath("debug");
			var result:String = list.child(value);
			
			return ( result ) ? result.toString() : null;
				
		}

		public function path( value:String, dependecy:Boolean = true ):String {
			return pathsList( dependecy ).value( value );
		}
		
		public function datalayer( value:String, dependecy:Boolean = true ):String {
			return datalayersList( dependecy ).value( value );
		}
		
		public function asset( value:String, dependecy:Boolean = true ):String {
			return assetsList( dependecy ).value( value );
		}
		
		public function getValueAndResolveDependency( node:String ):String {
			return dependency( getValue( node ) );
		}
		
		// @lists
		
		public function allowDomainsList():IMap {
			return ResolveList( "allowDomain" );
		}
		
		public function pathsList( dependecy:Boolean = true ):IMap {
			return ResolveList( "paths", dependecy );		
		}
		
		public function datalayersList( dependecy:Boolean = true ):IMap {
			return ResolveList( "datalayer", dependecy );					}
		
		public function assetsList( dependecy:Boolean = true ):IMap {
			return ResolveList( "assets", dependecy );			
		}
		
		protected function ResolveList( node:String, dependecy:Boolean = true ):IMap {
			if( dependecy ) _resolveFunction = RESOLVE_FUNCTION;
			var result:IMap = resolveAsMap( node, "id" );
			_resolveFunction = null;
			return result;
		}

		// @cache
		
		private function ResolveDependeciesCache(...rest):void {
			
			var data:XML = ( ! _loaded )
				? new XML( String( _loader.data ) )
				: content;
			
			var vdependency:String;
			var ddependency:XML = KCConfig.ResolveNamespace( data ); 
			var ldependency:IIterator = new SimpleIterator( ddependency.toXMLString().match( RegExpUtil.PATTERN_DEPENDENCY ) ); 
			
			if( ldependency.hasNext() ) {
				_dependencies = new SimpleMap();
				while( ldependency.hasNext() ) {
					vdependency = String( ldependency.next() ).match( RegExpUtil.PATTERN_DEPENDENCY_PATH )[0];
					if( ! _dependencies.containsKey( vdependency ) ) {
						_dependencies.add(
							vdependency,
							KCConfig.ResolveDependencies( 
								ldependency.value(), 
								ddependency 
							)
						);
					}
				}
			} else {
				_dependenciesCache = false;
			} 
			
			if( rest.length ) {
				super.CompleteHandler( rest[0] );
			}else{
				_loaded = true;
			}
						
		}
		
		// @dependency
		
		public function dependency( value:String, removeNS:Boolean = false ):String {
			
			if( ! _dependenciesCache ){
				return KCConfig.ResolveDependency( 
					value, 
					this.content, 
					removeNS 
				);				
			}
			
			var vdependency:String;
			var ldependency:IIterator = new SimpleIterator( value.match( RegExpUtil.PATTERN_DEPENDENCY ) );
			
			if( ldependency.hasNext() ) {
				while( ldependency.hasNext() ) {
					vdependency = String( ldependency.next() ).match( RegExpUtil.PATTERN_DEPENDENCY_PATH )[0];	
					if( _dependencies.containsKey( vdependency ) ){
						value = value.replace( 
							ldependency.value(), 
							_dependencies.value( vdependency ) 
						);
					}else{
						value = value.replace( 
							ldependency.value(), 
							NOT_FOUND_LITERAL 
						);
					}
				}
			} return value;
			
		}
		
		public static function ResolveDependency( value:String, data:XML, removeNS:Boolean = false ):String {
			if( removeNS ){
				data = KCConfig.ResolveNamespace( data );
			} return KCConfig.ResolveDependencies( value, data );
		}
		
		private static function ResolveDependencies( value:String, data:XML ):String {
			
			if( value.search( RegExpUtil.PATTERN_DEPENDENCY ) == NOT_FOUND ) {
				return value;
			}
			
			var ddependency:XML = data;
			var ldependency:XMLList;
			var vdependency:String = value.match( RegExpUtil.PATTERN_DEPENDENCY )[0];
			var node:Element;
			var pnode:Element;
			var vnode:String = vdependency.match( RegExpUtil.PATTERN_DEPENDENCY_PATH )[0];
			var lnode:IIterator = new SimpleIterator( vnode.split(".") );
			
			if( lnode.hasNext() ){
				while( lnode.hasNext() ) {					
					node = new Element( lnode.next() );
					pnode = new Element( lnode.peek() );
					if( ! node.isAttribute() && ddependency.hasOwnProperty(node.name) ) {
						ldependency = ddependency.child(node.name);
						if( pnode.isAttribute() ) {
							ldependency = ddependency.children();
							value = value.replace( 
								vdependency, 
								( pnode.value.length )
									? ldependency.( @[pnode.name] == pnode.value )
									: ldependency.attribute( pnode.name )[0]
							); return KCConfig.ResolveDependencies( value, data );
						}else if( node.position > NOT_FOUND ) {				
							if( node.position < ldependency.length() ) {
								ddependency = XML( ldependency[ node.position ] );								
							} else {
								ddependency = XML( ldependency[ ldependency.length() - 1 ] );								
							}							 
						} else {							
							ddependency = XML( ldependency[0] );							
						}						
					} else {					
						break;																		
					}				
				} value = value.replace( 
					vdependency, 
					( ddependency.children().length() > 1 )
						? NOT_FOUND_LITERAL
						: ddependency.toString()
				);			
			} return KCConfig.ResolveDependencies( value, data );
			
		}
		
		// @helpers
		
		public static function ResolveNamespace( value:* ):XML {
			
			if( value is XML || value is XMLList ){
				value = value.toXMLString();
			}
			
			return new XML(
				value.replace(
					RegExpUtil.PATTERN_NS_DEFINED,
					""
				).replace( 
					RegExpUtil.PATTERN_NS_ONODE,
					"<"
				).replace(
					RegExpUtil.PATTERN_NS_CNODE,
					"</"
				)
			);
			
		}
		
	}
	
}

import kc.utils.ExceptionUtil;
import kc.utils.RegExpUtil;
import kc.utils.StringUtil;

internal final class Element {
	
	// @const
	
	private static const NOT_FOUND:int = -1;
	
	// @variables
	
	private var _name:String;
	private var _value:String;
	private var _attribute:Boolean;
	private var _position:int = -1;
	
	// @constructor
	
	public function Element( value:String ) {
		if( value != null ) {
			var list:Array = value.split(":");
			_name = list[0];
			if( value.search( RegExpUtil.PATTERN_DEPENDENCY_ATTRIBUTE ) > NOT_FOUND ) {
				_attribute = true;
				_name = _name.replace( /@/g, "" );
				_value = list[1] || new String();
			}else {
				_position = ( list[1] != undefined ) 
					? int( list[1] ) 
					: NOT_FOUND;
			}
		}
	}
	
	// @properties (r)
	
	public function get name():String {
		return _name;
	}
	
	public function get value():String {
		if( ! isAttribute() ) {
			return ExceptionUtil.ViewError("The element is not an attribute.");
		} return _value;
	}
	
	public function get position():int {
		if( isAttribute() ) {
			return ExceptionUtil.ViewError("The element is an attribute.");
		} return _position;
	}
	
	// @methods
	
	public function isAttribute():Boolean {
		return _attribute;
	}
	
	public function toString():String {
		var value:String = "[Element name=\"{1}\" value=\"{2}\" position=\"{3}\"]";
		return StringUtil.substitute( value, _name, _value, _position );
	}
	
} 
