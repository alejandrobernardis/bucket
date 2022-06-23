package com.clarus.web.util;

import java.util.Iterator;
import java.util.Map;
import java.util.ResourceBundle;

import javax.faces.application.FacesMessage;
import javax.faces.component.UIComponent;
import javax.faces.component.UIViewRoot;
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

	public static void addFacesMessageForId( String id, String baseName, String key ){
		String compid = getClientId(id);
		addFacesMessage( compid, baseName, key );
	}
	
	public static void addFacesMessage( String clientId, String baseName, String key ){
		FacesContext context = FacesContext.getCurrentInstance();
		FacesMessage message = new FacesMessage( loadErrorMessage( baseName, key));
		message.setSeverity(FacesMessage.SEVERITY_ERROR);
		context.addMessage(clientId , message);
	}
	
	
	public static String getClientId(String componentId) {
	    FacesContext context = FacesContext.getCurrentInstance();
	    UIViewRoot root = context.getViewRoot();
	    UIComponent c = findComponent(root, componentId);
	    return c.getClientId(context);
	 }

	
	private static UIComponent findComponent(UIComponent c, String id) {
	    if (id.equals(c.getId())) {
	      return c;
	    }
	    Iterator<UIComponent> kids = c.getFacetsAndChildren();
	    while (kids.hasNext()) {
	      UIComponent found = findComponent(kids.next(), id);
	      if (found != null) {
	        return found;
	      }
	    }
	    return null;
	}
	
	
	
}
