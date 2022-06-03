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

	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.util.ArgumentsUtil;
	import com.emc2zen.util.TypeUtil;
	import flash.net.FileFilter;

	/**
	* Modelo para la implementacion de tipos de archivos.
	* @author	PollyJex
	*/
	public class FileType extends CoreStatic {
		
		/**
		* Constante ALL_FILE ( &#42;.&#42; ).
		*/
		public static const ALL_FILE:FileFilter = new FileFilter( "Todos los Archivos.", "*.*" );		
		
		/**
		* Constante FILE_JPG ( &#42;.jpe; &#42;.jpeg; &#42;.jpg ).
		*/
		public static const FILE_JPG:FileFilter = new FileFilter( "Imagen JPG ( *.jpe; *.jpeg; *.jpg )", "*.jpe;*.jpeg;*.jpg" );
		
		/**
		* Constante FILE_GIF ( &#42;.gif ).
		*/
		public static const FILE_GIF:FileFilter = new FileFilter( "Imagen GIF ( *.gif )", "*.gif" );
		
		/**
		* Constante FILE_PNG ( &#42;.png ).
		*/
		public static const FILE_PNG:FileFilter = new FileFilter( "Imagen PNG ( *.png )", "*.png" );
		
		/**
		* Constante FILE_BMP ( &#42;.bmp ).
		*/
		public static const FILE_BMP:FileFilter = new FileFilter( "Imagen BMP ( *.bmp )", "*.bmp" );
		
		/**
		* Constante FILE_WMV ( &#42;.wmv; &#42;.asf ).
		*/
		public static const FILE_WMV:FileFilter = new FileFilter( "Video Windows Media Video ( *.wmv; *.asf )", "*.wmv;*.asf" );
		
		/**
		* Constante FILE_MOV ( &#42;.mov ).
		*/
		public static const FILE_MOV:FileFilter = new FileFilter( "Video Quick Time ( *.mov )", "*.mov" );
		
		/**
		* Constante FILE_AVI ( &#42;.avi ).
		*/
		public static const FILE_AVI:FileFilter = new FileFilter( "Video AVI ( *.avi )", "*.avi" );
		
		/**
		* Constante FILE_MPEG ( &#42;.mpeg; &#42;.mpg ).
		*/
		public static const FILE_MPEG:FileFilter = new FileFilter( "Video MPEG ( *.mpeg; *.mpg )", "*.mpeg;*.mpg" );
		
		/**
		* Constante FILE_FLV ( &#42;.flv ).
		*/
		public static const FILE_FLV:FileFilter = new FileFilter( "Video FLASH ( *.flv )", "*.flv" );
		
		/**
		* Constante FILE_MP3 ( &#42;.mp3 ).
		*/
		public static const FILE_MP3:FileFilter = new FileFilter( "Audio MP3 ( *.mp3 )", "*.mp3" );
		
		/**
		* Constante FILE_MPC ( &#42;.mpc ).
		*/
		public static const FILE_MPC:FileFilter = new FileFilter( "Audio MPC ( *.mpc )", "*.mpc" );
		
		/**
		* Constante FILE_WAV ( &#42;.wav ).
		*/
		public static const FILE_WAV:FileFilter = new FileFilter( "Audio WAV ( *.wav )", "*.wav" );
		
		/**
		* Constante FILE_VQF ( &#42;.vqf ).
		*/
		public static const FILE_VQF:FileFilter = new FileFilter( "Audio VQF ( *.vqf )", "*.vqf" );
		
		/**
		* Constante FILE_WMA ( &#42;.wma ).
		*/
		public static const FILE_WMA:FileFilter = new FileFilter( "Audio WMA ( *.wma )", "*.wma" );
		
		/**
		* Constante FILE_AIFF ( &#42;.aif ).
		*/
		public static const FILE_AIFF:FileFilter = new FileFilter( "Audio AIFF ( *.aif )", "*.aif" );
		
		/**
		* Constante FILE_HTML ( &#42;.html; &#42;.htm ).
		*/
		public static const FILE_HTML:FileFilter = new FileFilter( "Documento HTML ( *.html; *.htm )", "*.html;*.htm" );
		
		/**
		* Constante FILE_XML ( &#42;.xml ).
		*/
		public static const FILE_XML:FileFilter = new FileFilter( "Documento XML ( *.xml )", "*.xml" );
		
		/**
		* Constante FILE_PDF ( &#42;.pdf ).
		*/
		public static const FILE_PDF:FileFilter = new FileFilter( "Documento Adobe PDF ( *.pdf )", "*.pdf" );
		
		/**
		* Constante FILE_TXT ( &#42;.txt ).
		*/
		public static const FILE_TXT:FileFilter = new FileFilter( "Documento de Texto ( *.txt )", "*.txt" );
		
		/**
		* Constante FILE_DOC ( &#42;.doc; &#42;.rtf ).
		*/
		public static const FILE_DOC:FileFilter = new FileFilter( "Documento Word ( *.doc; *.rtf )", "*.doc;*.rtf" );
		
		/**
		* Constante FILE_XLS ( &#42;.xls; &#42;csv ).
		*/
		public static const FILE_XLS:FileFilter = new FileFilter( "Documento Excel ( *.xls; *csv )", "*.xls;*csv" );
		
		/**
		* Constante FILE_PPT ( &#42;.ppt ).
		*/
		public static const FILE_PPT:FileFilter = new FileFilter( "Docuemnto Power Point ( *.ppt )", "*.ppt" );
		
		/**
		* Constante FILE_RAR ( &#42;.rar ).
		*/
		public static const FILE_RAR:FileFilter = new FileFilter( "Archivo RAR ( *.rar )", "*.rar" );
		
		/**
		* Constante FILE_ZIP ( &#42;.zip ).
		*/
		public static const FILE_ZIP:FileFilter = new FileFilter( "Archivo ZIP ( *.zip )", "*.zip" );
		
		/**
		* Constante FILE_SIT ( &#42;.sit ).
		*/
		public static const FILE_SIT:FileFilter = new FileFilter( "Archivo SIT ( *.sit )", "*.sit" );
		
		/**
		* Constante FILE_TAR ( &#42;.tar; &#42;.tar.gz; &#42;.tar.Z; &#42;.tgz  ).
		*/
		public static const FILE_TAR:FileFilter = new FileFilter( "Archivo TAR ( *.tar; *.tar.gz; *.tar.Z; *.tgz  )", "*.tar;*.tar.gz;*.tar.Z;*.tgz" ); 
		
		/**
		* Constante FILE_GZIP ( &#42;.gz; &#42;.gzip ).
		*/
		public static const FILE_GZIP:FileFilter = new FileFilter( "Archivo GZIP ( *.gz; *.gzip )", "*.gz;*.gzip" );
		
		/**
		* Constante FILE_SWF ( &#42;.swf ).
		*/
		public static const FILE_SWF:FileFilter = new FileFilter( "Peliculas Flash ( *.swf )", "*.swf" );
		
		
		
		/**
		* Constante ALL_IMAGE ( ALL_FILE, FILE_BMP, FILE_JPG, FILE_PNG, FILE_GIF ).
		* @see #ALL_FILE
		* @see #FILE_BMP
		* @see #FILE_JPG
		* @see #FILE_PNG
		* @see #FILE_GIF
		*/		
		public static const ALL_IMAGE:Array = new Array( ALL_FILE, FILE_BMP, FILE_JPG, FILE_PNG, FILE_GIF );
		
		/**
		* Constante ALL_VIDEO ( ALL_FILE, FILE_WMV, FILE_MOV, FILE_AVI, FILE_MPEG, FILE_FLV ).
		* @see #ALL_FILE
		* @see #FILE_WMV
		* @see #FILE_MOV
		* @see #FILE_AVI
		* @see #FILE_MPEG
		* @see #FILE_FLV
		*/
		public static const ALL_VIDEO:Array = new Array( ALL_FILE, FILE_WMV, FILE_MOV, FILE_AVI, FILE_MPEG, FILE_FLV );
		
		/**
		* Constante ALL_AUDIO ( ALL_FILE, FILE_MP3, FILE_MPC, FILE_WAV, FILE_VQF, FILE_WMA, FILE_AIFF ).
		* @see #ALL_FILE
		* @see #FILE_MP3
		* @see #FILE_MPC
		* @see #FILE_WAV
		* @see #FILE_VQF
		* @see #FILE_WMA
		* @see #FILE_AIFF
		*/
		public static const ALL_AUDIO:Array = new Array( ALL_FILE, FILE_MP3, FILE_MPC, FILE_WAV, FILE_VQF, FILE_WMA, FILE_AIFF );
		
		/**
		* Constante ALL_COMPRESS ( ALL_FILE, FILE_RAR, FILE_ZIP, FILE_SIT, FILE_TAR, FILE_GZIP ).
		* @see #ALL_FILE
		* @see #FILE_RAR
		* @see #FILE_ZIP
		* @see #FILE_SIT
		* @see #FILE_TAR
		* @see #FILE_GZIP
		*/
		public static const ALL_COMPRESS:Array = new Array( ALL_FILE, FILE_RAR, FILE_ZIP, FILE_SIT, FILE_TAR, FILE_GZIP );
		
		
		
		/**
		* Genera una lista con los valores pasados como parametro, los valore soportados son String y FileFilter.
		* @param	rest	Lista de valores.
		* @return	Array
		*/
		public static function GenerateList( ...rest ):Array {
			
			if( ! TypeUtil.isEmpty( rest ) ){
				
				var conTmp:Array = new Array( 
					FILE_JPG, 	FILE_GIF, 	FILE_PNG, 	FILE_BMP, 
					FILE_WMV, 	FILE_MOV, 	FILE_AVI, 	FILE_MPEG, 
					FILE_FLV, 	FILE_MP3, 	FILE_MPC, 	FILE_WAV, 
					FILE_VQF, 	FILE_WMA, 	FILE_AIFF, 	FILE_HTML, 
					FILE_XML, 	FILE_PDF, 	FILE_TXT, 	FILE_DOC, 
					FILE_XLS, 	FILE_PPT, 	FILE_RAR, 	FILE_ZIP, 
					FILE_SIT, 	FILE_TAR, 	FILE_GZIP, 	FILE_SWF 
				);	
				
				var arrTmp:Array = new Array();
				var argTmp:Array = ArgumentsUtil.Verify( rest );
				
				for( var a:int = 0; a < argTmp.length; a++ ){
					
					if( TypeUtil.isString( argTmp[ a ] ) ){
						
						VerifyConst: for( var b:int = 0; b < conTmp.length; b++ ){
							
							if( conTmp[ b ].extension.indexOf( argTmp[ a ] ) != -1 ){
								arrTmp.push( conTmp[ b ] );
								break VerifyConst;
							}
							
						}
						
					}else if( TypeUtil.thisIs( argTmp[ a ], FileFilter ) ){
						
						arrTmp.push( argTmp[ a ] );
						
					}					
					
				}
				
				return arrTmp;
				
			}
			
			return null;
			
		}		
		
	}
	
}
