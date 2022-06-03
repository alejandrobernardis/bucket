package com.clarus.web.controller;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.richfaces.component.UITree;
import org.richfaces.component.html.HtmlTree;
import org.richfaces.event.NodeSelectedEvent;
import org.richfaces.event.UploadEvent;
import org.richfaces.model.TreeNodeImpl;
import org.richfaces.model.UploadItem;

import com.clarus.cms.model.catalog.AcceptedFileExtension;
import com.clarus.cms.vo.TreeNodeContentType;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.ws.ContentService;
import com.clarus.transport.Agent;
import com.clarus.web.form.PublicationForm;
import com.clarus.web.util.Util;


public class PublicationController {

	protected Log log = LogFactory.getLog(this.getClass());
	private ContentService contentService;
	private PublicationForm publicationForm;
	private String message;
	private Boolean success;
	private Boolean error;
	private Integer pageIndex;
	
	
	public String addPublication(){
		publicationForm.setSelectedPublication(new Publication());
		publicationForm.setPages(new ArrayList<PublicationPage>());
		return "PublicationController:addPublication";
	}
	
	public String editPublication(){
		Publication publication = null;
		try{
			publication = contentService.findPublication(publicationForm.getSelectedPublication().getIdPublication());
		}catch (Exception e) {
			log.error("Error al obtener la publicacion " + publicationForm.getSelectedPublication().getIdPublication(), e);
		}
		publicationForm.setSelectedPublication(publication);
		if( publication != null ){
			List<PublicationPage> pages = null;
			try{
				pages = contentService.findPublicationPages(publication.getIdPublication());
			}catch (Exception e) {
				log.error("Error al obtrener las paginas de la publicacion " + publication.getIdPublication(), e);
			}
			publicationForm.setPages(pages);
		}
		return "PublicationController:addPublication";
	}
	
	public String deletePublications(){
		for( Agent<Publication> agentPublication : publicationForm.getPublicationList() ){
			if ( agentPublication.getSelected() ){
				Publication tempPub = agentPublication.getValue();  
				List<PublicationPage> pages = null;
				try{
					pages = contentService.findPublicationPages(tempPub.getIdPublication());
				}catch (Exception e) {
					log.error("Error al obtener las paginas de la publicacion " + tempPub.getIdPublication(), e);
				}
				if( pages != null ){
					for( PublicationPage page : pages ){
						try{
							contentService.deletePublicationPage(page);
						}catch (Exception e) {
							log.error("Error al borrar la pagina " + page,e);
						}
					}
				}
				try{
					contentService.deletePublication(agentPublication.getValue());
				}catch (Exception e) {
					log.error("Error al borrar la publicacion " + agentPublication.getValue(),e);
				}
			}
		}
		listPublications();
		return "PublicationController:deletePublication";
	}
	
	
	public String savePublication(){
		try{
			publicationForm.getSelectedPublication().setIdContentType(publicationForm.getSelectedContentType().getIdContentType());
			Publication savedPublication = contentService.savePublication(publicationForm.getSelectedPublication());
			publicationForm.setSelectedPublication(savedPublication);
			
			List<PublicationPage> pages = contentService.findPublicationPages(savedPublication.getIdPublication());
			for( PublicationPage page : pages ){
				contentService.deletePublicationPage(page);
			}
			
			for( int i = 0; i < publicationForm.getPages().size(); i++ ){
				PublicationPage page = publicationForm.getPages().get(i);
				page.setIdPublication(publicationForm.getSelectedPublication().getIdPublication());
				page.setIdPublicationPage(null);
				page.setOrder(i);
				contentService.savePublicationPage(page);
			}
			error = Boolean.FALSE;
			message = Util.loadErrorMessage("labels.labels", "saveSuccesful");
		}catch (Exception e) {
			log.error( "Error al guardar la Publicaion", e );
			error = Boolean.TRUE;
			message = Util.loadErrorMessage("labels.labels", "saveError");
		}
		return "PublicationController:savePublication";
			
	}
	
	
	
	
	public String listPublications(){

		List<TreeNodeContentType> nodes = null;
		try{
			nodes = contentService.findContentTypeTree();
		}catch (Exception e) {
			log.error("Error al biscar los Contenttypes", e);
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
		
		publicationForm.setPublicationList(null);
		publicationForm.setSelectedPublication(new Publication());
		publicationForm.setPages(new ArrayList<PublicationPage>());
		publicationForm.setContentTypeTree(base);
		if( publicationForm.getSelectedContentType() != null && publicationForm.getSelectedContentType().getIdContentType() != null){
			
			List<Publication> publicationList = null;
			try{
				publicationList = contentService.findPublications(publicationForm.getSelectedContentType().getIdContentType());
			}catch (Exception e) {
				log.error("Error al buscar las publicaciones " + publicationForm.getSelectedContentType().getIdContentType() , e);
			}
	        publicationForm.setPublicationList(new ArrayList<Agent<Publication>>());
	        if( publicationList != null ){
		        for( Publication publication : publicationList ){
		        	publicationForm.getPublicationList().add(new Agent<Publication>(publication));
		        }
	        }
		}
		
		return "PublicationController:listPublications";
	}



	public ContentService getContentService() {
		return contentService;
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
        publicationForm.setSelectedContentType(agent.getValue());
        
        List<Publication> publicationList = null;
        try{
        	publicationList = contentService.findPublications(agent.getValue().getIdContentType());
        }catch (Exception e) {
			log.error("Error al buscar las publicaciones para " + agent.getValue().getIdContentType(),e);
		}
        publicationForm.setPublicationList(new ArrayList<Agent<Publication>>());
        if( publicationList != null ){
	        for( Publication publication : publicationList ){
	        	publicationForm.getPublicationList().add(new Agent<Publication>(publication));
	        }
        }

    }



	public Boolean getError() {
		return error;
	}

	public void setError(Boolean error) {
		this.error = error;
	}

	public Long getDummy(){
		return Math.round( Math.random() * 100000000 ); 
	}
	
	public PublicationForm getPublicationForm() {
		return publicationForm;
	}

	public void setPublicationForm(PublicationForm publicationForm) {
		this.publicationForm = publicationForm;
	}
	
	public void paint(OutputStream out, Object data) throws IOException{
		 out.write(publicationForm.getSelectedPublication().getImage());
	}
	
	public void listener(UploadEvent event) throws Exception{
        UploadItem item = event.getUploadItem();
        String fileName = item.getFileName();
        String extension = fileName.substring(fileName.lastIndexOf('.')+1).toUpperCase();
        AcceptedFileExtension ext = AcceptedFileExtension.valueOf(extension);
        publicationForm.getSelectedPublication().setImageType(ext);
        publicationForm.getSelectedPublication().setImage(item.getData());
	}

	public Integer getPageIndex() {
		return pageIndex;
	}

	public void setPageIndex(Integer pageIndex) {
		this.pageIndex = pageIndex;
	}
	
	
	public void moveLeft(){
		if( pageIndex == 0 ){
			return;
		}
		PublicationPage page = publicationForm.getPages().get(pageIndex);
		publicationForm.getPages().remove(pageIndex.intValue());
		publicationForm.getPages().add(pageIndex-1, page);
	}
	
	public void moveRight(){
		if( pageIndex == publicationForm.getPages().size() - 1 ){
			return;
		}
		PublicationPage page = publicationForm.getPages().get(pageIndex);
		publicationForm.getPages().remove(pageIndex.intValue());
		publicationForm.getPages().add(pageIndex + 1, page);
	}
	
	public void deletePage(){
		publicationForm.getPages().remove(pageIndex.intValue());
	}
	
	
	public void paintPage(OutputStream out, Object data) throws IOException{
		 Integer index = (Integer)data;
		 PublicationPage page = publicationForm.getPages().get(index);
		 out.write(page.getImage());
	}
	
	public void paintPublication(OutputStream out, Object data) throws IOException{
		 Integer index = (Integer)data;
		 Publication publication = publicationForm.getPublicationList().get(index).getValue();
		 out.write(publication.getImage());
	}
	
	public void listenerPage(UploadEvent event) throws Exception{
        UploadItem item = event.getUploadItem();
        PublicationPage page = new PublicationPage();
        String fileName = item.getFileName();
        String extension = fileName.substring(fileName.lastIndexOf('.')+1).toUpperCase();
        AcceptedFileExtension ext = AcceptedFileExtension.valueOf(extension);
        page.setImageType(ext);
        page.setImage(item.getData());
        publicationForm.getPages().add(page);
	} 
	
	
}
