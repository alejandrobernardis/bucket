
package kc.core {
	import kc.api.IApplication;
	import kc.api.IIterator;
	import kc.api.IKCConfig;
	import kc.api.IKCQueueLoader;
	import kc.api.IMap;
	import kc.api.IPurger;
	import kc.events.KCQueueLoaderEvent;
	import kc.tda.SimpleMap;
	import kc.utils.ExceptionUtil;

	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.IOErrorEvent;
	import flash.events.SecurityErrorEvent;

	[Event(name="complete", type="flash.events.Event")]
	[Event(name="error", type="flash.events.ErrorEvent")]
	[Event(name="queueProgress", type="kc.events.KCQueueLoaderEvent")]
	
	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCDataLayer extends EventDispatcher implements IPurger {
		
		// @variables
		
		private static var $collection:IMap;
		private static var $config:IKCConfig;
		private static var $scope:IApplication;
		private static var $singleton:KCDataLayer;

		// @constructor

		public function KCDataLayer( access:SingletonClass = null ) {			
			if( access ) {
				super(this);
			}else{
				new KCSingleton();
			}
		}
		
		// @singleton
		
		public static function getInstance():KCDataLayer {
			if( ! $singleton )
				$singleton = new KCDataLayer( new SingletonClass() );
			return $singleton;
		}

		public static function destroy():void {
			if( ! $singleton ) 
				return;
			$singleton.purge();
			$singleton = null;
		}
		
		public static function init( scope:IApplication ):void {
			
			getInstance();
			
			// scope
			
			$scope = scope;
			
			// collection
			
			$collection = new SimpleMap( 100 );
			
			// config
			
			$config = new KCConfig( null, true );
			$config.addEventListener( Event.COMPLETE, $singleton.CompleteConfigHandler );
			$config.addEventListener( IOErrorEvent.IO_ERROR, $singleton.ErrorConfigHandler ); 
			$config.addEventListener( SecurityErrorEvent.SECURITY_ERROR, $singleton.ErrorConfigHandler );
			$config.load( new String( 
					( getFlashVar("cfgBasePath") || "" ) + 
					( getFlashVar("cfgConfigFile") || "../data/config.xml" ) 
				) 
			);
			 
		}

		// @statics
		
		public static function get scope():IApplication {
			return $scope;
		}

		public static function get basePath():String {
			return getFlashVar("cfgBasePath") || getPath("base") || "";
		}
		
		public static function get flashVars():Object {
			if( ! $scope ) 
				return null;
			if( ! $scope.stage.loaderInfo.parameters )
				return new Object();
			return $scope.stage.loaderInfo.parameters;
		}
		
		public static function get collection():IMap {
			return $collection;
		}

		public static function get config():IKCConfig {
			return $config;
		}
		
		public static function getFlashVar( value:String ):String {
			if( ! $scope ) 
				return null;
			return flashVars[value];
		}

		public static function getPath( value:String ):String {
			if( ! $config )
				return null;
			return $config.path( value );
		}

		// @methods
		
		public function purge(...rest):void {
			$scope = null;
			$collection.purge();
			$collection = null;
			$config.purge();
			$config = null;
		}
		
		// @handlers
		
		protected function ClearConfigHandlers():void {
			$config.removeEventListener( Event.COMPLETE, $singleton.CompleteConfigHandler );
			$config.removeEventListener( IOErrorEvent.IO_ERROR, $singleton.ErrorConfigHandler ); 
			$config.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, $singleton.ErrorConfigHandler );
		}
		
		protected function CompleteConfigHandler(e:Event):void {
			
			var notComplete:Boolean;
	
			// AllowDomain
			
			$config.allowDomain(null);
			
			// DataLayers
			
			var list:IMap = $config.datalayersList();
			
			if( list.size() ) {
				
				var mapping:IIterator = list.iterator();
				
				if( mapping.size() ) {
					
					var qloader:IKCQueueLoader = new KCQueueLoader();
					qloader.addEventListener( KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteQLoaderHandler );
					qloader.addEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, dispatchEvent );
					qloader.addEventListener( IOErrorEvent.IO_ERROR, ErrorQLoaderHandler ); 
					qloader.addEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorQLoaderHandler );
					//qloader.verbose = true;
					
					while( mapping.hasNext() ) {
						mapping.next();
						qloader.add( mapping.value()[1], { key: mapping.value()[0] } );
					}
					
					qloader.start();					
					notComplete = true;
					
				}
				
				mapping.purge();
				
			}
			
			list.purge();
			
			// Events
			
			ClearConfigHandlers(); 
			
			if( ! notComplete )
				dispatchEvent( new Event( Event.COMPLETE ) );
			
		}
		
		protected function ErrorConfigHandler(e:ErrorEvent):void{
			
			ExceptionUtil.ViewError( e, true );
			ClearConfigHandlers();
			
			dispatchEvent( 
				new ErrorEvent( ErrorEvent.ERROR, false, false, e.text ) 
			);
			
		}
		
		protected function ClearQLoaderHandlers( value:IKCQueueLoader ):void {
			value.removeEventListener( KCQueueLoaderEvent.QUEUE_COMPLETE, CompleteQLoaderHandler );
			value.removeEventListener( KCQueueLoaderEvent.QUEUE_PROGRESS, dispatchEvent );
			value.removeEventListener( IOErrorEvent.IO_ERROR, ErrorQLoaderHandler ); 
			value.removeEventListener( SecurityErrorEvent.SECURITY_ERROR, ErrorQLoaderHandler );
			value.purge();
			value = null;
		}
		
		protected function CompleteQLoaderHandler(e:Event):void {
			
			var qloader:IKCQueueLoader = e.target as KCQueueLoader;
			var mapping:IIterator = $config.datalayersList().iterator();
			
			while( mapping.hasNext() ) {
				mapping.next();
				$collection.add( 
					mapping.value()[0], 
					qloader.getContent( mapping.value()[1], true ) 
				);
			}
			
			mapping.purge();
			
			ClearQLoaderHandlers( qloader );
			dispatchEvent( new Event( Event.COMPLETE ) );
			
		}
		
		protected function ErrorQLoaderHandler(e:ErrorEvent):void {
			
			ExceptionUtil.ViewError( e, true );
			ClearQLoaderHandlers( e.target as IKCQueueLoader );
			
			dispatchEvent( 
				new ErrorEvent( ErrorEvent.ERROR, false, false, e.text ) 
			);
			
		} 
		
	}
	
}

internal final class SingletonClass {}
