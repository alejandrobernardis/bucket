
package kc.ui.screens {
	import kc.api.IIterator;
	import kc.api.IScreen;
	import kc.api.IStack;
	import kc.tda.SimpleIterator;
	import kc.tda.SimpleStack;

	public class ScreenViewsStack extends SimpleStack implements IStack {
		
		// @constructor
		
		public function ScreenViewsStack( capacity:int = undefined ) {
			super( capacity );
		}
		
		// @override
		
		override public function purge(...rest:*):void {
			
			var i:IIterator = new SimpleIterator( _records );
			
			while( i.hasNext() ) 
				IScreen( i.next() ).purge();
				
			i.purge(); 
			super.purge();
			
		}

		override public function element():* {
			return super.element() as IScreen;
		}

		override public function peek():* {
			return super.peek() as IScreen;
		}
		
		override public function push( value:* ):Boolean {
			if( value is IScreen )
				return super.push( value );
			return false;
		}

		override public function pop():* {
			return super.pop() as IScreen;
		}
		
	}
	
}
