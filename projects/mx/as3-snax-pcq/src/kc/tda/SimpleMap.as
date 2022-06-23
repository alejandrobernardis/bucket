
package kc.tda {
	import kc.api.IIterator;
	import kc.api.IMap;
	import kc.utils.ArrayUtil;
	import kc.utils.NumberUtil;
	import kc.utils.PurgerUtil;

	import flash.utils.Dictionary;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleMap extends Object implements IMap {
		
		// @const
		
		public static const DEFAULT_CAPACITY:int = 1 << 5;
		public static const DEFAULT_MIN_CAPACITY:int = 1 << 4;
		public static const DEFAULT_MAX_CAPACITY:int = 1 << 30;
		
		public static const NOT_FOUND:int = -1;
	
		// @protected
	
		protected var _records:Dictionary;
		protected var _capacity:int;
		protected var _size:int;
		protected var _weakReferences:Boolean;
		
		// @constructor
		
		public function SimpleMap( capacity:int = undefined ) {
			
			super();
			
			_capacity = NumberUtil.limits(
				capacity, 
				DEFAULT_MIN_CAPACITY, 
				DEFAULT_MAX_CAPACITY, 
				DEFAULT_CAPACITY
			);
			
			clear();
					
		}
		
		// @properties (r)
		
		public function get capacity():int {
			return _capacity;
		}
		
		public function get availableCapacity():int {
			return ( _capacity - _size );
		}

		// @methods
		
		public function add( key:*, value:* ):Boolean {
			if( containsKey(key) || availableCapacity == 0 ) return false;
			_records[key] = value;
			_size++;
			return true;
		}
		
		public function addAll( value:IMap ):Boolean {
			
			var i:IIterator = value.iterator();
			var q:int = _size;
			
			while( i.hasNext() ){
				remove( i.next() );
			} 
			
			return ( q < _size );
			
		}
		
		public function clear():void {
			PurgerUtil.cleanCollection(_records);
			_records = new Dictionary(_weakReferences);
		}
		
		public function containsKey( key:* ):Boolean {
			return _records[key] != null;
		}
		
		public function containsValue( value:* ):Boolean {
			for( var element:* in _records ){
				if( _records[element] === value ){
					return true;
				}
			} return false;
		}
		
		public function isEmpty():Boolean {
			return ( _size < 1 );
		}
		
		public function iterator():IIterator {
			return new SimpleIterator( toArray() );
		}
		
		public function iteratorKeys():IIterator {
			return new SimpleIterator( keys() );
		}
		
		public function iteratorValues():IIterator {
			return new SimpleIterator( values() );
		}

		public function key( value:* ):* {
			for( var element:* in _records ){
				if( _records[element] === value ){
					return element;
				}
			} return null;
		}
		
		public function keys():Array {
			return ArrayUtil.toArray( _records, -1 );
		}
		
		public function remove( key:* ):* {
			if( ! containsKey(key) ) return null;
			var element:* = _records[key];
			delete _records[key];
			_size--;
			return element;
		}
		
		public function removeAll( value:IMap ):Boolean {
			
			var i:IIterator = value.iteratorKeys();
			var q:int = _size;
			
			while( i.hasNext() ){
				remove( i.next() );
			} 
			
			return ( q > _size );
			
		}

		public function size():int {
			return _size;
		}
		
		public function toArray():Array {
			return ArrayUtil.toArray( _records, 0 );
		}

		public function update( key:*, value:* ):Boolean {
			if( ! containsKey(key) ) return false;
			_records[key] = value;
			return true;
		}

		public function value( key:* ):* {
			if( ! containsKey(key) ) return null;
			return _records[key];
		}
		
		public function values():Array {
			return ArrayUtil.toArray( _records, 1 );
		}
		
		// @purge
		
		public function purge(...rest):void {
			PurgerUtil.cleanCollection(_records);
			_records = null;
			_capacity = undefined;
			_size = undefined;
			_weakReferences = undefined;
		} 
		
	}
	
}
