package com.clarus.cms.model.catalog;

public enum AcceptedFileExtension {
	JPG("image/jpeg", AnimationType.SLIDESHOW),
	PNG("image/png", AnimationType.SLIDESHOW),
	GIF("image/gif", AnimationType.SLIDESHOW),
	SWF("application/x-shockwave-flash", AnimationType.FLASH);
	
	private String mimeType;
	private AnimationType type;
	
	private AcceptedFileExtension(String mimeType, AnimationType type) {
		this.mimeType = mimeType;
		this.type = type; 
	}
	
	public String getMimeType(){
		return this.mimeType;
	}
	
	public AnimationType getType(){
		return this.type;
	}
	
}
