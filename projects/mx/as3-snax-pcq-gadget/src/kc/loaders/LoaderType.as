
package kc.loaders {
	import kc.core.KCStatic;
	import kc.utils.ClassUtil;
	import kc.utils.ExceptionUtil;
	import kc.utils.RegExpUtil;
	import kc.utils.StringUtil;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class LoaderType extends KCStatic {

		// @const

		public static const ERROR:String = "This version is not compatible with the format: {1}";

		public static const FILE_TEXT:String 	= "fileText";
		public static const FILE_CONFIG:String 	= "fileConfig";
		public static const FILE_XML:String		= "fileXML";
		public static const FILE_ASSET:String 	= "fileAsset";
		public static const FILE_SOUND:String 	= "fileSound";
		public static const FILE_VIDEO:String 	= "fileVideo";

		// @variables

		private static var FILES_LIST:Array = [
			[ FILE_TEXT, 	RegExpUtil.PATTERN_FILE_TEXT, 	"kc.loaders::TextLoader" 	],
			[ FILE_CONFIG, 	RegExpUtil.PATTERN_FILE_CONFIG, "kc.core::KCConfig" 		],
			[ FILE_XML, 	RegExpUtil.PATTERN_FILE_XML, 	"kc.loaders::XMLLoader" 	],
			[ FILE_ASSET, 	RegExpUtil.PATTERN_FILE_ASSET, 	"kc.loaders::AssetLoader" 	],
			[ FILE_SOUND, 	RegExpUtil.PATTERN_FILE_SOUND, 	"kc.loaders::SoundLoader" 	],
			[ FILE_VIDEO, 	RegExpUtil.PATTERN_FILE_VIDEO, 	"" 							]
		];

		private static var NOT_FOUND:int = -1;

		// @constructor

		public function LoaderType() {
			super();
		}

		// @methods

		public static function getType( value:String ):String {

			if( ! value )
				return null;

			for( var a:uint = 0; a < FILES_LIST.length; a++ ){
				if( value.search( FILES_LIST[a][1] ) != NOT_FOUND ){
					return FILES_LIST[a][0];
				}
			}

			return null;

		}

		public static function getTypeClass( value:String ):* {

			if( ! value )
				return null;

			for( var a:uint = 0; a < FILES_LIST.length; a++ ){
				if( value.search( new RegExp( FILES_LIST[a][0], "gi" ) ) != NOT_FOUND ){
					return ClassUtil.getClass( FILES_LIST[a][2] );
				}
			}

			return ExceptionUtil.ViewError(
				StringUtil.substitute( ERROR, value )
			);

		}

		public static function getURLAsTypeClass( value:String ):* {

			return getTypeClass( getType( value ) );

		}
	}
}

import kc.loaders.*;

class hack{
	public function hack(){
		var a:Array = [
			AbstractLoader,
			AssetLoader,
			BinaryTextLoader,
			SoundLoader,
			TextLoader,
			VariablesTextLoader,
			XMLLoader
		]; trace(a);
	}
}
