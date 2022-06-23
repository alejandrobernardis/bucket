package com.clarus.cms.vo;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

public class TreeNodeContentTypeDisplay implements Serializable{
	private static final long serialVersionUID = -2763994539158181388L;
	private ContentTypeDisplay contentTypeDisplay;
	private List<ContentTypeDisplay> children = new ArrayList<ContentTypeDisplay>();
	
	public TreeNodeContentTypeDisplay(){
		
	}
	
	public TreeNodeContentTypeDisplay(ContentTypeDisplay contentTypeDisplay){
		this.contentTypeDisplay = contentTypeDisplay;
	}
	
	public TreeNodeContentTypeDisplay(ContentTypeDisplay contentTypeDisplay, List<ContentTypeDisplay> children){
		this.contentTypeDisplay = contentTypeDisplay;
		this.children = children;
	}
	
	
	public List<ContentTypeDisplay> getChildren() {
		return children;
	}
	public void setChildren(List<ContentTypeDisplay> children) {
		this.children = children;
	}

	public ContentTypeDisplay getContentTypeDisplay() {
		return contentTypeDisplay;
	}

	public void setContentTypeDisplay(ContentTypeDisplay contentTypeDisplay) {
		this.contentTypeDisplay = contentTypeDisplay;
	}
	
	
	
}
