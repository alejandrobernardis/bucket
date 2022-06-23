package activia.simon.shooter.ui.actors {
	import activia.simon.shooter.core.DataLayer;

	import pq.ui.StepManager;

	import flash.display.Sprite;
	import flash.errors.IllegalOperationError;
	
	
	public class AbstractActorComplex extends StepManager implements ActorComplex {
		
		protected var _type:String;
		protected var _points:String;
		protected var _wildcard:Boolean;
		protected var _actorTween:ActorTween;		
		
		protected var _speedX:Number;
		protected var _speedY:Number;
		protected var _desacX:Number;
		protected var _desacY:Number;		
		protected var _angle:Number;
		protected var _range:Number;
		protected var _delta:Number;
		protected var _sound:String;
		
		public function AbstractActorComplex() {
			super();
			this.tween = true;
		}
		
		public function get type():String { 
			return this._type; 
		}
		
		public function set type( value:String ):void {
			this._type = value;
		}
		
		public function get points():String { 
			return this._points; 
		}
		
		public function set points( value:String ):void {
			this._points = value;
		}
		
		public function set wildcard( value:Boolean ):void {
			this._wildcard = value;
		}
		
		public function get actorTween():ActorTween { 
			return this._actorTween; 
		}
		
		/* OVERRIDE */
		
		protected var $error:String = "Metodo no Disponible.";
		
		
		public function init():void {
			
			var node:XML = XML( DataLayer.CONFIG_GAME.tween.toString() );
			
			if( isNaN( this.speedX ) ) this.speedX = Number( node.speedx.text() );
			if( isNaN( this.speedY ) ) this.speedY = Number( node.speedy.text() );
			if( isNaN( this.desacX ) ) this.desacX = Number( node.desacx.text() );
			if( isNaN( this.desacY ) ) this.desacY = Number( node.desacy.text() );
			if( isNaN( this.angle ) ) this.angle = Number( node.angle.text() );
			if( isNaN( this.range ) ) this.range = Number( node.range.text() );
			if( isNaN( this.delta ) ) this.delta = Number( node.delta.text() );
			
			this.firstStep();
			
		}
		
		public function destroy():void {
			
			if ( this._actorTween != null ) {
				this._actorTween.stop();
				this._actorTween.purge();
				this._actorTween = null;
			}
			
			var scope:Sprite = Sprite( this.parent );
			
			if ( scope.contains( this ) ) {
				scope.removeChild( this );
			}
			
		}
		
		public function startMotion():void{ 
			throw new IllegalOperationError( $error );
		}
		
		public function pauseMotion():void{ 
			throw new IllegalOperationError( $error );
		}
		
		public function resumeMotion():void { 
			throw new IllegalOperationError( $error );
		}
		
		public function stopMotion():void { 
			throw new IllegalOperationError( $error );
		}
		
		/* GETTERS&SETTERS */
		
		public function get duration():Number {
			return ( this._actorTween != null ) ? this._actorTween.duration : NaN;
		}
		
		public function set duration(seconds:Number):void {
			if ( this._actorTween == null ) return;
			this._actorTween.duration = seconds;
		}
		
		public function get speedX():Number { 
			return this._speedX; 
		}
		
		public function set speedX(value:Number):void {
			this._speedX = value;
		}
		
		public function get speedY():Number { 
			return this._speedY; 
		}
		
		public function set speedY(value:Number):void {
			this._speedY = value;
		}
		
		public function get desacX():Number { 
			return this._desacX; 
		}
		
		public function set desacX(value:Number):void {
			this._desacX = value;
		}
		
		public function get desacY():Number { 
			return this._desacY; 
		}
		
		public function set desacY(value:Number):void {
			this._desacY = value;
		}
		
		public function get angle():Number { 
			return this._angle; 
		}
		
		public function set angle(value:Number):void {
			this._angle = value;
		}
		
		public function get range():Number { 
			return this._range; 
		}
		
		public function set range(value:Number):void {
			this._range = value;
		}
		
		public function get delta():Number { 
			return this._delta; 
		}
		
		public function set delta(value:Number):void {
			this._delta = value;
		}
		
		public function get sound():String { 
			return this._sound; 
		}
		
		public function set sound(value:String):void {
			this._sound = value;
		}
		
		/* PURGE */
		
		public override function purge(...rest):void {
			
			this._type = null;
			this._points = undefined;
			this._actorTween = null;
			
			this._speedX = undefined;
			this._speedY = undefined;
			this._desacX = undefined;
			this._desacY = undefined;		
			this._angle = undefined;
			this._range = undefined;
			this._delta = undefined;
			this._sound = undefined;
			
			super.purge();
			
		}
		
	}

}