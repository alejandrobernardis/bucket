
package kc.ui.screens {
	import kc.api.IScreen;
	import kc.api.IScreenContainer;
	import kc.api.IStack;
	import kc.events.ScreenEvent;
	import kc.ui.UIElement;
	import kc.utils.ExceptionUtil;

	import flash.display.DisplayObject;
	import flash.display.MovieClip;

	[Event( name="addScreen", type="kc.events.ScreenEvent" )]
	[Event( name="replaceScreen", type="kc.events.ScreenEvent" )]
	[Event( name="removeScreen", type="kc.events.ScreenEvent" )]

	public class ScreenContainer extends UIElement implements IScreenContainer {
		
		// @protected
		
		protected var _screens:IStack;
		protected var _ignoreEvents:Boolean;
		
		// @constructor
		
		public function ScreenContainer( capacity:int = undefined, data:XML = null, autorelease:Boolean = true) {
			super( data, autorelease );
			_screens = new ScreenViewsStack( capacity );
		}
		
		// @override
		
		override public function purge(...rest:*):void {
			clear();
			_screens = null;
			_ignoreEvents = undefined;
			super.purge();
		}
		
		override public function addChild(child:DisplayObject):DisplayObject {
			throw ExceptionUtil.MethodIsNotAvailable("addChild");
		}

		override public function addChildAt(child:DisplayObject, index:int):DisplayObject {
			throw ExceptionUtil.MethodIsNotAvailable("addChildAt");
		}

		override public function removeChild(child:DisplayObject):DisplayObject {
			throw ExceptionUtil.MethodIsNotAvailable("removeChild");
		}

		override public function removeChildAt(index:int):DisplayObject {
			throw ExceptionUtil.MethodIsNotAvailable("removeChildAt");
		}

		override public function swapChildren(child1:DisplayObject, child2:DisplayObject):void {
			throw ExceptionUtil.MethodIsNotAvailable("swapChildren");
		}
		
		override public function swapChildrenAt(index1:int, index2:int):void {
			throw ExceptionUtil.MethodIsNotAvailable("swapChildrenAt");
		}

		// @properties (r)
		
		public function get content():IScreen {
			return _screens.element();
		}
		
		public function get screens():IStack {
			return _screens;
		}
		
		public function get capacity():uint {
			return _screens.capacity;
		}
		
		public function get availableCapacity():uint {
			return _screens.availableCapacity;
		}
		
		public function get quantity():uint {
			return _screens.size();
		}
		
		// @methods
		
		public function add( value:IScreen, properties:Object = null ):void {
			
			if( availableCapacity == 0 )
				remove();
				
			if( _screens.push( value ) ) {
				
				var screen:IScreen = _screens.element() as IScreen;
				screen.init( properties );
				
				if( screen.isInitialized ) {
					super.addChild( screen as MovieClip );
					if( ! _ignoreEvents ) dispatchEvent(
						new ScreenEvent(
							ScreenEvent.ADD_SCREEN
						)
					);
				}
				
			}
				
		}
		
		public function replace( value:IScreen, properties:Object = null ):void {
			
			_ignoreEvents = true;
			
			remove(); 
			add( value, properties );
			
			_ignoreEvents = false;
			
			dispatchEvent(
				new ScreenEvent(
					ScreenEvent.REPLACE_SCREEN
				) 
			);
									
		}
		
		public function remove():void {
			
			if( _screens.isEmpty() ) return;
			
			var screen:IScreen = _screens.pop();
			screen.destroy();
			
			super.removeChild( screen as MovieClip );
			screen = null;     
			
			if( ! _ignoreEvents ) dispatchEvent(
				new ScreenEvent(
					ScreenEvent.REMOVE_SCREEN
				 )
			); 
		
		}
		
		public function clear():void {
			while( quantity ) {
				remove();
			}
		}
		
		// @helpers
		
		protected function ActionsHandler( e:* = null ):void {
			throw ExceptionUtil.MethodIsNotAvailable("ActionsHandler");
		}
		
		protected function addAsset( child:DisplayObject ):void {
			super.addChild(child);
		}
		
		protected function removeAsset( child:DisplayObject ):void {
			super.removeChild(child);
		}
		
	}
	
}
