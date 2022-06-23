package activia.simon.shooter.ui.assets {
	import pq.ui.UIComponent;
	import pq.utils.StringUtil;

	import flash.text.TextField;
	import flash.text.TextFormat;
	
	
	public class RankingCell extends UIComponent {
		
		public function RankingCell() {
			super();
		}		
		
		public function set positionNumber( value:Number ):void {
			TextField( this.getChildByName( "txPosition" ) ).text = StringUtil.substitute (
				this.data.position.text(),
				String( ( value < 10 ) ? "0"+value : value )
			);
		}
		
		public function set positionName( value:String ):void {
			TextField( this.getChildByName( "txName" ) ).text = StringUtil.substitute (
				this.data.name.text(),
				value
			);
		}
		
		public function set positionScore( value:Number ):void {
			TextField( this.getChildByName( "txScore" ) ).text = StringUtil.substitute (
				this.data.score.text(),
				String( value )
			);
		}
		
		public function myPosition():void {
			
			var tx:TextField;
			var tf:TextFormat;
			
			for ( var a:uint = 0; a < this.numChildren; a++ ) {
				if ( this.getChildAt(a) is TextField ) {
					tx = TextField( this.getChildAt(a) );
					tf = tx.defaultTextFormat;
					tf.color = 0xFAEC07;
					tx.setTextFormat(tf);
				}
			}
			
		}
		
	}

}