package com.clarus.cms.model.catalog;

public enum Language {
	ES("Español"),
	EN("English");
	
	private Language( String label ){
		this.label = label;
	}
	
	private String label;

	public String getLabel() {
		return label;
	}

	public void setLabel(String label) {
		this.label = label;
	}

	public String getValue(){
		return this.toString();
	}
	
	public void setValue( String value ){
		
	}
}
