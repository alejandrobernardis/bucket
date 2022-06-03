
package kc.tda {
	import kc.api.IIterator;
	import kc.utils.PurgerUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class SimpleIterator extends Object implements IIterator {

		// @const
		
		public static const NOT_FOUND:int = -1;

		// @protected
		
		protected var _records:Array;
		protected var _index:int;
		protected var _indexLast:int;
		
		// @constructor

		public function SimpleIterator( value:Array ) {
			_records = value || new Array();
			reset();
		}
		
		// @properties (r)
		
		public function get index():int {
			return ( _indexLast > NOT_FOUND )
				? _indexLast 
				: _index;
		}

		// @methods
		
		public function hasNext():Boolean {
			return ( _index < size() );
		}

		public function next():* {
			if( hasNext() ) {
				_indexLast = _index++;
				return _records[_indexLast];
			} return null;
		}
		
		public function peek():* {
			if( ! hasNext() ) return null;
			return _records[index+1];
		}

		public function remove():void {
			if( size() > 0 && _indexLast > NOT_FOUND ) {
				_records.splice( _indexLast, 1 );
				if( _indexLast < _index ) {
					_index--;
				} _indexLast = NOT_FOUND;	
			}
		}
		
		public function reset():void {
			_index = 0;
			_indexLast = NOT_FOUND;
		}
		
		public function size():int {
			return _records.length;
		}

		public function toArray():Array {
			return _records;
		}

		public function value():* {
			return _records[index];
		}

		// @purge
		
		public function purge(...rest):void {
			PurgerUtil.cleanCollection( _records );
			_records = null;
		}
		
	}
	
}
