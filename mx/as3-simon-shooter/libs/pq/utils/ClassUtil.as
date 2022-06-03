
package pq.utils {
	
	import flash.errors.IllegalOperationError;
	import flash.system.ApplicationDomain;
	
	import pq.core.CoreStatic;

	public final class ClassUtil extends CoreStatic {
		
		public static function create( value:String, domain:ApplicationDomain = null ):* {
			
			try{
				var Clazz:Class = getClass( value, domain );
				return new Clazz();	
			}catch( e:Error ){
				throw new IllegalOperationError( "Cannot create class with qualified class name: " + value );
			}			 
			
		}
		
		public static function getClass( value:String, domain:ApplicationDomain = null ):Class {
			
			var appDomain:ApplicationDomain = ( domain == null ) ? ApplicationDomain.currentDomain : domain;
			
			if( appDomain.hasDefinition( value ) ) {
				return appDomain.getDefinition( value ) as Class;
			}else{
				throw new IllegalOperationError( "Cannot find class with qualified class name: " + value );
			}
			
			return null;
			
		}
		
	}
	
}