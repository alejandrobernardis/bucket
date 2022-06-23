package com.clarus.web.converter;

import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.convert.Converter;

public class TrimConverter implements Converter {

	public Object getAsObject(FacesContext facesContext, UIComponent component, String stringValue) {
		if (stringValue == null) {
			return null;
		}
		return stringValue.trim();
	}

	public String getAsString(FacesContext facesContext,
			UIComponent uiComponent, Object objectValue) {
		if (objectValue == null) {
			return null;
		}
		return objectValue.toString().trim();
	}

}
