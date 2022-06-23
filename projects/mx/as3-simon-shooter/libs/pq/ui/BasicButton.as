
package pq.ui {
	
	import flash.display.MovieClip;
	import flash.errors.IllegalOperationError;
	import flash.events.Event;
	import flash.events.MouseEvent;
	
	[Event(name="click", type="flash.events.MouseEvent")]
	[Event(name="mouseUp", type="flash.events.MouseEvent")]
	[Event(name="mouseDown", type="flash.events.MouseEvent")]
	[Event(name="mouseOut", type="flash.events.MouseEvent")]
	[Event(name="mouseOver", type="flash.events.MouseEvent")]
	
	public class BasicButton extends UIComponent {
		
		/**
		 * Constantes para efectos de transición.
		 */
		protected static const DISABLED:String 		= "disabled";
		protected static const PRESS:String 		= "press";
		protected static const OVER:String 			= "over";
		protected static const OUT:String 			= "out";
		protected static const UP:String 			= "up";
		
		/**
		 * Define si el boton soporta transicion por frame.
		 */
		private var _frameTransition:Boolean = false;
		
		/**
		 * Constructor.
		 */
		public function BasicButton() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, Config );
		}
		
		/**
		 * Label.
		 */
		public function set label( value:String ):void {
			throw new IllegalOperationError( "Metodo no disponible" );
		}
		
		public function get label():String {
			throw new IllegalOperationError( "Metodo no disponible" );
		}
		
		/**
		 * Define si el boton soporta transicion por frame.
		 */
		public function get frameTransition():Boolean {
			return this._frameTransition;
		}
		
		public function set frameTransition( value:Boolean ):void {
			this._frameTransition = value;
		}
		
		/**
		 * Enabled.
		 */
		public override function set enabled( value:Boolean ):void {
			
			if( value != this.enabled ){
				
				super.enabled = value;
				
				var status:String;
				
				if( ! value ){
					status = BasicButton.DISABLED;
					this.PropertyManager( false );
				}else{
					status = MouseEvent.MOUSE_OUT;
					this.PropertyManager( true );
				}
				
				this.StyleManager( status );
				
			}
			
		}
		
		/**
		 * Config.
		 */
		private function Config( event:Event ):void {
			
			this.PropertyManager( true  );
			this.StyleManager( MouseEvent.MOUSE_OUT );
			
			this.addEventListener( MouseEvent.MOUSE_UP, MouseManager );
			this.addEventListener( MouseEvent.MOUSE_DOWN, MouseManager );
			this.addEventListener( MouseEvent.MOUSE_OUT, MouseManager );
			this.addEventListener( MouseEvent.MOUSE_OVER, MouseManager );
			this.addEventListener( Event.REMOVED_FROM_STAGE, purge );
			this.removeEventListener( Event.ADDED_TO_STAGE, Config );
			
			if( this.totalFrames > 4 ){
				this._frameTransition = true;
			}
			
		}
		
		/**
		 * BasicPropertyManager.
		 */
		private function PropertyManager( value:Boolean ):void {
			
			this.buttonMode = value;
			this.useHandCursor = value;
			this.mouseEnabled = value;
			
			this.mouseChildren = false;
			
		}
		
		/**
		 * MouseManager.
		 */
		private function MouseManager( event:MouseEvent ):void {
			
			if( this.enabled ) {
				this.StyleManager( event.type );
			}
			
		}
		
		/**
		 * StyleManager.
		 */
		protected function StyleManager( status:String = null ):void {
			
			switch( status ){
				
				case BasicButton.DISABLED:
					if( ! this._frameTransition ){
						this.gotoAndStop( 4 );
					}else{
						this.gotoAndPlay( BasicButton.DISABLED );
					}
					break;
				
				case MouseEvent.MOUSE_DOWN:
					if( ! this._frameTransition ){
						this.gotoAndStop( 3 );
					}else{
						this.gotoAndPlay( BasicButton.PRESS );
					}
					break;
				
				case MouseEvent.MOUSE_UP:
				case MouseEvent.MOUSE_OVER:
					if( ! this._frameTransition ) {
						this.gotoAndStop( 2 );
					}else{
						if( status != MouseEvent.MOUSE_UP ){
							this.gotoAndPlay( BasicButton.OVER );
						}else{
							this.gotoAndPlay( BasicButton.UP );
						}
					}
					break;
				
				default:
				case MouseEvent.MOUSE_OUT:
					if( ! this._frameTransition ) {
						this.gotoAndStop( 1 );
					}else{
						this.gotoAndPlay( BasicButton.OUT );
					}
					break;
				
			}
			
		}
		
		/**
		 * Purger.
		 */
		public override function purge(...rest):void {
			
			this.removeEventListener( MouseEvent.MOUSE_UP, MouseManager );
			this.removeEventListener( MouseEvent.MOUSE_DOWN, MouseManager );
			this.removeEventListener( MouseEvent.MOUSE_OUT, MouseManager );
			this.removeEventListener( MouseEvent.MOUSE_OVER, MouseManager );
			this.removeEventListener( Event.REMOVED_FROM_STAGE, purge );
			super.purge();
			
		}
		
	}
	
}