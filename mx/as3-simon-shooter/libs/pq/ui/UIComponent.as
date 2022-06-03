
package pq.ui {
	
	/**
	 * @imports
	 */
	
	import flash.display.DisplayObject;
	import flash.display.MovieClip;
	import flash.events.Event;
	import pq.log.Debugger;
	
	import pq.api.IUIComponent;
	import pq.events.UIComponentEvent;
	import pq.utils.UID;
	
	/**
	 * @events
	 */
	
	[Event(name="enabled", type="pq.events.UIComponentEvent")]
	[Event(name="changeData", type="pq.events.UIComponentEvent")]
	
	/**
	 * Modelo base de un Componente. 
	 * @author	Alejandro M. Bernardis (alejandro.bernardis@gmail.com)
	 */
	public class UIComponent extends MovieClip implements IUIComponent {
		
		/**
		 * Identificador unico del componente.
		 */
		private var _uid:String;
		
		/**
		 * Capa de datos del componente.
		 */
		private var _data:XML;
		
		/**
		 * Referencia al objeto creador.
		 */
		private var _owner:DisplayObject;
		
		/**
		 * Constructor
		 */
		public function UIComponent() {
			this.stop();
			this._uid = UID.create();
			this.addEventListener( Event.REMOVED_FROM_STAGE, purge );
		}

		/**
		 * Identificador unico del componente.
		 */
		public function get uid():String {
			return this._uid;
		}
		
		/**
		 * Capa de datos del componente.
		 */
		public function get data():XML {
			return this._data;
		}
		
		public function set data( value:XML ):void {
			this._data = value;
			this.dispatchEvent( new UIComponentEvent( UIComponentEvent.CHANGE_DATA ) );
		}
		
		/**
		 * Disponibilidad del componente.
		 */
		public override function get enabled():Boolean {
			return super.enabled;
		}
		
		public override function set enabled(value:Boolean):void {
			super.enabled = value;
			this.dispatchEvent( new UIComponentEvent( UIComponentEvent.ENABLED ) );
		}
		
		/**
		 * Objeto contenedor del componente.
		 */
		public function get owner():DisplayObject {
			return ( this._owner != null ) ? this._owner : this.parent;
		}
		
		public function set owner( value:DisplayObject ):void {
			this._owner = value;
		}
		
		/**
		 * Alienacion del Objeto.
		 */
		public function align( x:Number, y:Number = NaN ):void {
			this.x = x;
			this.y = y || x;
		}
		
		/**
		 * Escala del Objeto.
		 */
		public function scale( x:Number, y:Number = NaN ):void {
			this.scaleX = x;
			this.scaleY = y || x;
		}
		
		/**
		 * Purgador del componente.
		 */
		public function purge(...rest):void {
			this._uid 	= null;
			this._data 	= null;
			this._owner = null;
			this.removeEventListener( Event.REMOVED_FROM_STAGE, purge );
			Debugger.WARN( this, "Purge" );
		}
		
		/**
		 * Valida si el elemento es un hijo del componete.
		 */
		public function isChild( value:String ):Boolean {
			if( this.getChildByName( value ) != null ){
				return true;
			}else{
				return false;
			}
		}
		
	}
	
}