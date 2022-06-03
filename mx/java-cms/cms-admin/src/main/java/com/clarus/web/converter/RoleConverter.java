package com.clarus.web.converter;

import javax.faces.application.FacesMessage;
import javax.faces.component.UIComponent;
import javax.faces.context.FacesContext;
import javax.faces.convert.Converter;
import javax.faces.convert.ConverterException;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.clarus.cms.model.catalog.Role;
import com.clarus.web.util.Util;

public class RoleConverter implements Converter {
	protected Log log = LogFactory.getLog(getClass()); 
	public Object getAsObject(FacesContext facesContext, UIComponent component, String stringValue) {
		try{
			return Role.valueOf(stringValue);
		}catch (Exception e) {
			FacesMessage message = new FacesMessage( Util.loadErrorMessage( "labels.labels", "roleConversionError"));
			throw new ConverterException( message );
		}
	}

	public String getAsString(FacesContext facesContext, UIComponent uiComponent, Object objectValue) {
		if (objectValue == null) {
			return null;
		}
		return ((Role)objectValue).name();
	}

}
