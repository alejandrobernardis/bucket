
package kc.ui.components {
	import kc.api.IBasicButton;
	import kc.api.IIterator;
	import kc.data.Record;
	import kc.tda.SimpleIterator;
	import kc.ui.UIElement;
	import kc.utils.PurgerUtil;

	import flash.display.*;
	import flash.events.Event;
	import flash.events.MouseEvent;

	[Event(name="click", type="flash.events.MouseEvent")]
	[Event(name="mouseUp", type="flash.events.MouseEvent")]
	[Event(name="mouseDown", type="flash.events.MouseEvent")]
	[Event(name="mouseOut", type="flash.events.MouseEvent")]
	[Event(name="mouseOver", type="flash.events.MouseEvent")]

	public class BasicButton extends UIElement implements IBasicButton {

		// @const

		public static const DISABLED:String 	= "disabled";
		public static const PRESS:String 		= "press";
		public static const OVER:String 		= "over";
		public static const OUT:String 			= "out";
		public static const UP:String 			= "up";

		public static const HIT_AREA:String 	= "mcHitArea";

		// @protected

		protected var _label:String;		protected var _tweening:Boolean;
		protected var _tweeningFrames:int;
		protected var _tweeningStates:Array;
		protected var _events:Array;

		// @constructor

		public function BasicButton( data:XML = null, autorelease:Boolean = true ) {

			super( data, autorelease );

			_events = [
				[ MouseEvent.MOUSE_UP, MouseManager, false, 0, false ],
				[ MouseEvent.MOUSE_DOWN, MouseManager, false, 0, false ],
				[ MouseEvent.MOUSE_OUT, MouseManager, false, 0, false ],
				[ MouseEvent.MOUSE_OVER, MouseManager, false, 0, false ]
			];

			_tweeningFrames = 4;
			_tweeningStates = [ DISABLED, PRESS, OVER, OUT, UP ];

		}

		// @override

		override protected function $config(e:Event):void {

			super.$config( e );

			ResolveProperty( true );
			ResolveStyle( MouseEvent.MOUSE_OUT );
			ResolveEvents();

			if( totalFrames > _tweeningFrames ){
				_tweening = ResolveAvailableTweening();
			}

			if( getChildByName( HIT_AREA ) != null ){
				var hit:Sprite = getChildByName( HIT_AREA ) as Sprite;
				hitArea = hit;
				hit.alpha = 0;
			}

		}

		override public function set enabled(value:Boolean):void {

			if( value != enabled ){

				super.enabled = value;

				var status:String;

				if( ! value ){
					status = DISABLED;
					ResolveProperty( false );
				}else{
					status = MouseEvent.MOUSE_OUT;
					ResolveProperty( true );
				}

				ResolveStyle( status );

			}

		}

		override public function purge(...rest):void {

			ResolveEvents( null, true );

			PurgerUtil.cleanCollection( _events );			PurgerUtil.cleanCollection( _tweeningStates );

			_label = null;
			_events = null;
			_tweening = undefined;
			_tweeningFrames = undefined;
			_tweeningStates = null;

			super.purge();

		}

		// @properties (rw)

		public function set label( value:String ):void {
			_label = value;
		}

		public function get label():String {
			return _label;
		}

		public function get tweening():Boolean {
			return _tweening;
		}

		public function set tweening( value:Boolean ):void {
			_tweening = value;
		}

		// @helpers

		protected function MouseManager( event:MouseEvent ):void {
			if( enabled )
				ResolveStyle( event.type );
		}

		protected function ResolveEvents( list:Array = null, remove:Boolean = false ):void {

			var f:String = ( ! remove )
				? "addEventListener"
				: "removeEventListener";

			var i:IIterator = new SimpleIterator( list || _events );

			while( i.hasNext() ) {
				this[f].apply(
					this,
					( ! remove )
						? i.next()
						: i.next().slice( 0, 2 )
				);
			}

		}

		protected function ResolveAvailableTweening():Boolean {

			var f:IIterator = new SimpleIterator( currentLabels );

			while( f.hasNext() ){
				if( _tweeningStates.indexOf( f.next().name ) == -1 ){
					return false;
				}
			}

			return true;

		}

		protected function ResolveProperty( value:Boolean ):void {
			buttonMode = value;
			useHandCursor = value;
			mouseEnabled = value;
			mouseChildren = false;
		}

		protected function ResolveStyle( status:String = null ):void {

			var record:Record;

			switch( status ){

				case DISABLED:
					record = new Record( DISABLED, 4 );
					break;

				case MouseEvent.MOUSE_DOWN:
					record = new Record( PRESS, 3 );
					break;

				case MouseEvent.MOUSE_UP:
				case MouseEvent.MOUSE_OVER:
					record = new Record(
						( status != MouseEvent.MOUSE_UP )
							? OVER
							: UP
						, 2
					);
					break;

				default:
				case MouseEvent.MOUSE_OUT:
					record = new Record( OUT, 1 );
					break;

			}

			if( ! _tweening ) {
				gotoAndStop( record.value );
			}else{
				gotoAndPlay( record.key );
			}

		}

	}

}
