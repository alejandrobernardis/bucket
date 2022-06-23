package com.clarus.web.form;

import java.io.Serializable;
import java.util.List;

import javax.faces.model.SelectItem;

import org.richfaces.model.TreeNodeImpl;

import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.ContentTypeLabel;
import com.clarus.transport.Agent;

public class CategoryForm implements Serializable {

	private static final long serialVersionUID = 8676212211972982986L;
	
	private TreeNodeImpl<Agent<ContentType>> contentTypeTree;
	private ContentType selectedContentType = new ContentType();
	private Boolean showEdit = Boolean.FALSE;
	private List<SelectItem> parentCategories;
	private List<ContentTypeLabel> labels; 
	
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

	public Boolean getShowEdit() {
		return showEdit;
	}

	public void setShowEdit(Boolean showEdit) {
		this.showEdit = showEdit;
	}

	public List<SelectItem> getParentCategories() {
		return parentCategories;
	}

	public void setParentCategories(List<SelectItem> parentCategories) {
		this.parentCategories = parentCategories;
	}

	public List<ContentTypeLabel> getLabels() {
		return labels;
	}

	public void setLabels(List<ContentTypeLabel> labels) {
		this.labels = labels;
	}
	

}
