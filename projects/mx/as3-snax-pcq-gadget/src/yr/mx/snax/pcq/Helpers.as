package yr.mx.snax.pcq {
	import kc.api.IIterator;
	import kc.logging.SimpleLog;
	import kc.tda.SimpleMap;

	import flash.display.Sprite;

	public class Helpers extends Sprite {
		
		public function Helpers() {
			super();
			create_list();
		}
		
		private static const encodingID:String = "I";
		private static const encodingKey:String = "9B3B6EDFBFC34F98B94A305D2ED7C308";

		public static function create_list():void {
			var list:SimpleMap = new SimpleMap();
			list.add("BJEOa221K-t3", "quieras.");
			list.add("WZjp.0XXQ>m|", "ponlo");
			list.add("EcY6O@U1X8f*", "como");
			list.add("#5r1N6dNRJ!@", "Con Snax,");
			list.add("TS(m>sZ$q1q=", "ponlo como");
			list.add("h}g*pfU2!5ls", "Raya, diviértete y");
			list.add("Q51}DM%@DnNg", "quieras con");
			list.add("T~T5q#0rhU:4", "Snax.");
			var iter:IIterator = list.iterator();
			while(iter.hasNext()){
				var item:* = iter.next();
				SimpleLog.print(item);
				var v:String = Helpers.doit(item[1], item[0]);
				var k:String = Helpers.doit(item[0], v);
				SimpleLog.print(v, k);
				var h:String = v + k.substr(1);
				SimpleLog.print(h);
				var kd:String = Helpers.rdoit(k, v);
				var vd:String = Helpers.rdoit(v, kd);
				SimpleLog.print(vd, kd);
				var a:String = h.substr(0,1)+h.substr(-36);
				var b:String = h.substr(0, h.length-36);
				var w:String = Helpers.rdoit(b,Helpers.rdoit(a,b));
				SimpleLog.print(a, b, w);
				trace("\n");
			}
		}

		public static function doit( s:String, k:String=null ):String {
			var theResult:String = "";
			var iKey:int = 0;
			var i:int;
			if(!k)
				k = encodingKey;
			for (i = 0; i < s.length; ++i ) {
				var theNumber:int = s.charCodeAt(i) ^ k.charCodeAt(iKey);
				var xored:String = theNumber.toString();
				if (theNumber < 10) {
					xored = "00" + xored;
				}else if (theNumber < 100){
					xored = "0" + xored;
				}
				theResult = theResult + xored;
				if(iKey == k.length-1){
					iKey = 0;
				}else{
					iKey++;
				}
			}
			return (encodingID + theResult);
		}

		public static function rdoit( s:String, k:String=null ):String {
			var iKey:int = 0;
			var coef:uint = 3;
			var str:String = s.substring( 1 );
			var result:String = new String("");
			if(!k)
				k = encodingKey;
			for ( var a:uint = 0; a < ( str.length / coef ); a++ ) {
				var pos:uint = a * coef;
				var xored:String = str.substring( pos, pos + coef );
				result = result + String.fromCharCode( int( xored ) ^ k.charCodeAt(iKey) );
				if(iKey == k.length-1){
					iKey = 0;
				}else{
					iKey++;
				}
			}
			return result;
		}
		
	}
	
}
