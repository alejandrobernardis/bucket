package com.clarus.web.controller;

import java.util.Date;

import org.apache.commons.lang.StringUtils;

import com.clarus.web.util.Util;

public class UtilController {

	private String locale = "es";
	
	
	
	public Long getDummy(){
		return Math.round( Math.random()*100000.0 );
	}
	
	public void setDummy( Long dummy ){
		
	}

	public String getLocale() {
		return locale;
	}

	public void setLocale(String locale) {
		this.locale = locale;
	}
	
	
	public String selectLocale(){
		String selectedLocale = Util.getRequestParameter( "LANG" );
		if( StringUtils.isNotEmpty( selectedLocale )  ){
			locale = selectedLocale;
		}
		return "";
	}
	
	public Date getToday(){
		return new Date();
	}
	
	public void setToday(){
	}
	
	
	
}
