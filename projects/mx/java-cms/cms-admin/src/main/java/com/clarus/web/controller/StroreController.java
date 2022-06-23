package com.clarus.web.controller;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.richfaces.component.UITree;
import org.richfaces.component.html.HtmlTree;
import org.richfaces.event.NodeSelectedEvent;
import org.richfaces.model.TreeNodeImpl;

import com.clarus.cms.vo.TreeNodeContentType;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.Store;
import com.clarus.cms.ws.ContentService;
import com.clarus.transport.Agent;
import com.clarus.web.form.StoreForm;
import com.clarus.web.util.Util;


public class StroreController {

	protected Log log = LogFactory.getLog(this.getClass());
	private ContentService contentService;
	private StoreForm storeForm;
	private String message;
	private Boolean success;
	private Boolean error;
	
	
	public String addStore(){
		storeForm.setSelectedStore(new Store());
		return "StoreController:addStore";
	}
	
	public String editStore(){
		Store store = null;
		try{
			store = contentService.findStore(storeForm.getSelectedStore().getIdStore());
		}catch (Exception e) {
			log.error("Error al buscar la tienda " + storeForm.getSelectedStore().getIdStore(), e);
		}
		storeForm.setSelectedStore(store);
		return "StoreController:addStore";
	}
	
	public String deleteStores(){
		for( Agent<Store> agentStore : storeForm.getStoreList() ){
			if ( agentStore.getSelected() ){
				try{
					contentService.deleteStore(agentStore.getValue());
				}catch (Exception e) {
					log.error("Error al borrar la tienda "+agentStore.getValue(), e);
				}
			}
		}
		listStores();
		return "StoreController:deleteStores";
	}
	
	
	public String saveStore(){
		try{
			storeForm.getSelectedStore().setIdContentType(storeForm.getSelectedContentType().getIdContentType());
			Store savedStore = contentService.saveStore(storeForm.getSelectedStore());
			storeForm.setSelectedStore(savedStore);
			error = Boolean.FALSE;
			message = Util.loadErrorMessage("labels.labels", "saveSuccesful");
		}catch (Exception e) {
			log.error( "Error al guardar el store", e );
			error = Boolean.TRUE;
			message = Util.loadErrorMessage("labels.labels", "saveError");
		}
		return "StoreController:addStore";
			
	}
	
	
	
	
	public String listStores(){

		List<TreeNodeContentType> nodes = null;
		try{
			nodes = contentService.findContentTypeTree();
		}catch (Exception e) {
			log.error("Error al buscar los content types", e);
		}
		TreeNodeImpl<Agent<ContentType>> root = new TreeNodeImpl<Agent<ContentType>>();
		if( nodes != null ){
			for (TreeNodeContentType node : nodes) {
				TreeNodeImpl<Agent<ContentType>> treeNode = new TreeNodeImpl<Agent<ContentType>>();
				Agent<ContentType> agentNode = new Agent<ContentType>();
				agentNode.setValue(node.getContentType());
				
				agentNode.setType("Parent");
				if( !node.getContentType().getActive() ){
					agentNode.setType("Inactive");
				}
				treeNode.setData(agentNode);
				for (ContentType child : node.getChildren()) {
					
					Agent<ContentType> agentChild = new Agent<ContentType>();
					agentChild.setValue(child);
					agentChild.setType("Child");
					if( !child.getActive() ){
						agentChild.setType("Inactive");
					}
					TreeNodeImpl<Agent<ContentType>> treeNodeChild = new TreeNodeImpl<Agent<ContentType>>();
					treeNodeChild.setData(agentChild);
					
					
					treeNode.addChild(treeNodeChild.getData().getValue().getContentTypeName(),
							treeNodeChild);
				}
				root.addChild(treeNode.getData().getValue().getContentTypeName(), treeNode);
	
			}
		}
		
		
		Agent<ContentType> agentRoot = new Agent<ContentType>();
		agentRoot.setValue(new ContentType());
		agentRoot.setType("Root");
		root.setData(agentRoot);
		
		TreeNodeImpl<Agent<ContentType>> base = new TreeNodeImpl<Agent<ContentType>>();
		base.addChild("Root", root);
		
		storeForm.setStoreList(null);
		storeForm.setContentTypeTree(base);
		if( storeForm.getSelectedContentType() != null && storeForm.getSelectedContentType().getIdContentType() != null){
			List<Store> storeList = null;
			try{
				storeList = contentService.findStores(storeForm.getSelectedContentType().getIdContentType());
			}catch (Exception e) {
				log.error("Error al buscar las tiendas", e);
			}
	        storeForm.setStoreList(new ArrayList<Agent<Store>>());
	        if( storeList != null ){
		        for( Store store : storeList ){
		        	storeForm.getStoreList().add(new Agent<Store>(store));
		        }
	        }
		}
		
		return "StoreController:listStores";
	}



	public ContentService getContentService() {
		return contentService;
	}



	public StoreForm getStoreForm() {
		return storeForm;
	}



	public String getMessage() {
		return message;
	}



	public Boolean getSuccess() {
		return success;
	}



	public void setContentService(ContentService contentService) {
		this.contentService = contentService;
	}



	public void setStoreForm(StoreForm storeForm) {
		this.storeForm = storeForm;
	}



	public void setMessage(String message) {
		this.message = message;
	}



	public void setSuccess(Boolean success) {
		this.success = success;
	}
	
	public Boolean nodeOpened(UITree tree){
		return Boolean.TRUE;
	}

	@SuppressWarnings("unchecked")
	public void processSelection(NodeSelectedEvent event) {
        HtmlTree tree = (HtmlTree) event.getComponent();
        Agent<ContentType> agent = (Agent<ContentType>) tree.getRowData();
        storeForm.setSelectedContentType(agent.getValue());
        
        List<Store> storeList = null;
        try{
        	storeList = contentService.findStores(agent.getValue().getIdContentType());
        }catch (Exception e) {
			log.error("Error al buscar las tiendas para " + agent.getValue().getIdContentType(), e);
		}
        storeForm.setStoreList(new ArrayList<Agent<Store>>());
        if( storeList != null ){
	        for( Store store : storeList ){
	        	storeForm.getStoreList().add(new Agent<Store>(store));
	        }
        }

    }



	public Boolean getError() {
		return error;
	}



	public void setError(Boolean error) {
		this.error = error;
	}
	
}
