
package kc.utils {
	import kc.core.KCStatic;

	import flash.system.ApplicationDomain;
	import flash.utils.describeType;
	import flash.utils.getQualifiedClassName;
	import flash.utils.getQualifiedSuperclassName;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class ClassUtil extends KCStatic {
		
		// @const
		
		private static const RESOLVE_NAME:String = "name";
		private static const RESOLVE_PACKAGE:String = "package";
		private static const RESOLVE_PATH:String = "path";
		private static const RESOLVE_PATH_COMPLEX:String = "pathComplex";
		private static const RESOLVE_CONSTANT:String = "constant";
		private static const RESOLVE_EXTENDS:String = "extendsClass";
		private static const RESOLVE_INTERFACE:String = "implementsInterface";
		private static const RESOLVE_METHOD:String = "method";
		private static const RESOLVE_PROPERTY:String = "accessor";
		private static const RESOLVE_PROPERTY_READONLY:String = "readonly";
		private static const RESOLVE_PROPERTY_WRITEONLY:String = "writeonly";
		private static const RESOLVE_PROPERTY_WRITABLE:String = "readwrite";		
		private static const RESOLVE_VARIABLE:String = "variable";
		private static const RESOLVE_GET_INSTANCE:String = "getInstance";
		private static const RESOLVE_GET_CLASS:String = "getClass";
		private static const RESOLVE_HAS_CLASS:String = "hasClass"; 
		
		// @constructor
		
		public function ClassUtil() {
			super();
		}
		
		// @classes
		
		public static function classConstruct( value:*, ...rest ):* {
			
			if( rest.length > 10 )
				ExceptionUtil.ViewError( "You have passed more arguments than this method excepts (Ten or less)." );
			
			if( typeof( value ) == "string" )
				value = getClass(value);
				
			switch( rest.length ){
				
				case  1: return new value( rest[0] );
				case  2: return new value( rest[0], rest[1] );
				case  3: return new value( rest[0], rest[1], rest[2] );
				case  4: return new value( rest[0], rest[1], rest[2], rest[3] );
				case  5: return new value( rest[0], rest[1], rest[2], rest[3], rest[4] );
				case  6: return new value( rest[0], rest[1], rest[2], rest[3], rest[4], rest[5] );
				case  7: return new value( rest[0], rest[1], rest[2], rest[3], rest[4], rest[5], rest[6] );
				case  8: return new value( rest[0], rest[1], rest[2], rest[3], rest[4], rest[5], rest[6], rest[7] );
				case  9: return new value( rest[0], rest[1], rest[2], rest[3], rest[4], rest[5], rest[6], rest[7], rest[8] );
				case 10: return new value( rest[0], rest[1], rest[2], rest[3], rest[4], rest[5], rest[6], rest[7], rest[8], rest[9] );
				
				default:
					return new value();
					
			}
			
		}
		
		public static function getClassInstance( value:String, domain:ApplicationDomain = null ):* {
			return ResolveClass( value, RESOLVE_GET_INSTANCE, domain );
		}
		
		public static function getClass( value:String, domain:ApplicationDomain = null ):* {
			return ResolveClass( value, RESOLVE_GET_CLASS, domain );
		}
		
		public static function hasClass( value:String, domain:ApplicationDomain = null ):Boolean {
			return ResolveClass( value, RESOLVE_HAS_CLASS, domain );
		}
		
		public static function ResolveClass( value:String, type:String, domain:ApplicationDomain = null ):* {
			
			if ( ! domain ) {
				domain = ApplicationDomain.currentDomain;
			}
			
			value = pathComplexName( value );
			
			if( type == RESOLVE_HAS_CLASS ){
				return domain.hasDefinition( value );
			}
			
			try{
				var instance:* = domain.getDefinition( value );
				return ( type != RESOLVE_GET_INSTANCE ) 
					? instance 
					: new instance();					
			}catch (e:Error){
				return ExceptionUtil.ViewError(
					( ( type != RESOLVE_GET_INSTANCE )
						? "Cannot find class with qualified class name: \""
						: "Cannot create class with qualified class name: \""
					) + value + "\""
				);
			}
			
		}
		
		// @names
		
		public static function longName( value:* ):String {
			return getQualifiedClassName( value );	
		}
		
		public static function shortName( value:* ):String {
			return ResolveNames( value, RESOLVE_NAME );
		}
		
		public static function packageName( value:* ):String {
			return ResolveNames( value, RESOLVE_PACKAGE );
		}
		
		public static function pathName( value:* ):String {
			return ResolveNames( value, RESOLVE_PATH );	
		}
		
		public static function pathComplexName( value:* ):String {
			return ResolveNames( value, RESOLVE_PATH_COMPLEX );	
		}
		
		public static function SLongName( value:* ):String {
			return getQualifiedSuperclassName( value );	
		}
		
		public static function SShortName( value:* ):String {
			return ResolveNames( value, RESOLVE_NAME, true );
		}
		
		public static function SPackageName( value:* ):String {
			return ResolveNames( value, RESOLVE_PACKAGE, true );	
		}
		
		public static function SPathName( value:* ):String {
			return ResolveNames( value, RESOLVE_PATH, true );	
		}
		
		public static function SPathComplexName( value:* ):String {
			return ResolveNames( value, RESOLVE_PATH_COMPLEX, true );	
		}
		
		private static function ResolveNames( value:*, type:String, inheritance:Boolean = false ):String {
			
			var source:String;
			
			if( typeof( value ) != "string" ){
				source = ( ! inheritance ) 
					? longName( value ) 
					: SLongName( value );
			}else{
				source = value;
			}
			
			switch( type ){
				
				case RESOLVE_NAME:
					return source.replace( RegExpUtil.PATTERN_CLASS_PACKAGE, "" );
				
				case RESOLVE_PACKAGE:
					source = source.replace( RegExpUtil.PATTERN_CLASS_NAME, "" );
					return ( source != value ) ? source : new String();
					
				case RESOLVE_PATH:
					return source.replace( RegExpUtil.PATTERN_CLASS_COLON, "." );
				
				case RESOLVE_PATH_COMPLEX:
					return ( source.search( RegExpUtil.PATTERN_CLASS_PACKAGE ) != -1 ) 
						? String(
							ResolveNames( value, RESOLVE_PACKAGE ) 
							+ "::" + ResolveNames( value, RESOLVE_NAME ) )
						: source;
			}
			
			return value;
			
		}
		
		// @thisIs
		
		public static function isDynamic( value:* ):Boolean {
			return ( describeType( value ).@isDynamic.toString() == "true" );
		}
		
		public static function isFinal( value:* ):Boolean {
			return ( describeType( value ).@isFinal.toString() == "true" );
		}
		
		public static function isStatic( value:* ):Boolean {
			return ( describeType( value ).@isStatic.toString() == "true" );
		}
		
		public static function isConstant( value:*, name:String ):Boolean {
			return ResolveThisIs( value, name, RESOLVE_CONSTANT );
		}
		
		public static function isInterface( value:* ):Boolean {
			return ResolveThisIs( value, null, RESOLVE_INTERFACE );
		}
		
		public static function isMethod( value:*, name:String ):Boolean {
			return ResolveThisIs( value, name, RESOLVE_METHOD );
		}
		
		public static function isProperty( value:*, name:String ):Boolean {
			return ResolveThisIs( value, name, RESOLVE_PROPERTY );
		}
		
		public static function isReadOnlyProperty( value:*, name:String ):Boolean {
			return ResolveThisIs( value, name, RESOLVE_PROPERTY_READONLY );
		}
		
		public static function isWriteOnlyProperty( value:*, name:String ):Boolean {
			return ResolveThisIs( value, name, RESOLVE_PROPERTY_WRITEONLY );
		}
		
		public static function isWritableProperty( value:*, name:String ):Boolean {
			return ResolveThisIs( value, name, RESOLVE_PROPERTY_WRITABLE );
		}
		
		private static function ResolveThisIs( value:*, name:String, type:String  ):Boolean {
			
			if ( type == RESOLVE_INTERFACE ) {
				var describe:XML = describeType( value );
				return ( describe.@base.toString() == "Class" 
					&& describe.@isStatic.toString() == "true" 
					&& describe.factory..extendsClass.length() == 0  ) 
						? true 
						: false;
			}
			
			var source:XMLList = ResolveCaptureNode( value, type );
			return ( source.@name.contains( name ) );
			
		}
		
		// @list
		
		public static function constantsList( value:* ):Array {
			return ResolveListAttributes( value, RESOLVE_CONSTANT );
		}

		public static function heritageList( value:* ):Array {
			return ResolveListAttributes( value, RESOLVE_EXTENDS );
		}
		
		public static function interfacesList( value:* ):Array {
			return ResolveListAttributes( value, RESOLVE_INTERFACE );
		}
		
		public static function methodsList( value:*, inherited:int = 0 ):Array {
			return ResolveListAttributes( value, RESOLVE_METHOD, inherited );
		}
		
		public static function propertiesList( value:*, inherited:int = 0 ):Array {
			return ResolveListAttributes( value, RESOLVE_PROPERTY, inherited );
		}
		
		public static function readOnlyPropertiesList( value:*, inherited:int = 0 ):Array {
			return ResolveListAttributes( value, RESOLVE_PROPERTY_READONLY, inherited );
		}
		
		public static function writeOnlyPropertiesList( value:*, inherited:int = 0 ):Array {
			return ResolveListAttributes( value, RESOLVE_PROPERTY_WRITEONLY, inherited );
		}
		
		public static function writablePropertiesList( value:*, inherited:int = 0 ):Array {
			return ResolveListAttributes( value, RESOLVE_PROPERTY_WRITABLE, inherited );
		}
		
		public static function variablesList( value:* ):Array {
			return ResolveListAttributes( value, RESOLVE_VARIABLE );
		}
		
		private static function ResolveListAttributes( value:*, type:String, inherited:int = 0 ):Array {
			
			var list:Array = new Array();
			var inheritance:String = pathComplexName( value );
			var source:XMLList = ResolveCaptureNode( value, type );
			
			for each( var element:XML in source ){
				
				switch( type ){
					
					case RESOLVE_CONSTANT:
					case RESOLVE_VARIABLE:
						list.push( element.@name.toString() );
						break;
						
					case RESOLVE_EXTENDS:
					case RESOLVE_INTERFACE:
						list.push( element.@type.toString() );
						break;
						
					case RESOLVE_METHOD:
					case RESOLVE_PROPERTY:
					case RESOLVE_PROPERTY_READONLY:						
					case RESOLVE_PROPERTY_WRITABLE:						
					case RESOLVE_PROPERTY_WRITEONLY:						
						if( inherited == 0 
							|| ( inherited == -1 && element.@declaredBy != inheritance )
							|| ( inherited ==  1 && element.@declaredBy == inheritance )
						){
							list.push( element.@name.toString() );
						}
						break;
					
				}
				
			}
			
			return list;
			
		}
		
		// @implemented
		
		public static function implementsMethod( value:*, inheritance:*, name:String ):Boolean {
			return ResolveImplemented( value, inheritance, name, RESOLVE_METHOD );
		}
		
		public static function implementsProperty( value:*, inheritance:*, name:String ):Boolean {
			return ResolveImplemented( value, inheritance, name, RESOLVE_PROPERTY );
		}
		
		private static function ResolveImplemented( value:*, inheritance:*, name:String, type:String ):Boolean {
			
			var source:XMLList = ResolveCaptureNode( value, type );
			
			if ( typeof( value ) != "string" ) {
				value = longName( value );
			} 
			
			if ( typeof( inheritance ) != "string" ) {
				inheritance = longName( inheritance );
			}
			
			return ( source.( @name == name ).@declaredBy.toString() == inheritance );
			
		}
		
		// @helpers
		
		private static function ResolveCaptureNode( value:*, type:String ):XMLList {
			
			var source:XML = describeType( value );
			
			switch( type ){
				
				case RESOLVE_CONSTANT:
					return source..constant;
				
				case RESOLVE_EXTENDS:
					return source..extendsClass;
				
				case RESOLVE_METHOD:
					return source..method;
				
				case RESOLVE_PROPERTY:
					return source..accessor;
				
				case RESOLVE_PROPERTY_READONLY:
				case RESOLVE_PROPERTY_WRITEONLY:
					return source..accessor.( @access == type );
					
				case RESOLVE_PROPERTY_WRITABLE:
					return source..accessor.( 
						@access == RESOLVE_PROPERTY_WRITABLE 
						|| @access == RESOLVE_PROPERTY_WRITEONLY 
					);
				
				case RESOLVE_INTERFACE:
					return source..implementsInterface;
				
				case RESOLVE_VARIABLE:
					return source..variable;
				
				default:
					return null;
				
			}	
			
		}
		
	}
	
}
