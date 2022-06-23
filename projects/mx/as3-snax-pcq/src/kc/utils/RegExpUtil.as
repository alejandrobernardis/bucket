
package kc.utils {
	import kc.core.KCStatic;

	/**
	 * @author Alejandro M. Bernardis (alejandrob@kirikacode.com.ar)
	 */
	public class RegExpUtil extends KCStatic {
		
		// @string
		
		// literal (a-z,0-9,!@#...)
		public static const PATTERN_LITERAL:RegExp = /.+/gi;
		// white space (\t\r\n\v\f)
		public static const PATTERN_WHITE_SPACE:RegExp = /\s/gi;
		// white space left
		public static const PATTERN_WHITE_SPACE_LEFT:RegExp = /^\s+/;
		// white space right
		public static const PATTERN_WHITE_SPACE_RIGHT:RegExp = /\s+$/;
		// ${value}
		public static const PATTERN_HOLDER_VARIABLE:RegExp = /\${([^}]*)}/g;
		// @{value}
		public static const PATTERN_HOLDER_ATTRIBUTE:RegExp = /@{([^}]*)}/g;
		// {1}
		public static const PATTERN_HOLDER_NUMBER:RegExp = /{\d+}/g;
		// name@domain.com
		public static const PATTERN_EMAIL:RegExp = /^[a-z][\w.-]+@\w[\w.-]+\.[\w.-]*[a-z][a-z]$/i;
		
		// @files
		
		// text...
		public static const PATTERN_FILE_TEXT:RegExp = /^.+\.(txt|css|php|jsp|py)/i;
		// asset...
		public static const PATTERN_FILE_ASSET:RegExp = /^.+\.(jpg|jpeg|png|gif|swf)/i;
		// sound...
		public static const PATTERN_FILE_SOUND:RegExp = /^.+\.(mp3|mp4|f4a|f4b)/i;
		// video...
		public static const PATTERN_FILE_VIDEO:RegExp = /^.+\.(flv|mov)/i;
		// XML...
		public static const PATTERN_FILE_XML:RegExp = /^.+\.xml/i;
		// KCConfig...
		public static const PATTERN_FILE_CONFIG:RegExp = /^(((cfg|config|kcc|kcf):).+\.xml)|(.+\.(cfg|kcf))/i;
		
		// @classes
		
		// .Class, :Class, ::Class
		public static const PATTERN_CLASS_NAME:RegExp = /([\:]+|[\.])[A-Z]\w*$/;
		// package.package.package:, package.package.package::
		public static const PATTERN_CLASS_PACKAGE:RegExp = /^[a-z].+([\:]+|[\.])/;
		// :, ::
		public static const PATTERN_CLASS_COLON:RegExp = /\:+/g;
		
		// @config
		
		// {node:0.node:0.@attribute:value}
		public static const PATTERN_DEPENDENCY:RegExp = /\{(([A-Za-z]\w*)(\:\d+)?)([\.]([A-Za-z]\w*)(\:\d+)?)*([\.](\@[A-Za-z]\w*)(\:\w+)?)?\}/g;
		// node:0.node:0.@attribute:value
		public static const PATTERN_DEPENDENCY_PATH:RegExp = /(([A-Za-z]\w*)(\:\d+)?)([\.]([A-Za-z]\w*)(\:\d+)?)*([\.](\@[A-Za-z]\w*)(\:\w+)?)?/g;
		// @attribute:value
		public static const PATTERN_DEPENDENCY_ATTRIBUTE:RegExp = /(\@[a-z]\w*)(\:\w+)?/gi;
		// node:0
		public static const PATTERN_DEPENDENCY_NODE:RegExp = /[a-z]\w*(\:\d*)?/gi;
		// <?xml ... ?>
		public static const PATTERN_VALIDATE_XML_RESULT:RegExp = /^\<.+\>/g;
		// xmlns="http://..." //(xmlns(:\w*)?=\".*?\")/gim;
		public static const PATTERN_NS_DEFINED:RegExp = /(xmlns(:\w*)?="(.*?)")/gim; 
		// <ns:node
		public static const PATTERN_NS_ONODE:RegExp = /<\w+:/gim;
		// </ns:node
		public static const PATTERN_NS_CNODE:RegExp = /<\/\w+:/gim;
		// cfg:http://...
		public static const PATTERN_CONFIG_URL:RegExp = /^(cfg|config|kcc|kcf):/i;
		
		// @constructor
		
		public function RegExpUtil() {
			super( true );
		}
		
	}
	
}
