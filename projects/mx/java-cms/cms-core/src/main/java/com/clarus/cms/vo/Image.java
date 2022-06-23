package com.clarus.cms.vo;

import java.io.Serializable;

import javax.swing.ImageIcon;

public class Image implements Serializable {
	private static final long serialVersionUID = 1L;
	private Boolean selected = Boolean.FALSE;
	private Integer preferedHeight;
	private byte[] value = new byte[0];
	private Integer width = 0;
	private Integer height = 0;

	public byte[] getValue() {
		return value;
	}

	public void setValue(byte[] value) {
		if( value == null || value.length == 0 ){
			this.value = new byte[0];
			width = 0;
			height = 0;
		}
		ImageIcon icon = new ImageIcon( value );
		width = icon.getIconWidth();
		height = icon.getIconHeight();
		this.value = value;
		
	}

	public int getWidth() {
		return width;
	}

	public void setWidth(int width) {
		this.width = width;
	}

	public int getHeight() {
		return height;
	}

	public void setHeight(int height) {
		this.height = height;
	}

	public void setHeight(Integer height) {
		this.height = height;
	}

	public Integer getPreferedHeight() {
		return preferedHeight;
	}

	public void setPreferedHeight(Integer preferedHeight) {
		this.preferedHeight = preferedHeight;
	}

	public void setWidth(Integer width) {
		this.width = width;
	}
	
	
	public Integer getScaledWidth(){
		if(   preferedHeight == null || width == null || height == null || height == 0 ){
			return 0;
		}
		return preferedHeight * width/height;
	}
	
	public Integer getScaledHeight(){
		if( preferedHeight == null ){
			return 0;
		}
		return preferedHeight; 
	}

	public Boolean getSelected() {
		return selected;
	}

	public void setSelected(Boolean selected) {
		this.selected = selected;
	}
}
