
package kc.core {
	import kc.api.IKCComponent;
	import kc.events.KCComponentEvent;
	import kc.utils.ClassUtil;
	import kc.utils.ExceptionUtil;
	import kc.utils.PurgerUtil;
	import kc.utils.UID;

	import flash.display.DisplayObject;
	import flash.display.DisplayObjectContainer;
	import flash.display.MovieClip;
	import flash.events.Event;

	[Event( name="disabled", type="kc.events.KCComponentEvent" )]
	[Event( name="enabled", type="kc.events.KCComponentEvent" )]
	[Event( name="dataChange", type="kc.events.KCComponentEvent" )]

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class KCComponent extends MovieClip implements IKCComponent {

		// @const

		private static const NOT_FOUND:int = -1;

		// @variables

		protected var _data:XML;
		protected var _autorelease:Boolean;

		private var _uid:String;
		private var _owner:DisplayObjectContainer;

		// @constructor

		public function KCComponent( data:XML = null, autorelease:Boolean = true ) {
			super();
			// MovieClip
			this.stop();
			this.focusRect = false;
			//this.tabEnabled = false;
			//this.tabChildren = false;
			// KCCompoenent
			this.data = data;
			this.autorelease = autorelease;
			this.addEventListener(
				Event.ADDED_TO_STAGE,
				$config
			);
		}

		// @override

		override public function get enabled():Boolean {
			return super.enabled;
		}

		override public function set enabled( value:Boolean ):void {
			super.enabled = value;
			this.dispatchEvent(
				new KCComponentEvent(
					( ! value )
						? KCComponentEvent.DISABLED
						: KCComponentEvent.ENABLED
				)
			);
		}

		// @methods

		public function get data():XML {
			return this._data;
		}

		public function set data( value:XML ):void {
			if( this._data === value ) return;
			this._data = value;
			this.dispatchEvent(
				new KCComponentEvent (
					KCComponentEvent.DATA_CHANGE
				)
			);
		}

		public function get autorelease():Boolean {
			return this._autorelease;
		}

		public function set autorelease( value:Boolean ):void {

			if( this._autorelease == value ) {
				return;
			}

			this._autorelease = value;

			if( ! this._autorelease ){
				this.removeEventListener(
					Event.REMOVED_FROM_STAGE,
					purge
				);
			}else{
				this.addEventListener(
					Event.REMOVED_FROM_STAGE,
					purge
				);
			}

		}

		public function get owner():DisplayObjectContainer {
			return this._owner || this.parent;
		}

		public function set owner( value:DisplayObjectContainer ):void {
			this._owner = value;
		}

		public function get uid():String {
			if( this._uid == null ){
				this._uid = UID.create();
			} return this._uid;
		}

		public function owns( value:DisplayObject ):Boolean {
			if ( this.contains( value ) ) return true;
			try{
				while( value && value != this ){
					if( value is IKCComponent ){
						value = IKCComponent( value ).owner;
					}else{
						value = value.parent;
					}
				}
			}catch( e:SecurityError ){
		        return false;
			} return ( value == this );
    	}

		public function applyToAllChildren( action:String, ...rest ):void {
			var child:IKCComponent;
			var mList:Array = ClassUtil.methodsList( this );
			var pList:Array = ClassUtil.writablePropertiesList( this );
			for ( var a:int = 0; a < this.numChildren; a++ ) {
				if ( this.getChildAt(a) is IKCComponent ) {
					child = this.getChildAt(a) as IKCComponent;
					try{
						if( mList.indexOf( action ) != NOT_FOUND ) {
							child[action].apply( child, rest );
						}else if ( pList.indexOf( action ) != NOT_FOUND ) {
							child[action] = rest[0];
						}
					}catch(e:Error){
						ExceptionUtil.ViewError(
							[ child, action, e ],
							true
						);
						break;
					}
				}
			} PurgerUtil.cleanCollection( mList );
			PurgerUtil.cleanCollection( pList );
		}

		public function position( x:Number, y:Number = NaN ):void {
			this.x = x;
			this.y = ( ! isNaN( y ) ) ? y : x;
		}

		public function scale( x:Number, y:Number = NaN ):void {
			this.scaleX = x;
			this.scaleY = ( ! isNaN( y ) ) ? y : x;
		}

		public function resize( w:Number, h:Number = NaN ):void {
			this.width = w;
			this.height = ( ! isNaN( h ) ) ? h : w;
		}

		// @purge

		public function purge(...rest):void {

			this._data = null;
			this._uid = null;
			this._owner = null;
			this._autorelease = undefined;

			if ( this.hasEventListener( Event.REMOVED_FROM_STAGE ) ) {
				this.removeEventListener(
					Event.REMOVED_FROM_STAGE,
					purge
				);
			}

			if ( this.hasEventListener( Event.ADDED_TO_STAGE ) ) {
				this.removeEventListener(
					Event.ADDED_TO_STAGE,
					$config
				);
			}

		}

		// @handlers

		protected function $config(e:Event):void {

			this.removeEventListener(
				Event.ADDED_TO_STAGE,
				$config
			);

		}

	}

}