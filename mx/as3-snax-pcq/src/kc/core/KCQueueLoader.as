
package kc.core {
	import kc.api.IIterator;
	import kc.api.IKCQueueLoader;
	import kc.api.IKCQueueLoaderItem;
	import kc.api.ILoader;
	import kc.events.KCQueueLoaderEvent;
	import kc.logging.SimpleLog;
	import kc.tda.SimpleIterator;
	import kc.utils.ClassUtil;
	import kc.utils.NumberUtil;
	import kc.utils.PurgerUtil;
	import kc.utils.RegExpUtil;
	import kc.utils.StringUtil;

	import flash.events.ErrorEvent;
	import flash.events.Event;
	import flash.events.EventDispatcher;
	import flash.events.HTTPStatusEvent;
	import flash.events.IOErrorEvent;
	import flash.events.ProgressEvent;
	import flash.events.SecurityErrorEvent;
	import flash.system.ApplicationDomain;

	[Event( name="complete", type="flash.events.Event" )]
	[Event( name="open", type="flash.events.Event" )]
	[Event( name="httpStatus", type="flash.events.HTTPStatusEvent" )]
	[Event( name="ioError", type="flash.events.IOErrorEvent" )]
	[Event( name="securityError", type="flash.events.SecurityErrorEvent" )]
	[Event( name="queueStart", type="kc.events.KCQueueLoaderEvent" )]
	[Event( name="queueStop", type="kc.events.KCQueueLoaderEvent" )]
	[Event( name="queueCatchError", type="kc.events.KCQueueLoaderEvent" )]
	[Event( name="queueProgress", type="kc.events.KCQueueLoaderEvent" )]
	[Event( name="queueItemComplete", type="kc.events.KCQueueLoaderEvent" )]
	[Event( name="queueComplete", type="kc.events.KCQueueLoaderEvent" )]
	
	/**
	 * TODO: Necesita una revision y una normalización de su estrucutra.
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCQueueLoader extends EventDispatcher implements IKCQueueLoader {
		
		// @const
		
		public static const DEFAULT_CAPACITY:int = 1 << 5;
		public static const DEFAULT_MIN_CAPACITY:int = 1 << 4;
		public static const DEFAULT_MAX_CAPACITY:int = 1 << 30;
		
		private static const NOT_FOUND:int = -1;
		
		// @variables
		
		protected var _records:Array;
		protected var _capacity:int;
		
		protected var _item:IKCQueueLoaderItem;
		protected var _items:IIterator;
		protected var _itemsLoaded:int;
		protected var _itemsFailed:int;
		protected var _itemsFailedList:Array;
		
		protected var _verbose:Boolean;
		protected var _catchExceptions:Boolean;
		protected var _events:Array;
		protected var _isRunning:Boolean;

		// @constructor

		public function KCQueueLoader( capacity:int = undefined, catchExceptions:Boolean = false, verbose:Boolean = false ) {
			
			super( this );
			
			_capacity = NumberUtil.limits(
				capacity, 
				DEFAULT_MIN_CAPACITY, 
				DEFAULT_MAX_CAPACITY, 
				DEFAULT_CAPACITY
			);
			
			_events = [				
				[ Event.COMPLETE, CompleteHandler, false, 0, false ],
				[ Event.OPEN, dispatchEvent, false, 0, false ],
				[ ProgressEvent.PROGRESS, ProgressHandler, false, 0, false ],
				[ HTTPStatusEvent.HTTP_STATUS, dispatchEvent, false, 0, false ],
				[ IOErrorEvent.IO_ERROR, ErrorHandler, false, 0, false ],
				[ SecurityErrorEvent.SECURITY_ERROR, ErrorHandler, false, 0, false ]
			];
			
			_catchExceptions = catchExceptions;
			_verbose = verbose;
			
			clear();
			
		}
		
		// @override
		
		override public function toString():String {
			var pattern:String = "[KCQueueLoader running=\"{1}\" total=\"{2}\" loaded=\"{3}\" failed=\"{4}\"]";
			return StringUtil.substitute( pattern, _isRunning, size(), _itemsLoaded, _itemsFailed );
		}
		
		// @properties (wr)
		
		public function get verbose():Boolean {
			return _verbose;
		}
		
		public function set verbose( value:Boolean ):void {
			_verbose = value;
		}
		
		public function get catchExceptions():Boolean {
			return _catchExceptions;
		}

		public function set catchExceptions( value:Boolean ):void {
			_catchExceptions = value;
		}

		// @properties (r)
		
		public function get index():int {
			return ( _items != null )
				? _items.index + 1
				: 0;
		}
		
		public function get capacity():int {
			return _capacity;
		}

		public function get availableCapacity():int {
			return ( _capacity - size() );
		}
		
		public function get itemsLoaded():int {
			return _itemsLoaded || 0;
		}

		public function get itemsFailed():int {
			return _itemsFailed || 0;
		}
		
		public function get itemsFailedList():Array {
			return _itemsFailedList || new Array();
		}
		
		// @queue
		
		public function add( url:String, properties:Object = null ):Boolean {
			
			var value:String = url.replace( RegExpUtil.PATTERN_CONFIG_URL, "" );
			
			if( availableCapacity == 0 || contains( value ) != NOT_FOUND ) {
				return false;
			}
			
			var q:int = size();
			var item:IKCQueueLoaderItem = new QueueLoaderItem( url, properties );
			
			if( item.isValid() ) {
				_records.push( item );
			}
			
			return ( q < size() );
			
		}
		
		public function remove( url:String ):Boolean {
			
			var i:int = contains(url);
			var q:int = size();			
			
			if( i != NOT_FOUND ) {
				var item:IKCQueueLoaderItem = _records[i];
				item.purge();
				_records.splice( i, 1 );
			} 
			
			return ( q > size() );
			
		}
		
		public function contains( url:String ):int {
			for( var a:int=0; a<_records.length; a++ ){
				if( _records[a].url == url ){
					return a;
				}
			} return NOT_FOUND;
		}
		
		public function clear():void {
			PurgerUtil.cleanCollection( _records );
			_records = new Array();
		}
		
		public function isEmpty():Boolean {
			return ( size() == 0 );
		}

		public function size():int {
			return _records.length;
		}
		
		public function toArray():Array {
			return _records;
		}
		
		public function dump():void {
			SimpleLog.dump( _records );
		}
		
		// @content 
		
		public function getContent( url:String, remove:Boolean = false ):* {
			return ResolveGetContent( contains( url ), remove );			
		}
		
		public function getContentAt( index:int, remove:Boolean = false ):* {
			return ResolveGetContent( index, remove );
		}
		
		public function getContentAs( url:String, type:*, remove:Boolean = false ):* {
			return ResolveGetContent( contains( url ), remove ) as type;			 
		}
		
		public function getContentAsAt( index:int, type:*, remove:Boolean = false ):* {
			return ResolveGetContent( index, remove ) as type;			
		}
		
		protected function ResolveGetContent( index:int, remove:Boolean = false ):* {
			
			var content:* = null;
						
			if( _records[index] && _itemsFailedList.indexOf(index) == NOT_FOUND ) {
				content = IKCQueueLoaderItem( _records[index] ).loader.content;
				if( remove ){
					_records.splice( index, 1 );
					_itemsLoaded--;
				}
			} 
			
			return content;
			
		}
		
		// TODO: experimentales...
		
		public function containsKey( key:String ):int {
			for( var a:int=0; a<_records.length; a++ ){
				if( _records[a].key == key ){
					return a;
				}
			} return NOT_FOUND;
		}
		
		public function getContentKey( key:String, remove:Boolean = false ):* {
			return ResolveGetContent( containsKey( key ), remove );			
		}
		
		public function getContentKeyAs( key:String, type:*, remove:Boolean = false ):* {
			return ResolveGetContent( containsKey( key ), remove ) as type;			 
		}
		
		public function getContentByDomainAs( url:String, type:*, domain:ApplicationDomain = null, remove:Boolean = false ):* {
			return getContentByDomainAsAt( contains( url ), type, domain, remove );
		}
		
		public function getContentByDomainAsAt( index:int, type:*, domain:ApplicationDomain = null, remove:Boolean = false ):* {
			return ResolveGetContent(
				index, remove
			) as ClassUtil.getClass(
				ClassUtil.longName( type ),	domain
			);
		}
		
		// @loader
		
		public function start( catchExceptions:Boolean = false, verbose:Boolean = false ):void {
			
			if( _isRunning ) return;
			
			ResolveStop(true);
			 
			if( verbose ) _verbose = verbose;
			if( catchExceptions )  _catchExceptions = catchExceptions;
			
			_items = new SimpleIterator( _records.slice() );
			_itemsFailedList = new Array();			
			_isRunning = true;
			
			ResolveVerbose( "START" );
			ResolveHasNext();
			
			dispatchEvent( 
				new KCQueueLoaderEvent(
					KCQueueLoaderEvent.QUEUE_START, 
					ResolveEventProperties()
				) 
			);
			
		}
		
		public function stop():void {
			
			if( ! _isRunning ) return;
			
			ResolveStop();
			
			dispatchEvent( 
				new KCQueueLoaderEvent(
					KCQueueLoaderEvent.QUEUE_STOP, 
					ResolveEventProperties() 
				) 
			);
			
			ResolveVerbose( "STOP" );
			
		}
		
		public function isRunning():Boolean {
			return _isRunning;
		}
		
		public function isLoaded():Boolean {
			return ( _itemsLoaded == size() );
		}
		
		// @handlers
		
		protected function CompleteHandler(e:Event):void {
			
			_itemsLoaded++;
			
			dispatchEvent( 
				new KCQueueLoaderEvent(
					KCQueueLoaderEvent.QUEUE_ITEM_COMPLETE, 
					ResolveEventProperties() 
				) 
			);
			
			ResolveVerbose( "COMPLETE" );
			ResolveHasNext();
			
		}
		
		protected function ProgressHandler(e:ProgressEvent):void {
			
			dispatchEvent( 
				new KCQueueLoaderEvent(
					KCQueueLoaderEvent.QUEUE_PROGRESS,
					ResolveEventProperties() 
				) 
			);
			
			ResolveVerbose( "PROGRESS" );
			
		}

		protected function ErrorHandler(e:ErrorEvent):void {
			
			_itemsFailed++;
			_itemsFailedList.push( _items.index );
			
			if( ! _catchExceptions ) {
				
				ResolveVerbose( "ERROR" );
				ResolveStop();
				dispatchEvent(e);
				
			} else {
				
				_itemsLoaded++;
				
				var properties:Object = ResolveEventProperties();
				properties.error = e.text;
				
				ResolveVerbose( "CATCH ERROR", properties );
				
				dispatchEvent(
					new KCQueueLoaderEvent(
						KCQueueLoaderEvent.QUEUE_CATCH_ERROR, 
						properties 
					) 
				);
				
				ResolveHasNext();
				
			}
			
		}
		
		// @purge
		
		public function purge(...rest):void {
			
			if( ! _items )
				_items = new SimpleIterator( _records );
			_items.reset();	
				
			while( _items.hasNext() ){
				_item = _items.next();
				ResolveEvents( null, true );
				_item.purge();
			}
			
			_item = null;
			_items.purge();
			_items = null;
			
			PurgerUtil.cleanCollection( _records );
			PurgerUtil.cleanCollection( _events );
			PurgerUtil.cleanCollection( _itemsFailedList );
			
			_records = null;
			_capacity = undefined;
			_itemsLoaded = undefined;
			_itemsFailed = undefined;
			_itemsFailedList = null;
			_verbose = undefined;
			_catchExceptions = undefined;
			_events = null;
			_isRunning = undefined;
			
		}
		
		// @helpers
		
		protected function ResolveStop( reset:Boolean = false ):void {
			
			ResolveEvents( null, true );
			
			if( _items )
				_items.purge();
			
			_items = null;
			
			if( _isRunning && _item )
				_item.loader.close();
			
			_item = null;
			
			if( reset ) {
			
				if( _itemsFailedList ) 
					PurgerUtil.cleanCollection( _itemsFailedList );
				
				_itemsLoaded = 0;
				_itemsFailed = 0;	
				_itemsFailedList = null;				
				
			}
			
			_isRunning = false;
			
		}
		
		protected function ResolveHasNext():void {
			
			if( ! _items ) return;			
			
			if( _items.hasNext() ) {
				
				ResolveEvents( null, true );
				
				_item = _items.next() as IKCQueueLoaderItem;
				ResolveEvents();
				
				_item.loader.load();
				ResolveVerbose( "NEXT LOAD" );
				
				return;
								
			} 
			
			_isRunning = false;
			
			ResolveStop();
			ResolveVerbose( "C'est fini ^_^" );
			
			dispatchEvent(
				new KCQueueLoaderEvent(
					KCQueueLoaderEvent.QUEUE_COMPLETE, 
					ResolveEventProperties() 
				) 
			);
			
		}
		
		protected function ResolveEventProperties():Object {			
			
			var properties:Object = new Object();			
			
			properties.itemIndex = index;
			properties.itemsLoaded = _itemsLoaded;
			properties.itemsFailed = _itemsFailed;
			properties.itemsTotal = size();
			
			if( _item ){
				properties.itemBytesLoaded = _item.loader.bytesLoaded;
				properties.itemBytesTotal = _item.loader.bytesTotal;
				properties.itemProgress = _item.loader.progress;	
			}
			
			properties.progress = Math.ceil( ( _itemsLoaded / size() ) * 100 );
			
			return properties;
						
		}

		protected function ResolveEvents( list:Array = null, remove:Boolean = false ):void {
			
			if( ! _item ) return;
			
			var f:String = ( ! remove ) 
				? "addEventListener" 
				: "removeEventListener";
			
			var loader:ILoader = _item.loader;	
			var i:IIterator = new SimpleIterator( list || _events );
						
			while( i.hasNext() ) {
				loader[f].apply( 
					loader, 
					( ! remove ) 
						? i.next()
						: i.next().slice( 0, 2 )
				);
			}
			
		}
		
		protected function ResolveVerbose(...rest:*):void {
			
			if( _verbose ){
				
				var properties:Object;
				
				if( rest.length == 1 ){
					properties = ResolveEventProperties();
					rest.push( properties );
				}else{
				 	properties = rest[1];
				}
				
				if( _item ){
					properties.uid = _item.uid;
					properties.url = _item.url;
					properties.loader = _item.loader;
				} 
				
				rest.unshift("Kirika Code - QueueLoader v1.0");
				
				if( rest[1] == "PROGRESS" ){
					SimpleLog.print.apply( null, [ rest[0], rest[1], properties.itemProgress ] );
				}else{
					SimpleLog.dump.apply( null, rest );
				}
				
			}
			
		}
	}
}

import kc.api.IKCQueueLoaderItem;
import kc.api.ILoader;
import kc.core.KCClassFactory;
import kc.loaders.LoaderType;
import kc.utils.UID;

import flash.display.MovieClip;

internal final class QueueLoaderItem extends Object implements IKCQueueLoaderItem {
	
	private var _uid:String;
	private var _key:String;
	private var _target:MovieClip;
	private var _loader:ILoader;
	
	// @constructor
	
	public function QueueLoaderItem( url:String, properties:Object = null ) {	
	
		if( ! properties ) 
			properties = new Object();

		var type:* = ( ! properties.type )
			? LoaderType.getURLAsTypeClass( url )
			: LoaderType.getTypeClass( properties.type );
			
		if( ! type ) return;
		 
		_loader = new KCClassFactory(type).newInstance(properties);
		_loader.url = url;
		
		_key = properties.key || null;
		_target = properties.target || null;
	
	}

	// @properties (r)
	
	public function get uid():String {
		if( ! _uid ){
			_uid = UID.create();
		} return _uid;
	}
	
	public function get key():String {
		return _key;
	}
	
	public function get url():String {
		if( ! _loader ) return null;
		return _loader.url;
	}

	public function get loader():ILoader {
		return _loader;
	}
	
	// @methods
	
	public function isValid():Boolean {
		return ( _loader != null );
	}
	
	// @purge
	
	public function purge(...rest:*):void {
		
		if( _loader != null ) {
			_loader.purge();
			_loader = null;
		}
		
		_uid = null;
		_target = null;
		
	}
	
}
