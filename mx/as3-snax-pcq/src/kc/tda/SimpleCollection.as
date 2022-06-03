
package kc.tda {
	import kc.api.ICollection;
	import kc.api.IIterator;
	import kc.utils.NumberUtil;
	import kc.utils.PurgerUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleCollection extends Object implements ICollection {
		
		// @const
		
		public static const DEFAULT_CAPACITY:int = 1 << 5;
		public static const DEFAULT_MIN_CAPACITY:int = 1 << 4;
		public static const DEFAULT_MAX_CAPACITY:int = 1 << 30;
		
		public static const NOT_FOUND:int = -1;
		
		// @protected
		
		protected var _records:Array;
		protected var _capacity:int;
		
		// @constructor

		public function SimpleCollection( capacity:int = undefined ) {
			
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
			return ( _capacity - size() );
		}
		
		// @methods
		
		public function add(value:*):Boolean {
			if( availableCapacity == 0 ) return false;
			var q:int = size();
			return ( q < _records.push(value) );
		}

		public function addAll(value:ICollection):Boolean {
			
			var i:IIterator = value.iterator();
			var q:int = size();
			
			while( i.hasNext() ){
				add( i.next() );
			}
			
			return ( q < size() );
			
		}
		
		public function clear():void {
			PurgerUtil.cleanCollection( _records );
			_records = new Array();
		}

		public function contains(value:*):int {
			return _records.indexOf(value);
		}

		public function containsAll(value:ICollection):Boolean {
			
			var i:IIterator = value.iterator();
			
			while( i.hasNext() ){
				if( contains( i.next() ) == NOT_FOUND ) {
					return false;
				}
			}
			
			return true;			

		}
		
		public function copy():ICollection {
			var value:ICollection = new SimpleCollection( capacity );
			value.addAll(this);
			return value; 
		}
		
		public function isEmpty():Boolean {
			return ( size() == 0 );
		}
		
		public function iterator():IIterator {
			return new SimpleIterator( _records );
		}
		
		public function remove(value:*):Boolean {
			
			var i:int = contains(value);
			var q:int = size();
			
			if( i > NOT_FOUND ) {
				_records.splice( i, 1 );
			}
			
			return ( q > size() );
			
		}
		
		public function removeAll(value:ICollection):Boolean {
			
			var i:IIterator = value.iterator();
			var q:int = size();
			
			while( i.hasNext() ){
				remove( i.next() );
			}
			
			return ( q > size() );
			
		}
		
		public function retainAll(value:ICollection):Boolean {
			
			var i:IIterator;
			var q:int = size();
			var records:Array = new Array();
			
			if( q > value.size() ){
				i = value.iterator();
				value = this;
			}else{
				i = iterator();
			}
			
			while( i.hasNext() ){
				if( value.contains( i.next() ) != NOT_FOUND ) {
					records.push( i.value() );
				}
			}
			
			if( q != records.length ) {
				_records = records;
				return true;
			} 
			
			return false;
			
		}
		
		public function size():uint {
			return _records.length;
		}

		public function toArray():Array {
			return _records;
		}

		// @purge
		
		public function purge(...rest):void {
			PurgerUtil.cleanCollection( _records );
			_records = null;
			_capacity = undefined;		
		} 
		
	}
	
}
