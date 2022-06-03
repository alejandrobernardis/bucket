package com.clarus.web.converter;

import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.convert.Converter;

public class UpperCaseConverter implements Converter {

	public Object getAsObject(FacesContext facesContext, UIComponent component, String stringValue) {
		if( stringValue == null ){
			return null;
		}
		return stringValue.toUpperCase().trim();
	}

	public String getAsString(FacesContext facesContext, UIComponent uiComponent, Object objectValue) {
		if( objectValue == null ){
			return null;
		}
		return objectValue.toString().toUpperCase().trim();
	}

}
