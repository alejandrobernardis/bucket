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

package com.emc2zen.util {

	/**
	* @import
	*/

	import com.emc2zen.core.CoreStatic;
	import com.emc2zen.data.map.HashMap;
	import com.emc2zen.util.StringUtil;
	import com.emc2zen.util.TypeUtil;
	import flash.utils.describeType;
	import flash.utils.getQualifiedClassName;
	import flash.utils.getQualifiedSuperclassName;

	/**
	* Utilidades para la verificacion de tipos de clases, metodos o propiedades.
	* @author	PollyJex
	*/
	public final class ClassUtil extends CoreStatic {
		
		/**
		* Resuelve el nombre de la clase.
		*/
		private static const RESOLVE_NAME:String = "NAME";
		
		/**
		* Resuelve el nombre del paquete, retorna null en caso de no poseer package.
		*/
		private static const RESOLVE_PACKAGE:String = "PACKAGE";
		
		/**
		* Resuelve el nombre absoluto de la clase reemplazando el calificador de nombres por el punto.
		*/
		private static const RESOLVE_PATH:String = "PATH";
		
		/**
		* Resuelve la constante.
		*/
		private static const RESOLVE_CONSTANT:String = "constant";
		
		/**
		* Resuelve la interfaz.
		*/
		private static const RESOLVE_INTERFACE:String = "implementsInterface";
		
		/**
		* Resuelve el metodo.
		*/
		private static const RESOLVE_METHOD:String = "method";
		
		/**
		* Resuelve la propiedad.
		*/
		private static const RESOLVE_PROPERTY:String = "accessor";
		
		/**
		* Resuelve la variable.
		*/
		private static const RESOLVE_VARIABLE:String = "variable";
		
		
		
		/**
		* Mapa de las clases que acceden al metodo createUniqueName.
		*/
		private static var $uniqueMap:HashMap = new HashMap();
		
		
		
		/**
		* Crea un nombre unico a partir del nombre de una clase agregandole al final un numero.
		* @param	value 	Instancia de una clase.
		* @return	String
		*/
		public static function createUniqueName( value:* ):String {
			
			if( TypeUtil.isNull( value ) || TypeUtil.isUndefined( value ) ){
				return null;
			}
			
			var intTmp:int = 0;
			var strTmp:String = shortName( value );
			var strChr:int = strTmp.charCodeAt( strTmp.length - 1 );
			
			if( $uniqueMap.containsKey( strTmp ) ){	
				intTmp = $uniqueMap.getValue( strTmp );
				intTmp ++;
			}			
			
			$uniqueMap.put( strTmp, intTmp );
			
			if( strChr >= 48 && strChr <= 57 ){
				strTmp += "_";
			}
			
			return strTmp + intTmp;			
			
		}
		
		/**
		* Retorna el nombre de la clase.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function shortName( value:* ):String {
			
			return ResolveFormat( value, RESOLVE_NAME );
			
		}
		
		/**
		* Retorna el nombre completo de la clase.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function fullName( value:* ):String {
			
			return getQualifiedClassName( value );
			
		}
		
		/**
		* Retorna el package de la clase, retorna null en caso de no poseer package.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function packageName( value:* ):String {
			
			return ResolveFormat( value, RESOLVE_PACKAGE );
			
		}
		
		/**
		* Retorna el path de la clase, reemplazando el calificador de nombres por el punto.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function pathName( value:* ):String {
			
			return ResolveFormat( value, RESOLVE_PATH );
			
		}		
		
		/**
		* Retorna el nombre de la super clase.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function superShortName( value:* ):String {
			
			return ResolveFormat( value, RESOLVE_NAME, true );
			
		}
		
		/**
		* Retorna el nombre completo de la super clase.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function superFullName( value:* ):String {
			
			return getQualifiedSuperclassName( value );
			
		}
		
		/**
		* Retorna el package de la super clase, retorna null en caso de no poseer package.
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function superPackageName( value:* ):String {
			
			return ResolveFormat( value, RESOLVE_PACKAGE, true );
			
		}
		
		/**
		* Retorna el path de la super clase, reemplazando el calificador de nombres por el punto. 
		* @param	value		Instancia de la clase.
		* @return	String
		*/
		public static function superPathName( value:* ):String {
			
			return ResolveFormat( value, RESOLVE_PATH, true );
			
		}	
		
		
		
		/**
		* Verifica si clase es dinamica.
		* @param	value	Referencia a la clase.
		* @return	Boolean
		*/
		public static function isDynamic( value:* ):Boolean {
			
			return TypeUtil.isBoolean( describeType( value ).@isDynamic.toString() );
			
		}
		
		/**
		* Verifica si clase es final.
		* @param	value	Referencia a la clase.
		* @return	Boolean	
		*/
		public static function isFinal( value:* ):Boolean {
			
			return TypeUtil.isBoolean( describeType( value ).@isFinal.toString() );
			
		}
		
		/**
		* Verifica si clase es estatica.
		* @param	value	Referencia a la clase.
		* @return	Boolean
		*/
		public static function isStatic( value:* ):Boolean {
			
			return TypeUtil.isBoolean( describeType( value ).@isStatic.toString() );
			
		}
		
		
		
		/**
		* Verifica si la clase implementa la constante.
		* @param	source		Referencia de la clase.
		* @param	value		Nombre de la constante.
		* @return	Boolean
		*/
		public static function isConstant( source:*, value:String ):Boolean {
			
			return ResolveThisIs( source, value, RESOLVE_CONSTANT );
			
		}
		
		/**
		* Verifica si la clase implementa la interfaz.
		* @param	source		Referencia de la clase.
		* @return	Boolean
		*/
		public static function isInterface( source:* ):Boolean {
			
			return ResolveThisIs( source, null, RESOLVE_INTERFACE );
			
		}
		
		/**
		* Verifica si la clase implementa el metodo. 
		* @param	source		Referencia de la clase.
		* @param	value		Nombre del metodo.
		* @return	Boolean	
		*/
		public static function isMethod( source:*, value:String ):Boolean {
			
			return ResolveThisIs( source, value, RESOLVE_METHOD );
			
		}
		
		/**
		* Verifica si la clase implementa la propiedad.
		* @param	source		Referencia de la clase.
		* @param	value		Nombre de la propiedad.
		* @return	Boolean
		*/
		public static function isProperty( source:*, value:String ):Boolean {
			
			return ResolveThisIs( source, value, RESOLVE_PROPERTY );
			
		}
		
		/**
		* Verifica si la clase implementa la variable.
		* @param	source		Referencia de la clase.
		* @param	value		Nombre de la variable.
		* @return	Boolean
		*/
		public static function isVariable( source:*, value:String ):Boolean {
			
			return isImplementedVariable( source, value );
			
		}
		
		
		
		/**
		* Verifica si la clase implementa un metodo de otra clase.
		* @param	source			Clase.
		* @param	interfaz		Interfaz.
		* @return	Boolean
		*/
		public static function isImplementedInterface( source:*, interfaz:String ):Boolean {
			
			return ResolveImplemented( source, interfaz, null, RESOLVE_INTERFACE );
			
		}
		
		/**
		* Verifica si la clase implementa una constante de otra clase.
		* @param	subclass		Clase.
		* @param	superclass		Clase a evaluar.
		* @param	value			Constante a evaluar.
		* @return	Boolean
		*/
		public static function isImplementedConstant( subclass:*, superclass:String, value:String ):Boolean {
			
			return ResolveImplemented( subclass, superclass, value, RESOLVE_CONSTANT );
			
		}
		
		/**
		* Verifica si la clase implementa un metodo de otra clase.
		* @param	subclass		Clase.
		* @param	superclass		Clase a evaluar.
		* @param	value			Metodo a evaluar.
		* @return	Boolean
		*/
		public static function isImplementedMethod( subclass:*, superclass:String, value:String ):Boolean {
			
			return ResolveImplemented( subclass, superclass, value, RESOLVE_METHOD );
			
		}
		
		/**
		* Verifica si la clase implementa una propiedad de otra clase.
		* @param	subclass		Clase.
		* @param	superclass		Clase a evaluar.
		* @param	value			Propiedad a evaluar.
		* @return	Boolean
		*/
		public static function isImplementedProperty( subclass:*, superclass:String, value:String ):Boolean {
			
			return ResolveImplemented( subclass, superclass, value, RESOLVE_PROPERTY );
			
		}
		
		/**
		* Verifica si la clase implementa la variable.
		* @param	subclass		Clase.
		* @param	value			Variable a evaluar.
		* @return	Boolean
		*/
		public static function isImplementedVariable( source:*, value:String ):Boolean {
			
			return ResolveImplemented( source, null, value, RESOLVE_VARIABLE );
			
		}
		
		
		
		/**
		* Resuelve la busqueda de la constante, metodo o propiedad a verificar.
		* @param	source		Referencia de la clase.
		* @param	value		Valor a buscar.
		* @param	property	Tipo de la propiedad.
		* @return	Boolean
		*/
		private static function ResolveThisIs( source:*, value:String, property:String ):Boolean {
			
			if( property == RESOLVE_INTERFACE ){
				return ( describeType( source ).factory[0].extendsClass.length() == 0 ) ? true : false;					
			}		
			
			var xmlTmp:XMLList = ResolveCaptureNode( source, property );
			
			return ! TypeUtil.isEmpty( xmlTmp.( @name == value ).@name.toString() );
			
		}
		
		/**
		* Resuelve la captura del nodo.
		* @param	source		Clase.
		* @param	property	Propiedad.
		* @return	XMLList
		*/
		private static function ResolveCaptureNode( source:*, property:String ):XMLList {
			
			var desTmp:XML = describeType( source );
			
			switch( property ){
				
				case RESOLVE_CONSTANT:
					return desTmp..constant;
					break;
					
				case RESOLVE_METHOD:
					return desTmp..method;
					break;
					
				case RESOLVE_PROPERTY:
					return desTmp..accessor;
					break;
					
				case RESOLVE_INTERFACE:
					return desTmp..implementsInterface;
					break;
					
				case RESOLVE_VARIABLE:
					return desTmp..variable;
					break;
					
				default:
					return null;
					
			}	
			
		}
		
		/**
		* Rseuelve la verificacion en la implementacion de metodo y propiedades de otras clases.
		* @param	subclass		Clase.
		* @param	superclass		Clase a evaluar.
		* @param	value			Valor a evaluar.	
		* @param	property		Propiedad a evaluar. 
		* @return	
		*/
		private static function ResolveImplemented( subclass:*, superclass:String, value:String, property:String ):Boolean {
			
			var metTmp:String = new String();	
			var xmlTmp:XMLList = ResolveCaptureNode( subclass, property );
			
			if( property == RESOLVE_VARIABLE ){
				
				metTmp = xmlTmp.( @name == value ).@name.toString();
				return ! TypeUtil.isEmpty( metTmp );
				
			}else if( property == RESOLVE_INTERFACE ){
				metTmp = xmlTmp.( @type == superclass ).@type;
			}else if( property == RESOLVE_CONSTANT ){
				metTmp = xmlTmp.( @name == value ).@type;
			}else{
				metTmp = xmlTmp.( @name == value ).@declaredBy;
			}
			
			metTmp = ResolveFormat( metTmp, RESOLVE_PATH );
			superclass = ResolveFormat( superclass, RESOLVE_PATH );
			
			return new Boolean( metTmp == superclass );
			
		}
		
		/**
		* Resuelve el formato elegido.
		* @param	value		Valor a evaluar.
		* @param	resolve		Tipo de evaluacion.
		* @param	type		Tipo de clase.
		* @return	String
		*/
		private static function ResolveFormat( value:*, resolve:String, type:Boolean = false ):String {
			
			var strTmp:String = new String();
			var resTmp:String = new String();
			
			if( !TypeUtil.isString( value ) ){
				if( !type ){
					resTmp = fullName( value );
				}else{
					resTmp = superFullName( value );
				}
			}else{
				resTmp = value;
			}
			
			switch( resolve ){
				
				case RESOLVE_NAME:					
					strTmp = StringUtil.remove( resTmp, "[A-Za-z0-9\.]+\:\:" );
					break;
					
				case RESOLVE_PACKAGE:
					if( resTmp.indexOf("::") != -1 ){
						strTmp = StringUtil.remove( resTmp, "\:\:[A-Za-z0-9]+" );
					}else{
						strTmp = null;
					}					
					break;
					
				case RESOLVE_PATH:
					strTmp = StringUtil.replace( resTmp, "\:\:", "." );
					break;
				
			}
			
			return strTmp;
			
		}
		
	}
	
}
