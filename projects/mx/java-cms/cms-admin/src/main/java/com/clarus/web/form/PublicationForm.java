package com.clarus.web.form;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import org.richfaces.model.TreeNodeImpl;

import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.transport.Agent;

public class PublicationForm implements Serializable{

	private static final long serialVersionUID = 1L;
	private List<Agent<Publication>> publicationList;
	private TreeNodeImpl<Agent<ContentType>> contentTypeTree;
	private ContentType selectedContentType = new ContentType();
	
	
	private Publication selectedPublication = new Publication();
	private List<PublicationPage> pages = new ArrayList<PublicationPage>();

	public TreeNodeImpl<Agent<ContentType>> getContentTypeTree() {
		return contentTypeTree;
	}
	public void setContentTypeTree(TreeNodeImpl<Agent<ContentType>> contentTypeTree) {
		this.contentTypeTree = contentTypeTree;
	}
	public ContentType getSelectedContentType() {
		return selectedContentType;
	}
	public void setSelectedContentType(ContentType selectedContentType) {
		this.selectedContentType = selectedContentType;
	}
	public List<Agent<Publication>> getPublicationList() {
		return publicationList;
	}
	public Publication getSelectedPublication() {
		return selectedPublication;
	}
	public void setPublicationList(List<Agent<Publication>> publicationList) {
		this.publicationList = publicationList;
	}
	public void setSelectedPublication(Publication selectedPublication) {
		this.selectedPublication = selectedPublication;
	}
	public List<PublicationPage> getPages() {
		return pages;
	}
	public void setPages(List<PublicationPage> pages) {
		this.pages = pages;
	}

	
	public Integer getNumPages(){
		if( pages == null ){
			return 0;
		}
		return pages.size();
	}
	
	
	
}
