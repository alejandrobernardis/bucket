package com.clarus.web.controller;

import java.util.ArrayList;
import java.util.List;

import javax.faces.model.SelectItem;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.richfaces.component.UITree;
import org.richfaces.component.html.HtmlTree;
import org.richfaces.event.NodeSelectedEvent;
import org.richfaces.model.TreeNodeImpl;

import com.clarus.cms.model.catalog.Language;
import com.clarus.cms.vo.TreeNodeContentType;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.ContentTypeLabel;
import com.clarus.cms.vo.model.ContentTypeLabelId;
import com.clarus.cms.ws.ContentService;
import com.clarus.transport.Agent;
import com.clarus.web.form.CategoryForm;
import com.clarus.web.util.Util;

public class CategoryController {

	protected Log log = LogFactory.getLog(getClass()); 
	private ContentService contentService;
	private CategoryForm categoryForm;
	private String message;
	private String messageList;
	private Boolean error;
	 

	public String listCategory() {

		List<TreeNodeContentType> nodes = null;
		try{
			nodes = contentService.findContentTypeTree();
		}catch (Exception e) {
			log.error( "Error al obtener los cotentTypes",e );
		}
		
		categoryForm.setParentCategories(new ArrayList<SelectItem>());
		
		TreeNodeImpl<Agent<ContentType>> root = new TreeNodeImpl<Agent<ContentType>>();
		root.setData(new Agent<ContentType>(new ContentType(),"Root"));
		if( nodes != null ){
			for (TreeNodeContentType node : nodes) {
				
				SelectItem item = new SelectItem( node.getContentType().getIdContentType(),node.getContentType().getContentTypeName() );
				categoryForm.getParentCategories().add(item);
				
				TreeNodeImpl<Agent<ContentType>> treeNode = new TreeNodeImpl<Agent<ContentType>>();
				treeNode.setData(new Agent<ContentType>(node.getContentType(),node.getContentType().getActive() ? "Parent" : "Inactive"));
				
	
				for (ContentType child : node.getChildren()) {
					TreeNodeImpl<Agent<ContentType>> treeNodeChild = new TreeNodeImpl<Agent<ContentType>>();
					treeNodeChild.setData(new Agent<ContentType>(child, child.getActive() ? "Child" : "Inactive"));
					treeNode.addChild(treeNodeChild.getData().getValue().getContentTypeName(), treeNodeChild);
				}
				root.addChild(treeNode.getData().getValue().getContentTypeName(), treeNode);
	
			}
		}
		
		
		TreeNodeImpl<Agent<ContentType>> base = new TreeNodeImpl<Agent<ContentType>>();
		base.addChild("Root", root);
		
		categoryForm.setContentTypeTree(base);
		
		/*categoryForm.setNameComponent(null);
		categoryForm.setSelectedContentType(new ContentType());
		cleanLabels();*/
        categoryForm.setShowEdit(Boolean.FALSE);
		return "CategoryController:listCategory";
	}
	
	
	 @SuppressWarnings("unchecked")
	public void processSelection(NodeSelectedEvent event) {
        HtmlTree tree = (HtmlTree) event.getComponent();
        Agent<ContentType> agent = (Agent<ContentType>) tree.getRowData();
        categoryForm.setSelectedContentType(agent.getValue());
        
        List<ContentTypeLabel> labels = null;
        try{
        	labels = contentService.findContentTypeLabelsForContent( agent.getValue().getIdContentType() );
        }catch (Exception e) {
			log.error("Error al obtener las etiquetas del contentype " + agent.getValue().getIdContentType(), e);
			labels = new ArrayList<ContentTypeLabel>();
		}
        categoryForm.setLabels(labels);

        categoryForm.setShowEdit(Boolean.TRUE);
    }
	
	public void cancelEdit(){
		categoryForm.setSelectedContentType(new ContentType());
		cleanLabels();
        categoryForm.setShowEdit(Boolean.FALSE);
	}

	
	 private void cleanLabels(){
		 List<ContentTypeLabel> labels = new ArrayList<ContentTypeLabel>();
			for( Language allowedLang :  Language.values()){
				ContentTypeLabel label = new ContentTypeLabel();
				ContentTypeLabelId id = new ContentTypeLabelId( );
				id.setLanguage(allowedLang);
				id.setIdContentType(null);
				label.setId(id);
				labels.add(label );
			}
			categoryForm.setLabels(labels);
	 }
	
	
	public void addCategory() {
		categoryForm.setSelectedContentType(new ContentType());
		cleanLabels();
		categoryForm.setShowEdit(Boolean.TRUE);
	}

	
	public void deleteCategories() {
		if(categoryForm.getSelectedContentType().getIdContentType() != null){
			try{
				if( contentService.hasContents( categoryForm.getSelectedContentType().getIdContentType() ) ){
					messageList = Util.loadErrorMessage("labels.labels", "hasContents");
					return;
				}
				
				for( ContentTypeLabel label : categoryForm.getLabels() ){
					contentService.deleteContentTypeLabel(label);
				}
				contentService.deleteContentType(categoryForm.getSelectedContentType());
				listCategory();
				categoryForm.setShowEdit(Boolean.FALSE);
			}catch (Exception e) {
				log.error("Error al guardar los contenttypes",e);
				messageList = Util.loadErrorMessage("labels.labels", "errorOccured");
			}
		}
	}

	public void saveCategory(){
		try{
			ContentType ctExists  = contentService.findContentTypeByName(categoryForm.getSelectedContentType().getContentTypeName());
			if( ctExists != null && !ctExists.getIdContentType().equals(categoryForm.getSelectedContentType().getIdContentType()) ){
				Util.addFacesMessageForId("ctName", "labels.labels", "nameExists" );
				return;
			}
	
			ContentType savedContentType = contentService.saveOrUpdateContentType(categoryForm.getSelectedContentType());
			for( ContentTypeLabel label : categoryForm.getLabels() ){
				label.getId().setIdContentType(savedContentType.getIdContentType());
				ContentTypeLabel savedLabel = contentService.saveContentTypeLabel(label);
				label.init(savedLabel);
			}
			
			listCategory();
		
			error = Boolean.FALSE;
			message = Util.loadErrorMessage("labels.labels", "saveSuccesful");
			
			categoryForm.setSelectedContentType(savedContentType);
			categoryForm.setShowEdit(Boolean.TRUE);
		}catch (Exception e) {
			log.error("Error al guardar el contenttype", e);
			error = Boolean.TRUE;
			message = Util.loadErrorMessage("labels.labels", "saveError");
		}
	}
	
	public ContentService getContentService() {
		return contentService;
	}

	public void setContentService(ContentService contentService) {
		this.contentService = contentService;
	}

	public CategoryForm getCategoryForm() {
		return categoryForm;
	}

	public void setCategoryForm(CategoryForm categoryForm) {
		this.categoryForm = categoryForm;
	}
	
	public Boolean nodeOpened(UITree tree){
		return Boolean.TRUE;
	}


	public String getMessage() {
		return message;
	}


	public void setMessage(String message) {
		this.message = message;
	}


	public Boolean getError() {
		return error;
	}


	public void setError(Boolean error) {
		this.error = error;
	}


	public String getMessageList() {
		return messageList;
	}


	public void setMessageList(String messageList) {
		this.messageList = messageList;
	}


}
