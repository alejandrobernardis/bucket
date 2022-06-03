package activia.simon.shooter.ui.assets {
	import pq.ui.UIComponent;

	import flash.display.MovieClip;
	import flash.text.TextField;
	
	
	public class Countdown extends UIComponent {
		
		public function Countdown() {
			super();
		}
		
		public function set label( value:String ):void {
			var capsule:MovieClip = MovieClip( this.getChildByName( "mcLabel" ) );
			TextField( capsule.getChildByName( "txLabel" ) ).text = value;
			this.gotoAndPlay( "animation" );
		}
		
	}
	
}