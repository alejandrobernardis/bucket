package activia.simon.shooter.ui.assets {
	import caurina.transitions.Tweener;

	import pq.ui.UIComponent;

	import flash.display.MovieClip;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.filters.GlowFilter;
	import flash.text.TextField;
	

	public class LabelPoint extends UIComponent {
		
		public function LabelPoint() {
			super();
			this.addEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function $config( e:Event ):void {
			this.addFrameScript( this.totalFrames, Actions );
			this.removeEventListener( Event.ADDED_TO_STAGE, $config );
		}
		
		private function Actions():void {
			this.stop();
			var mc:Sprite = this.parent as Sprite;
			mc.removeChild(this);
		}
		
		public function set point( value:String ):void {
			
			var mc:MovieClip = this.getChildByName("mcLabel") as MovieClip;
			var tx:TextField = mc.getChildByName( "txLabel" ) as TextField;
			tx.text = value;
			
			if( value.search(/^\-/) > -1 ){
				mc.filters = [ new GlowFilter( 0xFF0000, 1, 4, 4, 2 ) ];
			}else{
				mc.filters = [ new GlowFilter( 0xD6D6D6, 1, 4, 4, 2 ) ];
			}
			
			Tweener.addTween( this, 
				{
					y:this.y-20, 
					time:3
				} 
			);
			
			Tweener.addTween( this, 
				{
					alpha:0, 
					time:2
				} 
			);
			
		}
		
	}
	
}