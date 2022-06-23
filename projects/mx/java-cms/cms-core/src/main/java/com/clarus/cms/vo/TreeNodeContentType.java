package com.clarus.cms.vo;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import com.clarus.cms.vo.model.ContentType;

public class TreeNodeContentType implements Serializable{
	private static final long serialVersionUID = -2763994539158181388L;
	private ContentType contentType;
	private List<ContentType> children = new ArrayList<ContentType>();
	
	public TreeNodeContentType(){
		
	}
	
	public TreeNodeContentType(ContentType contentType){
		this.contentType = contentType;
	}
	
	public TreeNodeContentType(ContentType contentType, List<ContentType> children){
		this.contentType = contentType;
		this.children = children;
	}
	
	public ContentType getContentType() {
		return contentType;
	}
	public void setContentType(ContentType contentType) {
		this.contentType = contentType;
	}
	public List<ContentType> getChildren() {
		return children;
	}
	public void setChildren(List<ContentType> children) {
		this.children = children;
	}
	
	
	
}
