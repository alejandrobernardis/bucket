package com.clarus.web.form;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import org.richfaces.model.TreeNodeImpl;

import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.transport.Agent;

public class ContentForm implements Serializable {

	private static final long serialVersionUID = 8676212211972982986L;
	
	private TreeNodeImpl<Agent<ContentType>> contentTypeTree;
	private ContentType selectedContentType = new ContentType();
	private List<Agent<Content>> contentList;
	private Content selectedContent = new Content();
	private List<Animation> selectedContentAnimation = new ArrayList<Animation>();
	
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

	public List<Agent<Content>> getContentList() {
		return contentList;
	}

	public void setContentList(List<Agent<Content>> contentList) {
		this.contentList = contentList;
	}

	public Content getSelectedContent() {
		return selectedContent;
	}

	public void setSelectedContent(Content selectedContent) {
		this.selectedContent = selectedContent;
	}

	public List<Animation> getSelectedContentAnimation() {
		return selectedContentAnimation;
	}

	public void setSelectedContentAnimation(List<Animation> selectedContentAnimation) {
		this.selectedContentAnimation = selectedContentAnimation;
	}

	

}
