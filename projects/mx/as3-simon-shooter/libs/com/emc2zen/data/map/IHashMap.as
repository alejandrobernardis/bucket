
package com.emc2zen.data.map {

	/**
	* @import
	*/



	/**
	* Modelo de implementacion de un HASHMAP.
	* Autor: PollyJex
	*/
	public interface IHashMap {
		
		/**
		* Inserta un registro ( KEY > VALUE ).
		* @param	key		Identificador	
		* @param	value	Valor	
		* @return	void
		*/
		function put( key:String, value:* ):void;
        
		/**
		* Remueve un registro (KEY).
		* @param	key Identificador
		* @return	void
		*/
        function remove( key:String ):void;
		
		/**
		* Verifica si existe la clave.
		* @param	key 	Identificador
		* @return	void
		*/
        function containsKey( key:String ):Boolean;
		
		/**
		* Verifica si exite el valor.
		* @param	value 	Valor
		* @return	void
		*/
        function containsValue( value:* ):Boolean;
		
		/**
		* Retorna la clave asociada al valor.
		* @param	value	Valor
		* @return	String
		*/
        function getKey( value:* ):String;
		
		/**
		* Retorna el valor asociado a una clave.
		* @param	key 	Identificador
		* @return	*
		*/
        function getValue( key:String ):*;
		
		/**
		* Verifica el largo del registro.
		* @param	void
		* @return	int
		*/
        function size():int;
		
		/**
		* Verifica si el registro esta vacio.
		* @param	void
		* @return	Boolean
		*/
        function isEmpty():Boolean;
		
		/**
		* Reinicia el registro.
		* @param	void
		* @return	void
		*/
        function clear():void;
		
	}
	
}
