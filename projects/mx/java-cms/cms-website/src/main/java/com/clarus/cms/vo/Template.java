package com.clarus.cms.vo;

public enum Template {
	TMPL_1280x124(1280,1024,"/web-resources/media1024"),
	TMPL_1152x864(1152,864,"/web-resources/media864"),
	TMPL_1024x768(1024,768,"/web-resources/media768"),
	TMPL_800x600(800,600,"/web-resources/media600");
	
	private Integer width;
	private Integer height;
	private String mediaFolder;
	
	private Template( Integer width, Integer height, String mediaFolder ){
		this.width = width;
		this.height = height;
		this.mediaFolder = mediaFolder;
	}

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
		this.height = height;
	}

	public String getMediaFolder() {
		return mediaFolder;
	}

	public void setMediaFolder(String mediaFolder) {
		this.mediaFolder = mediaFolder;
	}

	
	
	
}
