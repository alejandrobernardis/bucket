package com.clarus.cms.web.util;

import java.util.Map;
import java.util.ResourceBundle;

import javax.faces.application.FacesMessage;
import javax.faces.component.UIComponent;
import javax.faces.context.ExternalContext;
import javax.faces.context.FacesContext;
import javax.servlet.http.HttpServletRequest;

public class Util {

	public static HttpServletRequest getRequest() {
		FacesContext context = FacesContext.getCurrentInstance();
		ExternalContext extContext = context.getExternalContext();
		return (HttpServletRequest) extContext.getRequest();
	}

	public static String getRequestParameter(String param) {
		FacesContext context = FacesContext.getCurrentInstance();
		ExternalContext extContext = context.getExternalContext();
		Map<String, String> params = extContext.getRequestParameterMap();
		return params.get(param);
	}

	public static String loadErrorMessage( String basename, String key ) {
		FacesContext context = FacesContext.getCurrentInstance();
		ResourceBundle bundle;
		try {
			bundle = ResourceBundle.getBundle(basename, context
					.getViewRoot().getLocale());
		} catch (Exception e) {
			return null;
		}
		return bundle.getString(key);
	}
	
	public static void addFacesMessage( UIComponent comp, String baseName, String key ){
		FacesContext context = FacesContext.getCurrentInstance();
		addFacesMessage(comp.getClientId(context), baseName, key );
	}

	public static void addFacesMessage( String clientId, String baseName, String key ){
		FacesContext context = FacesContext.getCurrentInstance();
		FacesMessage message = new FacesMessage( loadErrorMessage( baseName, key));
		message.setSeverity(FacesMessage.SEVERITY_ERROR);
		context.addMessage(clientId , message);
	}
	
}
