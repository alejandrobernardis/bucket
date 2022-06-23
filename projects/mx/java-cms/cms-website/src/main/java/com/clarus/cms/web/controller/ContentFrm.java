package com.clarus.cms.web.controller;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import com.clarus.cms.vo.TreeNodeContentTypeDisplay;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.vo.model.Store;

public class ContentFrm implements Serializable{

	private static final long serialVersionUID = 1L;
	private Content content;
	private List<TreeNodeContentTypeDisplay> menu;
	private List<Animation> listAnimation = new ArrayList<Animation>();
	private List<Publication> listPublication = null;
	private Integer contentType;
	private List<PublicationPage> pages;
	private List<Store> stores;
	private Integer publication;
	
	
	public Content getContent() {
		return content;
	}

	public void setContent(Content content) {
		this.content = content;
	}

	public List<TreeNodeContentTypeDisplay> getMenu() {
		return menu;
	}

	public void setMenu(List<TreeNodeContentTypeDisplay> menu) {
		this.menu = menu;
	}

	public List<Animation> getListAnimation() {
		return listAnimation;
	}

	public void setListAnimation(List<Animation> listAnimation) {
		this.listAnimation = listAnimation;
	}

	public Integer getContentType() {
		return contentType;
	}

	public void setContentType(Integer contentType) {
		this.contentType = contentType;
	}

	public List<Publication> getListPublication() {
		return listPublication;
	}

	public void setListPublication(List<Publication> listPublication) {
		this.listPublication = listPublication;
	}

	public List<PublicationPage> getPages() {
		return pages;
	}

	public void setPages(List<PublicationPage> pages) {
		this.pages = pages;
	}

	public Integer getPublication() {
		return publication;
	}

	public void setPublication(Integer publication) {
		this.publication = publication;
	}

	public List<Store> getStores() {
		return stores;
	}

	public void setStores(List<Store> stores) {
		this.stores = stores;
	}
	
}
