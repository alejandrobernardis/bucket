package com.clarus.cms.vo;

import java.io.Serializable;

public class Config implements Serializable {

	private static final long serialVersionUID = 1L;
	private Integer width;
	private Integer height;
	private String locale;
	private Template templateFolder;
	
	public Integer getWidth() {
		return width;
	}
	public void setWidth(Integer width) {
		this.width = width;
	}
	public Integer getHeight() {
		return height;
	}
	public void setHeight(Integer height) {
		Template[] templates = Template.values();
		for( int i = 0 ; i < templates.length; i++ ){
			templateFolder = templates[i];
			if( height.intValue() >= templateFolder.getHeight().intValue() ){
				break;
			}
		}
		this.height = height;
	}
	public String getLocale() {
		return locale;
	}
	public void setLocale(String locale) {
		this.locale = locale;
	}
	
	public Long getDummy(){
		return Math.round(Math.random() + 1000000000 );
	}
	
	public void setDummy( Long dummy ){
		
	}
	public Template getTemplateFolder() {
		return templateFolder;
	}
	public void setTemplateFolder(Template templateFolder) {
		this.templateFolder = templateFolder;
	}
}
