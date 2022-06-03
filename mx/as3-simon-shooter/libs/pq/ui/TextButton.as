
package pq.ui {
	
	import flash.display.MovieClip;
	import flash.events.MouseEvent;
	import flash.text.TextField;
	import flash.text.TextFieldAutoSize;
	
	public class TextButton extends BasicButton {
		
		/** 
		 * Nombre de los elementos por default.
		 */
		private static const MC_LABEL:String = "mcLabel";
		private static const TX_LABEL:String = "txLabel";
			
		/**
		 * Propiedades basicas de estilo.
		 */
		private var TEXT_OUT:uint = 0x3C3C3C;
		private var TEXT_OVER:uint = 0xFF0000;
		private var TEXT_PRESS:uint = 0xAA0000;
		private var TEXT_DISABLED:uint = 0xCCCCCC;
		
		/**
		 * Constructor.
		 */
		public function TextButton() {
			super();
		}
		
		/**
		 * Label.
		 */
		public override function set label( value:String ):void {
			var tx:TextField = this.getTextField();
			tx.autoSize = TextFieldAutoSize.LEFT;
			tx.wordWrap = false;
			tx.text = value;	
		}
		
		public override function get label():String {
			return this.getTextField().text;		
		}
		
		/**
		 * Out Color.
		 */
		public function get colorOut():uint { 
			return this.TEXT_OUT; 
		}
		
		public function set colorOut( value:uint ):void { 
			this.TEXT_OUT = value; 
		}
		
		/**
		 * Over Color.
		 */
		public function get colorOver():uint { 
			return this.TEXT_OVER; 
		}
		
		public function set colorOver( value:uint ):void { 
			this.TEXT_OVER = value; 
		}
		
		/**
		 * Press Color.
		 */
		public function get colorPress():uint {
			return this.TEXT_PRESS;
		}
		
		public function set colorPress( value:uint ):void {
			this.TEXT_PRESS = value;
		}
			
		/**
		 * Disabled Color.
		 */
		public function get colorDisabled():uint {
			return this.TEXT_DISABLED;
		}
		
		public function set colorDisabled( value:uint ):void {
			this.TEXT_DISABLED = value;
		}
		
		/**
		 * StyleManager.
		 */
		protected override function StyleManager( status:String = null ):void {
			
			super.StyleManager( status );
			
			if( isTextField() ){
			
				var txColor:uint;
				
				switch( status ){
					
					case BasicButton.DISABLED:
						txColor = TEXT_DISABLED;
						break;
					
					case MouseEvent.MOUSE_DOWN:
						txColor = TEXT_PRESS;
						break;	
						
					case MouseEvent.MOUSE_UP:
					case MouseEvent.MOUSE_OVER:
						txColor = TEXT_OVER;
						break;	
						
					default:
					case MouseEvent.MOUSE_OUT:
						txColor = TEXT_OUT;
						break;	
						
				}
				
				this.getTextField().textColor = txColor;
			
			}
			
		}
		
		private function isTextField():Boolean {
			
			return Boolean( this.getChildByName( TextButton.TX_LABEL ) is TextField );
			
		}
		
		private function getTextField():TextField {
			
			if( isTextField() ){
				return TextField( this.getChildByName( TextButton.TX_LABEL ) );
			}else{
				return TextField( MovieClip( this.getChildByName( TextButton.MC_LABEL ) )[ TextButton.TX_LABEL ] );
			}
			
		}
		
	}
	
}