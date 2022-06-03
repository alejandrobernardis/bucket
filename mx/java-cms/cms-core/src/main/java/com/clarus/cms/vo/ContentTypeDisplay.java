package com.clarus.cms.vo;

import java.io.Serializable;

public class ContentTypeDisplay implements Serializable {
	private static final long serialVersionUID = 1L;
	
	private Integer idContentType;
	private Integer idContentTypeParent;
	private String contentTypeLabel;
	private Integer childNum;
	private Integer displayOrder;
	
	
	public String getContentTypeLabel() {
		return contentTypeLabel;
	}
	public void setContentTypeLabel(String contentTypeLabel) {
		this.contentTypeLabel = contentTypeLabel;
	}
	public Integer getChildNum() {
		return childNum;
	}
	public void setChildNum(Integer childNum) {
		this.childNum = childNum;
	}
	public Integer getIdContentType() {
		return idContentType;
	}
	public Integer getIdContentTypeParent() {
		return idContentTypeParent;
	}
	public void setIdContentType(Integer idContentType) {
		this.idContentType = idContentType;
	}
	public void setIdContentTypeParent(Integer idContentTypeParent) {
		this.idContentTypeParent = idContentTypeParent;
	}
	public Integer getDisplayOrder() {
		return displayOrder;
	}
	public void setDisplayOrder(Integer displayOrder) {
		this.displayOrder = displayOrder;
	}


}
