package activia.simon.shooter.core {
	import activia.simon.shooter.ui.ScreenFactory;

	import pq.core.Config;
	import pq.core.CoreSingleton;
	import pq.log.Debugger;
	import pq.utils.StringUtil;

	import flash.display.MovieClip;
	import flash.display.StageScaleMode;
	import flash.errors.IllegalOperationError;
	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.system.Security;
	import flash.system.System;
	
	
	public final class DataLayer extends EventDispatcher {
		
		/**
		 * Instancia unica de la clase.
		 */
		private static var $singleton:DataLayer;
		
		/**
		 * Contructor.
		 * @param	access Parametro para la inicializacion del singleton.
		 * @return	DataLayer
		 */
		public function DataLayer( access:SingletonClass = null ) {			
			if( access != null ){
				super( this );
			}else {				
				new CoreSingleton();
			}
		}
		
		/**
		 * Destruye al objeto y lo reinicializa.
		 * @return	void
		 */
		public static function destroy():void {	
			$singleton.purge();
			$singleton = null;			
		}
		
		/**
		 * Retorna una refencia de la instacia.
		 * @return	DataLayer
		 */
		public static function getInstance():DataLayer {			
			if( $singleton == null ){
				$singleton = new DataLayer( new SingletonClass() );
			}			
			return $singleton;			
		}		
		
		/**
		 * Inicializa la capa de datos.
		 * @param scope Entorno donde corre la aplicacion.
		 * @return void
		 */
		public static function initialize( scope:MovieClip ):void {
			
			getInstance();			
			Security.allowDomain("*");
			
			$scope = scope;
			$scope.stage.scaleMode = StageScaleMode.NO_SCALE;
			//$scope.stage.align = StageAlign.TOP_LEFT;
			
			try {				
				$flash_vars = $scope.stage.loaderInfo.parameters;
				$base_path = $flash_vars.cfgPath || new String();
				$fb_username = $flash_vars.fb_username || "@NN@";
			}catch ( e:Error ) { trace( "FLASH_VARS:", e.message ); }
			
			collection = new DataLayerMap();
			
			// if( ! isFacebook() ){			
				$config = new Config();
				$config.addEventListener( Event.COMPLETE, $singleton.CompleteConfig );
				$config.addEventListener( ErrorEvent.ERROR, $singleton.ErrorConfig );
				$config.load(new String($flash_vars.cfgData || "../data/config.xml"));
				
				
								
			/* } else {
				$config = new Config( FacebookXMLHelper.XML_CONFIG ); 
				$singleton.ValidateConfig();
			} */
			
		}
		
		/**
		 * Datos que maneja la aplicacion (HashMap).
		 */
		public static var collection:DataLayerMap;
		
		/**
		 * Base Path de la aplicacion.
		 */
		private static var $base_path:String;
		
		/**
		 * Base Path de la aplicacion.
		 * @return	String
		 */ 
		public static function get BASE_PATH():String {
			return $base_path;
		}
		
		/**
		 * Entorno de la aplicacion.
		 */
		private static var $scope:MovieClip;
		
		/**
		 * Entorno de la aplicacion.
		 * @return	MovieClip
		 */ 
		public static function get SCOPE():MovieClip {
			return $scope;
		}
		
		/**
		 * Variables externas.
		 */
		private static var $flash_vars:Object;
		
		/**
		 * Variables externas.
		 * @return Object
		 */
		public static function get FLASH_VARS():Object {
			return $flash_vars;
		}
		
		/**
		 * Configuracion de la aplicacion.
		 */
		private static var $config:Config;
		
		/**
		 * Configuracion de la aplicacion.
		 * @return Config
		 */
		public static function get CONFIG():Config {
			return $config;
		}
		
		/**
		 * Configuracion del juego, xml puro.
		 */
		private static var $config_game:XML;
		
		/**
		 * Configuracion del juego, xml puro.
		 * @return	XML
		 */
		public static function get CONFIG_GAME():XML {
			return $config_game;				
		}
		
		/**
		 * Factoria de pantallas.
		 */
		private static var $screen_factory:ScreenFactory;
		
		/**
		 * Factoria de pantallas.
		 */
		public static function get SCREEN():ScreenFactory {
			return $screen_factory;				
		}
		
		/**
		 * Nombre dle usuario de facebook.
		 */
		private static var $fb_username:String;
		
		/**
		 * Verifica el entorno del juego.
		 */
		public static function isFacebook():Boolean {
			return ( $fb_username != "@NN@" );
		}
		
		/**
		 * Aplica la validacion de dominios permitods.
		 */
		public static function applyAllowDomains( value:* = null ):void {
			if ( $config.data.config.hasOwnProperty( "allowDomain" ) ) {				
				for each( var node:XML in $config.data.config.allowDomain.children() ) {
					if ( value == null ) {
						Security.allowDomain( node.text().toString() );
					}else {
						value.allowDomain( node.text().toString() );
					}
					Debugger.WARN( $singleton, "AllowDomain: " + node.text().toString() );
				}
			}	
		}
		
		/**
		 * Purga el contenido del Objeto.
		 * @param	rest	Argumentos opcionales.
		 * @return	void
		 */
		public function purge( ...rest ):void {			
			
			$scope = null;
			$base_path = null;
			$flash_vars = null;
			$config_game = null;
			$fb_username = null;
			
			$config.purge();
			$config = null;	
			
			$screen_factory.purge();
			$screen_factory = null;
			
			Localization.purge();
			
			System.gc();
			
		}
		
		private function ValidateConfig():void {
			
			var node:XMLList = $config.data.config;
			
			// Debug ~
			
			if ( node.hasOwnProperty( "debug" ) ) {
				Debugger.active( true );
				Debugger.level( node.debug.level.text() );
				Debugger.appender( node.debug.appender.text() );
				Debugger.filter( node.debug.filter.text() );
				Debugger.separator( node.debug.separator.text() );
			}
			
			// Config ~
			
			Security.allowInsecureDomain("*");
			DataLayer.applyAllowDomains();
			
			if( ! StringUtil.isEmpty( node..paths.base.text() ) ){
				$base_path = node.paths.base.text();
			}
			
			if ( ! StringUtil.isEmpty( node..game.text() ) ) {
				
				
				var configGame:Config = new Config();
				
				// if ( ! isFacebook() ) {
					trace($config.dependency( node..game.text() ));
					configGame = new Config();
					configGame.addEventListener(Event.COMPLETE, CompleteConfigGame);
					configGame.addEventListener(ErrorEvent.ERROR, ErrorConfigGame);
					configGame.load($config.dependency(node..game.text()));
				/* } else {
					$config_game = FacebookXMLHelper.XML_GAME;
					CompleteConfigGame();
				} */
				
				
			} else {
				
				throw new IllegalOperationError( "No existe la ruta del archivo de configuración del juego." );
				
			}
			
		}
		
		private function ClearConfig():void {
			$config.removeEventListener( Event.COMPLETE, $singleton.CompleteConfig );
			$config.removeEventListener( ErrorEvent.ERROR, $singleton.ErrorConfig );
		}
		
		private function ErrorConfig( e:ErrorEvent ):void {
			this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR, false, false, "El XML de configuración no pudo ser cargado." ) );
			ClearConfig();
		}
		
		private function CompleteConfig( e:Event ):void {
			
			if ( ! $config.data.hasOwnProperty( "config" ) ) {
				throw new IllegalOperationError( "El XML de configuración esta mal formateado." );
			}else {
				ValidateConfig();
			}			
			
			ClearConfig();
			
		}
		
		private function ClearConfigGame( e:Event ):void {
			e.target.removeEventListener( Event.COMPLETE, CompleteConfigGame );
			e.target.removeEventListener( ErrorEvent.ERROR, ErrorConfigGame );
		}
		
		private function ErrorConfigGame( e:ErrorEvent ):void {
			this.dispatchEvent( new ErrorEvent( ErrorEvent.ERROR, false, false, "El XML de configuración del juego no pudo ser cargado." ) );
			ClearConfigGame(e);
		}
		
		private function CompleteConfigGame( e:Event = null ):void {
			
			if ( e != null ) {
				$config_game = e.target.data;
				e.target.purge();
				ClearConfigGame(e);
			}
			
			DataLayer.collection.add( "score_name", 	$fb_username );
			DataLayer.collection.add( "score_value", 	0 );
			DataLayer.collection.add( "score_minutes", 	0 );
			DataLayer.collection.add( "score_seconds", 	0 );
			DataLayer.collection.add( "score_position", 0 );
			
			SoundManager.initialize( XML( $config_game.sounds.toString() ) );
			$screen_factory = new ScreenFactory();
			
			Debugger.DEBUG( this, "FLASH_VARS:", $flash_vars );
			Debugger.DEBUG( this, "FACEBOOK_MODE:", isFacebook() );
			Debugger.DEBUG( this, "CONFIG:", $config );
			Debugger.DEBUG( this, "CONFIG_GAME:", $config_game );
			Debugger.DEBUG( this, "COLLECTION:", collection.itarator() );
			
			// if ( ! isFacebook() ) {
				this.dispatchEvent( new Event( Event.COMPLETE ) );
			/* } else {
				GameContent( $scope ).CompleteHandler();
			} */
			
		}
		
	}
	
}
import flash.utils.Dictionary;
/* ### HashMap ### */


class DataLayerMap extends Object {

	private var _records:Dictionary = null;
	
	public function DataLayerMap() {
		this.clear();
	}
	
	public function add( k:String, v:* ):void {
		if ( ! contain( k ) ) this._records[ k ] = v;
	}
	
	public function clear():void {
		this._records = new Dictionary();
	}
	
	public function contain( k:String ):Boolean {
		return ( this._records[ k ] != undefined && this._records[ k ] != null );
	}
	
	public function key( v:* ):* {
		for ( var a:String in this._records ) {
			if ( this._records[ a ] === v ) {
				return a;
			}
		}
		return null;
	}
	
	public function remove( k:String, v:* ):void {
		if( contain( k ) ) delete this._records[ k ];
	}
	
	public function update( k:String, v:* ):void {
		if( contain( k ) ) this._records[ k ] = v;
	}
	
	public function value( k:String ):Object {
		if ( contain( k ) ) return this._records[ k ];
		else return null;
	}	
	
	public function itarator():Array {
		var result:Array = new Array();
		for ( var element:* in _records ) {
			result.push( { key: element, value: _records[element] } );
		}
		return result;
	}
	
	public function purge( ...rest ):void {
		this._records = null;
	}
	
}

/* ### Singleton ### */

internal final class SingletonClass { }
