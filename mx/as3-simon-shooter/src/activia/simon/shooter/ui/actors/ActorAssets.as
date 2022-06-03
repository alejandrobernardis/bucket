
package activia.simon.shooter.ui.actors {
	
	
	public class ActorAssets extends Object {
		
		private var _id:String;
		private var _controller:String;
		private var _scaleMin:Number;
		private var _scaleMax:Number;
		private var _speedMin:Number;
		private var _speedMax:Number;
		private var _value:String;
		private var _coef:Number;
		private var _sound:String;
		
		public function ActorAssets( value:XML ) {
			this._id = value.@id;
			this._controller = value.@controller;
			this._scaleMin = Number( value.scmin.text() );
			this._scaleMax = Number( value.scmax.text() );
			this._speedMin = Number( value.spmin.text() );
			this._speedMax = Number( value.spmax.text() );
			this._value = value.value.text();			
			this._coef = Number( value.coef.text() );	
			this._sound = value.sound.text();
		}
		
		public function get id():String { return _id; }
		public function get controller():String { return _controller; }
		public function get scaleMin():Number { return _scaleMin; }
		public function get scaleMax():Number { return _scaleMax; }
		public function get speedMin():Number { return _speedMin; }
		public function get speedMax():Number { return _speedMax; }
		public function get value():String { return _value; }		
		public function get coef():Number { return _coef; }
		public function get sound():String { return _sound; }
		
	}

}
