package com.clarus.cms.vo;

import java.io.Serializable;

public class FlashAnimation implements Serializable {
	private static final long serialVersionUID = 1L;
	private Integer preferedHeight;
	private Integer preferedWidth;
	private byte[] value = new byte[0];

	public byte[] getValue() {
		return value;
	}

	public void setValue(byte[] value) {
		this.value = value;
		if( value == null || value.length == 0 ){
			this.value = new byte[0];
		}
		
		
	}

	public Integer getPreferedHeight() {
		return preferedHeight;
	}

	public void setPreferedHeight(Integer preferedHeight) {
		this.preferedHeight = preferedHeight;
	}

	public Integer getPreferedWidth() {
		return preferedWidth;
	}

	public void setPreferedWidth(Integer preferedWidth) {
		this.preferedWidth = preferedWidth;
	}


}
