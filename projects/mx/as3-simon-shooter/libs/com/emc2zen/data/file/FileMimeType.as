/**
* @private
* @license	GNU GPLv2
*
* Copyright (C) 2007  Polly Jex.
* 
* This program is free software; you can redistribute it and/or
* modify it under the terms of the GNU General Public License
* as published by the Free Software Foundation; either version 2
* of the License, or (at your option) any later version.
* 
* This program is distributed in the hope that it will be useful,
* but WITHOUT ANY WARRANTY; without even the implied warranty of
* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
* GNU General Public License for more details.
* 
* You should have received a copy of the GNU General Public License
* along with this program; if not, write to the Free Software
* Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, 
* MA  02110-1301, USA.
*
* @see	http://www.gnu.org/licenses/old-licenses/gpl-2.0.html
*/

package com.emc2zen.data.file {

	/**
	* @import
	*/
	
	import com.emc2zen.core.Constant;
	import com.emc2zen.core.CoreStatic;
	
	/**
	* Modelo para la implementacion de tipos de mime para archivos.
	* @author	PollyJex
	*/
	public class FileMimeType extends CoreStatic {
		
		/**
		* Constante MIME_BZ2: application/x-bzip2 ( ID: 0 ).
		*/
		public static const MIME_BZ2:Constant = new Constant( "application/x-bzip2", 0, $CLASS_REF );
		
		/**
		* Constante MIME_GZ: application/x-gzip ( ID: 1 ).
		*/
		public static const MIME_GZ:Constant = new Constant( "application/x-gzip", 1, $CLASS_REF );
		
		/**
		* Constante MIME_PDF: application/pdf ( ID: 2 ).
		*/
		public static const MIME_PDF:Constant = new Constant( "application/pdf", 2, $CLASS_REF );
		
		/**
		* Constante MIME_SWF: application/x-shockwave-flash ( ID: 3 ).
		*/
		public static const MIME_SWF:Constant = new Constant( "application/x-shockwave-flash", 3, $CLASS_REF );
		
		/**
		* Constante MIME_TAR: application/x-tar ( ID: 4 ).
		*/
		public static const MIME_TAR:Constant = new Constant( "application/x-tar", 4, $CLASS_REF );
		
		/**
		* Constante MIME_TGZ: application/x-zip ( ID: 5 ).
		*/
		public static const MIME_TGZ:Constant = new Constant( "application/x-gzip", 5, $CLASS_REF );
		
		/**
		* Constante MIME_ZIP: application/zip ( ID: 6 ).
		*/
		public static const MIME_ZIP:Constant = new Constant( "application/zip", 6, $CLASS_REF );
		
		
		
		/**
		* Constante MIME_BMP: image/bmp ( ID: 7 ).
		*/
		public static const MIME_BMP:Constant = new Constant( "image/bmp", 7, $CLASS_REF );
		
		/**
		* Constante MIME_GIF: image/gif ( ID: 8 ).
		*/
		public static const MIME_GIF:Constant = new Constant( "image/gif", 8, $CLASS_REF );
		
		/**
		* Constante MIME_JPE: image/jpeg ( ID: 9 ).
		*/
		public static const MIME_JPE:Constant = new Constant( "image/jpeg", 9, $CLASS_REF );
		
		/**
		* Constante MIME_JPEG: image/jpeg ( ID: 10 ).
		*/
		public static const MIME_JPEG:Constant = new Constant( "image/jpeg", 10, $CLASS_REF );
		
		/**
		* Constante MIME_JPG: image/jpeg ( ID: 11 ).
		*/
		public static const MIME_JPG:Constant = new Constant( "image/jpeg", 11, $CLASS_REF );
		
		/**
		* Constante MIME_PNG: image/png ( ID: 12 ).
		*/
		public static const MIME_PNG:Constant = new Constant( "image/png", 12, $CLASS_REF );
		
		/**
		* Constante MIME_TIF: image/tiff ( ID: 13 ).
		*/
		public static const MIME_TIF:Constant = new Constant( "image/tiff", 13, $CLASS_REF );
		
		/**
		* Constante MIME_TIFF: image/tiff ( ID: 14 ).
		*/
		public static const MIME_TIFF:Constant = new Constant( "image/tiff", 14, $CLASS_REF );
		
		
		
		/**
		* Constante MIME_CSS: text/css ( ID: 15 ).
		*/
		public static const MIME_CSS:Constant = new Constant( "text/css", 15, $CLASS_REF );
		
		/**
		* Constante MIME_HTM: text/html ( ID: 16 ).
		*/
		public static const MIME_HTM:Constant = new Constant( "text/html", 16, $CLASS_REF );
		
		/**
		* Constante MIME_HTML: text/html ( ID: 17 ).
		*/
		public static const MIME_HTML:Constant = new Constant( "text/html", 17, $CLASS_REF );
		
		/**
		* Constante MIME_JS: text/javascript ( ID: 18 ).
		*/
		public static const MIME_JS:Constant = new Constant( "text/javascript", 8, $CLASS_REF );
		
		/**
		* Constante MIME_RTF: text/rtf ( ID: 19 ).
		*/
		public static const MIME_RTF:Constant = new Constant( "text/rtf", 19, $CLASS_REF );
		
		/**
		* Constante MIME_TXT: text/plain ( ID: 20 ).
		*/
		public static const MIME_TXT:Constant = new Constant( "text/plain", 20, $CLASS_REF );
		
		/**
		* Constante MIME_XML: text/xml ( ID: 21 ).
		*/
		public static const MIME_XML:Constant = new Constant( "text/xml", 21, $CLASS_REF );
		
		
		
		/**
		* Constante MIME_AVI: video/x-msvideo ( ID: 22 ).
		*/
		public static const MIME_AVI:Constant = new Constant( "video/x-msvideo", 22, $CLASS_REF );
		
		/**
		* Constante MIME_MOV: video/quicktime ( ID: 23 ).
		*/
		public static const MIME_MOV:Constant = new Constant( "video/quicktime", 23, $CLASS_REF );
		
		/**
		* Constante MIME_MPE: video/mpeg ( ID: 24 ).
		*/
		public static const MIME_MPE:Constant = new Constant( "video/mpeg", 24, $CLASS_REF );
		
		/**
		* Constante MIME_MPEG: video/mpeg ( ID: 25 ).
		*/
		public static const MIME_MPEG:Constant = new Constant( "video/mpeg", 25, $CLASS_REF );
		
		/**
		* Constante MIME_MPG: video/mpeg ( ID: 26 ).
		*/
		public static const MIME_MPG:Constant = new Constant( "video/mpeg", 26, $CLASS_REF );
		
		/**
		* Constante MIME_QT: video/quicktime ( ID: 27 ).
		*/
		public static const MIME_QT:Constant = new Constant( "video/quicktime", 27, $CLASS_REF );
		
		
		
		/**
		* Referencia de la clase.
		*/
		private static const $CLASS_REF:String = "FileMimeType";
		
		
		
		/**
		* Resuelve el tipo de MIME por el numero de ID.
		* @param	value	Identificador numerico.
		* @return	String
		*/
		public static function resolveMimeTypeAsName( value:int ):String {
			
			var list:Array = new Array(
				
				MIME_BZ2, 	MIME_GZ, 	MIME_PDF, 	MIME_SWF,
				MIME_TAR, 	MIME_TGZ, 	MIME_ZIP, 	MIME_BMP,
				MIME_GIF, 	MIME_JPE, 	MIME_JPEG, 	MIME_JPG,
				MIME_PNG, 	MIME_TIF, 	MIME_TIFF, 	MIME_CSS,
				MIME_HTM, 	MIME_HTML, 	MIME_JS, 	MIME_RTF,
				MIME_TXT, 	MIME_XML, 	MIME_AVI, 	MIME_MOV,
				MIME_MPE, 	MIME_MPEG,	MIME_MPG,	MIME_QT
				
			)
			
			if( value > -1 && value < list.length ){				
				return list[ value ].name;				
			}
			
			return null;
			
		}
		
	}
	
}
