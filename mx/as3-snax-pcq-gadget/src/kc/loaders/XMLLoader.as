
package kc.loaders {
	import kc.api.IIterator;
	import kc.api.IMap;
	import kc.api.IXMLLoader;
	import kc.tda.SimpleIterator;
	import kc.tda.SimpleMap;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class XMLLoader extends TextLoader implements IXMLLoader {

		// @variables

		protected var _resolveFunction:String;

		// @constructor

		public function XMLLoader() {
			super();
		}

		// @override

		override public function get content():* {
			if( _content is String )
				_content = new XML( String( _content ) );
			return _content;
		}

		override public function purge(...rest):void {
			_resolveFunction = null;
			super.purge();
		}

		// @methods

		public function getValue( node:String ):String {
			var value:XMLList = resolveSimplePath( node );
			return value.text().toString() || null;
		}

		public function resolveAsMap( node:String, attribute:String ):IMap {

			var value:XMLList = resolveSimplePath( node ).children();
			var list:IMap = new SimpleMap( value.length() );

			for each( var element:XML in value ) {
				if( element.@[ attribute ] != undefined ) {
					if( ! _resolveFunction ){
						list.add(
							element.@[ attribute ].toString(),
							element.toString()
						);
					}else{
						list.add(
							this[_resolveFunction].apply(
								this,
								[element.@[ attribute ].toString()]
							),
							this[_resolveFunction].apply(
								this,
								[element.toString()]
							)
						);
					}
				}
			}

			return list;

		}

		public function resolveAsArrayList( node:String, attribute:String = null ):Array {

			var value:XMLList = resolveSimplePath( node ).children();
			var list:Array = new Array();

			for each( var element:XML in value ) {

				if( attribute && element.@[ attribute ] == undefined ){
					continue;
				}

				list.push(
					( ! _resolveFunction )
						? element.toString()
						: this[_resolveFunction].apply( this, [element.toString()] )
				);

			}

			return list;
		}

		public function resolveSimplePath( value:String ):XMLList {

			var list:IIterator = new SimpleIterator( value.split( "." ) );
			var result:XMLList;

			if( list.hasNext() ){
				result = content.elements( list.next() );
				while( list.hasNext() ) {
					result = result.elements( list.next() );
				}
			}

			return result;

		}

	}

}
