
package kc.ui.screens {
	import caurina.transitions.Tweener;

	import kc.api.IBasicButton;
	import kc.api.IScreen;
	import kc.ui.UIElementSteps;
	import kc.utils.ClassUtil;
	import kc.utils.ExceptionUtil;

	import flash.display.DisplayObject;
	import flash.display.Shape;
	import flash.display.SimpleButton;
	import flash.events.Event;
	import flash.events.IEventDispatcher;
	import flash.events.MouseEvent;
	import flash.geom.Rectangle;

	public class AbstractScreen extends UIElementSteps implements IScreen {
		
		// @protectes
		
		protected var _isInitialized:Boolean;
		protected var _ignoreUIElements:Boolean;
		protected var _isApplyActionFirstStep:Boolean;

		// @constructor
		
		public function AbstractScreen(data:XML = null, autorelease:Boolean = true) {
			super( data, autorelease );
		}
		
		// @override
		
		override protected function $config(e:Event):void {
			
			super.$config(e);
			
			if( _available ) {
				if( ! labels.length ) {
					addStepScript( _content.frame-1, ApplyActions );
				}else{
					for ( var a:uint = 0; a < labels.length; a++ )
						addStepScript( labels[a].name, ApplyActions );
					tweening = true;
				}	
			}
			
		}
		
		override public function purge(...rest:*):void {
			
			RemoveActions();
			
			for ( var a:uint = 0; a < labels.length; a++ )
				removeStepScript( labels[a].name );
			
			_isInitialized = undefined;
			_ignoreUIElements = undefined;			_isApplyActionFirstStep = undefined;
			super.purge();
			
		}

		override public function set enabled(value:Boolean):void {
			super.enabled = value;
			mouseChildren = value;
			opaque();			
		}
		
		override public function addChild(child:DisplayObject):DisplayObject {
			if( ! enabled ) return null;
			return super.addChild( child );
		}

		override public function addChildAt(child:DisplayObject, index:int):DisplayObject {
			if( ! enabled ) return null;
			return super.addChildAt( child, index );
		}

		override public function removeChild(child:DisplayObject):DisplayObject {
			if( ! enabled ) return null;
			return super.removeChild( child );
		}

		override public function removeChildAt(index:int):DisplayObject {
			if( ! enabled ) return null;
			return super.removeChildAt( index );
		}

		override public function swapChildren(child1:DisplayObject, child2:DisplayObject):void {
			if( ! enabled ) return;
			super.swapChildren( child1, child2 );
		}
		
		override public function swapChildrenAt(index1:int, index2:int):void {
			if( ! enabled ) return;
			super.swapChildrenAt( index1, index2 );
		}
		
		override protected function GoTo(value:uint, ignoreHistory:Boolean = false):uint {
			if( ! _isInitialized ) 
				ExceptionUtil.ViewError( 
					"The screen \""
					+ ClassUtil.shortName(this)
					+ "\" has not been initialized."
				); 			
			return super.GoTo( value, ignoreHistory );
		}

		// @prepertie (rw)
		
		public function get ignoreUIElements():Boolean {
			return _ignoreUIElements;
		}
		
		public function set ignoreUIElements(value:Boolean):void {
			_ignoreUIElements = value;
		}

		// @prepertie (r)
		
		public function get isInitialized():Boolean {
			return _isInitialized;
		}
		
		// @methods
		
		public function init(...rest:*):void {
			if( _isInitialized ) return;
			_isInitialized = true;
		}

		public function destroy():void {
			if( ! _isInitialized ) return;
			_isInitialized = false;
			purge();
		}
		
		public function validate_status():Boolean{
			return true;
		}
		
		// @helpers
				
		protected function ApplyActions():void {
			ResolveActions( false, _ignoreUIElements );
		}
		
		protected function RemoveActions():void {
			ResolveActions( true, _ignoreUIElements );
		}

		protected function ResolveActions( remove:Boolean = false, ignoreUIElements:Boolean = false ):void {
			
			//var element:IBasicButton;
			var element:IEventDispatcher;	
			
			var f:String = ( ! remove ) 
				? "addEventListener" 
				: "removeEventListener";
			
			if( ! remove && ! _isApplyActionFirstStep ) {
				_isApplyActionFirstStep = true;
				ignoreUIElements = false;
			}
			
			for ( var a:uint = 0; a < this.numChildren; a++ ) {
				//if( this.getChildAt(a) is IBasicButton ){
				if( this.getChildAt(a) is SimpleButton || this.getChildAt(a) is IBasicButton ){
					//element = this.getChildAt(a) as IBasicButton;
					element = this.getChildAt(a) as IEventDispatcher;
					//if( ! ignoreUIElements || ( ignoreUIElements && ! element.isUIElement() ) ) {
					if( ! ignoreUIElements || ( ignoreUIElements && ( element is IBasicButton && ! IBasicButton(element).isUIElement() ) ) ) {
						element[f].apply( 
							element,
							[MouseEvent.CLICK, ButtonsManager] 
						);
					}
				}
			}
			
		}
		
		protected function ButtonsManager( e:MouseEvent ):void {
			throw ExceptionUtil.MethodIsNotAvailable( "ButtonsManager" );
		}
		
		protected function opaque():void {
			
			if( ! enabled ){
				
				var rect:Rectangle = getUIRectangle() || new Rectangle();
							
				var shape:Shape = new Shape();
				shape.graphics.beginFill(0x000000);
				
				shape.graphics.drawRect( 
					0, 0, 
					( rect.width == 0 ) 
						? this.stage.stageWidth 
						: rect.width, 
					( rect.height == 0 ) 
						? this.stage.stageHeight
						: rect.height
				);
				
				shape.graphics.endFill();
				shape.alpha = 0;
				
				super.addChild( shape );
				
				Tweener.addTween(
					shape,
					{
						alpha: .75,
						time: 1,
						transition: "easeOutQuint"
					}
				);
				
			}else if((numChildren-1) > -1){
				
				super.removeChildAt( numChildren - 1 );
				
			}
			
		}
		
	}
	
}
