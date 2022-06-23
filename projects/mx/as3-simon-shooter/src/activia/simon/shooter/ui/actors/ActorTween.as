package activia.simon.shooter.ui.actors {
	import activia.simon.shooter.core.DataLayer;

	import pq.ui.Size;

	import org.goasap.items.LinearGo;

	import flash.events.Event;
	
	
	public class ActorTween extends LinearGo {
		
		private var _target:Actor;
		private var _positionX:Number;
		private var _positionY:Number;	
		private var _endPoint:uint;
		
		public function ActorTween( target:Actor, duration:Number = NaN ) {
			this._target = target;			
			this.duration = duration;
		}
		
		public override function start():Boolean {
			
			this._positionX = - this._target.width;
			this._positionY = this._target.y;
			
			var size:Size = new Size( DataLayer.CONFIG_GAME.config.canvas.size.text() );
			this._endPoint = size.width + this._target.width;
			
			return super.start();
			
		}
		
		protected override function onUpdate( type:String ):void {
			
			this._target.x += this._target.speedX * ( Math.random() * this._target.delta ) / this._target.desacX;
			this._target.y = this._positionY + ( Math.sin( this._target.angle ) * this._target.range ) / this._target.desacY;
			this._target.angle += this._target.speedY;
			
			if ( this._target.x >= this._endPoint ) {
				this._target.visible = false;
				if ( this.stop() ) {
					this.dispatchEvent( new Event( Event.COMPLETE ) );
				}
			}
			
		}
		
		public function purge(...rest):void {
			this._positionX = undefined;
			this._positionY = undefined;
			this._endPoint = undefined;
			this._target = null;
		}
		
	}

}