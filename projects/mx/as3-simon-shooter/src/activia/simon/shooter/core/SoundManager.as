package activia.simon.shooter.core {
	import pq.core.CoreSingleton;
	import pq.log.Debugger;

	import flash.events.EventDispatcher;
	import flash.media.Sound;
	import flash.media.SoundChannel;
	import flash.media.SoundTransform;
	import flash.system.ApplicationDomain;
	
	
	public class SoundManager extends EventDispatcher {
		
		private static var $singleton:SoundManager;
		
		public function SoundManager( access:SingletonClass = null ) {			
			if( access != null ){
				super( this );
				this._collections = new SoundDictionary();
				this._playList = new SoundDictionary();
			}else {				
				new CoreSingleton();
			}
		}
		
		public static function destroy():void {	
			$singleton.purge();
			$singleton = null;			
		}
		
		public static function getInstance():SoundManager {			
			if( $singleton == null ){
				$singleton = new SoundManager( new SingletonClass() );
			}			
			return $singleton;			
		}	
		
		public static function initialize( data:XML ):void {
			
			getInstance();
			
			for each ( var node:XML in data.sound ) {
				if ( ApplicationDomain.currentDomain.hasDefinition( node.text() ) ) {
					var clazz:Class = ApplicationDomain.currentDomain.getDefinition( node.text() ) as Class;
					$singleton._collections.add( node.@id,  new clazz() );
				}
			}
			
			Debugger.DEBUG( $singleton, $singleton._collections );
			
		}
		
		// ~
		
		private var _collections:SoundDictionary;
		private var _playList:SoundDictionary;
		
		public function hit( k:String, volume:Number = .5 ):void {			
			var sndt:SoundTransform = new SoundTransform( volume );
			Sound( _collections.value( k ) ).play( 0, 1, sndt );
		}
		
		public function play( k:String ):void {			
			if ( isPlaying( k ) ) return;		
			var snd:SoundChannel = Sound( _collections.value( k ) ).play( 0 );			
			_playList.add( k, snd );
		}
		
		public function isPlaying( k:String ):Boolean {
			return ( _collections.contain( k ) 
						&& _playList.contain( k ) 
							&& _playList.value( k ) is SoundChannel );
		}
		
		public function stop( k:String ):void {			
			if ( isPlaying( k ) ) return;
			SoundChannel( _playList.remove( k ) ).stop();
		}
		
		public function pause( k:String ):void {
			if ( ! isPlaying( k ) ) return;
			var snd:SoundChannel = _playList.remove( k );
			_playList.add( k, snd.position );
			snd.stop();
		}
		
		public function resume( k:String ):void {
			if ( isPlaying( k ) || isNaN( _playList.value( k ) ) ) return;
			var pos:Number = Number( _playList.remove(k) );
			var snd:SoundChannel = Sound( _collections.value( k ) ).play( pos );
			_playList.add( k, snd );
		}
		
		public function mute( k:String ):void {
			if ( isPlaying( k ) || isMute( k ) ) return;
		}
		
		public function purge( ...rest ):void {
			_collections.purge();
			_playList.purge();
			_collections = null;
			_playList = null;
		}
		
		private function isMute( k:String ):Boolean {
			return true;
		}
		
	}

}
import flash.utils.Dictionary;

class SoundDictionary extends Object {
	
	private var _size:uint;
	private var _collection:Dictionary;
	
	public function SoundDictionary() {
		_collection = new Dictionary( true );
		_size = 0;
	}
	
	public function add( k:String, v:* ):void {			
		if ( ! contain( k ) ) {
			_collection[k] = v;			
			_size ++;
		}
	}
	
	public function remove( k:String ):* {			
		if ( ! contain( k ) ) return null;			
		var obj:* = _collection[k];
		_collection[k] = null;
		_size --;
		return obj;			
	}
	
	public function value( k:String ):* {
		if ( ! contain( k ) ) return null;
		return _collection[k];
	}
	
	public function contain( k:String ):Boolean {			
		return ( _collection[k] != null );
	}
	
	public function get size():uint { 
		return _size; 
	}
	
	public function purge():void {
		_size = undefined;
		_collection = null;
	}
	
}

/* ### Singleton ### */

internal final class SingletonClass { }