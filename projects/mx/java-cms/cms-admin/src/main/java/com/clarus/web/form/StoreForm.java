package com.clarus.web.form;

import java.io.Serializable;
import java.util.List;

import org.richfaces.model.TreeNodeImpl;

import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.Store;
import com.clarus.transport.Agent;

public class StoreForm implements Serializable{

	private static final long serialVersionUID = 1L;
	private List<Agent<Store>> storeList;
	private TreeNodeImpl<Agent<ContentType>> contentTypeTree;
	private ContentType selectedContentType = new ContentType();
	private Store selectedStore = new Store();

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
	public List<Agent<Store>> getStoreList() {
		return storeList;
	}
	public void setStoreList(List<Agent<Store>> storeList) {
		this.storeList = storeList;
	}
	public Store getSelectedStore() {
		return selectedStore;
	}
	public void setSelectedStore(Store selectedStore) {
		this.selectedStore = selectedStore;
	}
	
	
	
	
	
}
