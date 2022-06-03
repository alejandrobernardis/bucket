package activia.simon.shooter.ui.actors {
	import activia.simon.shooter.core.DataLayer;
	import activia.simon.shooter.ui.assets.Pointer;

	import caurina.transitions.Tweener;

	import pq.log.Debugger;
	import pq.ui.Size;
	import pq.ui.UIComponent;
	import pq.utils.ClassUtil;
	import pq.utils.StringUtil;

	import flash.display.Shape;
	import flash.display.Sprite;
	import flash.events.Event;
	import flash.events.TimerEvent;
	import flash.geom.Point;
	import flash.geom.Rectangle;
	import flash.ui.Mouse;
	import flash.utils.Timer;
	
	public class ActorFactory extends UIComponent {
		
		private static var $instance:ActorFactory;
		public static function get instance():ActorFactory { return $instance; }
		
		private var _isInit:Boolean;
		private var _assetsList:Object;
		
		private var _stageArea:Rectangle;
		private var _stageExit:Shape;
		private var _stageMask:Shape;
		private var _stageHolder:Sprite;
		private var _size:Size;
		
		private var _particleTime:Timer;
		private var _particleLevel:uint;
		private var _particleMin:uint;
		private var _particleMax:uint; 
		
		private var _pointer:Pointer;
		
		private var _count:uint = 0;
		private var _actors:uint = 0;
		private var _critical:Number;
		
		    
		
		public function ActorFactory() {
			super();
		}
		
		public function init():void {
			
			if ( this._isInit ) return;
			this._isInit = true;
			$instance = this;
			
			// Actors
			
			this._assetsList = new Object();
			
			for each ( var node:XML in this.data..asset ) {
				if ( ! StringUtil.isEmpty( node.@id ) ) {
					this._assetsList[ node.@id.toString() ] = {
						id: node.@id.toString(), 
						actor: new ActorAssets( XML( node.toString() ) )
					};
				}
			}
			
			// Properties
			
			this._particleLevel = 1;
			this._particleMin = this.data.assets.@min;
			this._particleMax = this.data.assets.@max;
			this._critical = this.data.critical.text();
			
			// Display Objects
			
			this._stageArea = new Rectangle( 0, 0, size.width, size.height );
			
			this._stageMask = new Shape();
			this._stageMask.graphics.beginFill(0x00FF00);
			this._stageMask.graphics.drawRect( 0, 0, size.width, size.height );
			this._stageMask.graphics.endFill();
			//this._stageMask.alpha = .3;
			
			this._stageHolder = new Sprite();
			this._stageHolder.mask = this._stageMask;
			this._stageHolder.addEventListener( Event.ADDED_TO_STAGE, AddedToStage );
			
			this._pointer = new Pointer();
			this._pointer.scale(.5);
			this.addEventListener( Event.ENTER_FRAME, MouseHandler );
			
			this.addChild( this._stageHolder );
			this.addChild( this._stageMask );
			this.addChild( this._pointer );
			
			Debugger.INFO( this, "Init Actor Factory." );
			Debugger.INFO( this, this.data );
			
		}
		
		public function increment():void { 
			this._actors++; 
		}
		
		public function decrement():void { 
			if ( this._actors > 1 ) {
				this._actors--; 
			}
		}
		
		public function destroy():void {
			
			this.stopAllMotion();
			this.removeEventListener( Event.ENTER_FRAME, MouseHandler );
			
			this._particleTime.stop();
			this._particleTime.removeEventListener( TimerEvent.TIMER, add );
			
		}
		
		public function get size():Size {
			if ( this._size == null ) {
				this._size = new Size( this.data.area.text() );
			} return this._size;
		}
		
		public function get pointer():Pointer {
			return this._pointer;
		}
		
		public function forceFrameRate():void {
			if ( ! DataLayer.SCOPE.stage ) return;
			DataLayer.SCOPE.stage.frameRate = Number( this.data.framerate.text() );
		}
		
		public function finished():void {
			
			this.removeEventListener( Event.ENTER_FRAME, MouseHandler );
			
			this._stageExit = new Shape();
			this._stageExit.graphics.beginFill(0x3B223F);
			this._stageExit.graphics.drawRect( 0, 0, size.width, size.height );
			this._stageExit.graphics.endFill();
			this._stageExit.alpha = 0;
			
			this.addChild( this._stageExit );
			Tweener.addTween( this._stageExit, { alpha:.9, time:.5, transition:"linear", onComplete:DataLayer.SCREEN.sGameOver } );
			
		}
		
		public override function purge(...rest):void {
			
			this.destroy();
			Debugger.ERROR( this, "Destroy" );
			
			this._isInit = undefined;
			this._assetsList = null;
			this._stageArea = null;
			this._stageMask = null;
			this._stageHolder = null;
			this._size = null;	
			this._count = undefined;
			
			ActorFactory.$instance = null;
			
			super.purge();
			
		}
		
		public function get level():uint {
			return this._particleLevel;
		}
		
		public function set level( value:uint ):void {
			this._particleLevel = value;
			this._particleTime.delay = this.ResolveDelay( this._particleLevel );
			this.ResolveTimer();
		}
		
		public function applyWildcard():void {
			
			var actor:Actor;
			
			for( var a:uint = 0; a < this._stageHolder.numChildren; a ++ ){
				if ( this._stageHolder.getChildAt(a) != null && this._stageHolder.getChildAt(a) is Actor ) {					
					actor = this._stageHolder.getChildAt(a) as Actor;					
					if ( actor.type == "protons" ) {
						ProtonsBomb( actor ).updateScore();
					}					
				}
			}
			
		}
		
		public function stopAllMotion():void { 
			this._particleTime.stop();
			this.removeEventListener( Event.ENTER_FRAME, MouseHandler );
			this.ResolveMotion(0); 
		}
		
		public function startAllMotion():void { 
			this.ResolveMotion(1); 
		}
		
		public function pauseAllMotion():void { 
			this._particleTime.stop();
			this.removeEventListener( Event.ENTER_FRAME, MouseHandler );
			this.ResolveMotion(2); 
		}
		
		public function resumeAllMotion():void { 
			this.ResolveMotion(3);
			this.addEventListener( Event.ENTER_FRAME, MouseHandler );
			this._particleTime.start(); 
		}
		
		private function ResolveMotion( value:uint ):void {
			
			var actor:Actor;
			
			for( var a:uint = 0; a < this._stageHolder.numChildren; a ++ ){
				
				if ( this._stageHolder.getChildAt(a) != null && this._stageHolder.getChildAt(a) is Actor ) {
					
					actor = this._stageHolder.getChildAt(a) as Actor;
					
					switch(value){
						
						case 0: 
							actor.stopMotion(); 
							break;
							
						case 1: 
							actor.startMotion(); 
							break;
							
						case 2: 
						case 3: 
							actor.resumeMotion(); 
							break;
							
					}
					
				}
				
			}
			
		}
		
		private function add( e:TimerEvent = null ):void { 	
			
			var a:uint;
			//var aold:Position;
			var actor:Actor;
			
			if ( this._actors > this._critical ) {
				Debugger.CRITICAL( this, this._actors, "El numero de elementos es mayor a " + this.data.critical.text() );
				return;
			}
			
			var aquantity:Number = this.toLimit (
				Math.round( Math.random() * this._particleMax ),
				this._particleMin,
				this._particleMax
			);
			
			if ( this._actors + aquantity > this._critical ) {
				aquantity = this._critical - this._actors;
			}
			
			for ( a = 0; a < aquantity; a++ ) {
				actor = ResolveActor();
				actor.y = size.height * Math.random();
				actor.x = -40 * a / .8;
				actor.startMotion();
				this._stageHolder.addChild( Sprite( actor ) );
				this.increment();
			}
			
		}
		
		public function toLimit ( value:Number, min:Number, max:Number ):Number {
			return new Number( Math.min( max, Math.max( min, value ) ) );
		}
		
		public function isModule ( value:Number, mod:Number ):Boolean {
			return new Boolean( ( value % mod ) == 0 );
		}
		
		private function ResolveActor():Actor {
			
			this._count ++;
			
			var actor:ActorAssets;
			
			if ( isModule( this._count, this._assetsList.allies.actor.coef ) ) {
				actor = this._assetsList.allies.actor;
			} else if ( isModule( this._count, this._assetsList.acid.actor.coef ) ) {
				actor = this._assetsList.acid.actor;
			} else if ( isModule( this._count, this._assetsList.threats.actor.coef ) ) {
				actor = this._assetsList.threats.actor;
			} else {
				actor = this._assetsList.protons.actor;
			}
			
			var asset:Actor = ClassUtil.create( actor.controller ) as Actor;
			
			asset.type = actor.id;
			asset.angle = Math.round( Math.random() * Number( DataLayer.CONFIG_GAME.tween.angle.text() ) );
			asset.sound = actor.sound;
			
			if( actor.value.search( /^(\-\+)?\d*/ ) > -1 ) {
				asset.points = actor.value;
			} else if ( actor.value == "*" ){
				asset.wildcard = true;
			}
			
			asset.scale ( 
				this.toLimit (
					Math.random() * actor.scaleMax,
					actor.scaleMin,
					actor.scaleMax
				)
			);
				
			if ( asset.type == "allies" || this._particleLevel == 3 ){
				asset.speedX = this.toLimit (
					Math.random() * actor.speedMax,
					actor.speedMax / 2,
					actor.speedMax
				);
			} else if ( this._particleLevel == 2 ){
				asset.speedX = Math.round( actor.speedMax / 2 );
			} else {
				asset.speedX = this.toLimit (
					Math.random() * ( actor.speedMax / 2 ),
					actor.speedMin,
					actor.speedMax / 2
				);
			}
			
			return asset;
			
		}
		
		private function ResolveDelay( value:uint ):Number {
			if ( StringUtil.isEmpty( this.data.delay.level.( @id == value ) ) ) return NaN; 
			return Number( this.data.delay.level.( @id == value ).toString() );
		}
		
		private function ResolveTimer():void {
			
			if ( this._particleTime == null ) {
				this._particleTime = new Timer( this.ResolveDelay( this._particleLevel ) );
				this._particleTime.addEventListener( TimerEvent.TIMER, add );
			} else {
				this._particleTime.reset();
			}			
			
			this._particleTime.start();
			
		}
		
		private function MouseHandler(e:Event):void {
			
			var point:Point = new Point();
			point.x = this._stageHolder.mouseX;
			point.y = this._stageHolder.mouseY;
			
			if( point.x < 0 || point.y < 0 ){
				Mouse.show();
			} else {				
				Mouse.hide();
				this._pointer.x = this.mouseX;
				this._pointer.y = this.mouseY;
			}
			
		}
		
		private function AddedToStage(e:Event):void {
			
			if ( e.currentTarget.stage ) {
				this.add();
				this.ResolveTimer();
			}
			
			e.currentTarget.removeEventListener(Event.ADDED_TO_STAGE, AddedToStage);
			
		}
		
	}

}