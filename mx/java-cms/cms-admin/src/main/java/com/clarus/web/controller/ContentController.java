package com.clarus.web.controller;

import java.io.IOException;
import java.io.OutputStream;
import java.util.ArrayList;
import java.util.List;

import javax.faces.context.FacesContext;
import javax.faces.model.SelectItem;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.richfaces.component.UITree;
import org.richfaces.component.html.HtmlTree;
import org.richfaces.event.NodeSelectedEvent;
import org.richfaces.event.UploadEvent;
import org.richfaces.model.TreeNodeImpl;
import org.richfaces.model.UploadItem;

import com.clarus.cms.model.catalog.AnimationType;
import com.clarus.cms.model.catalog.Language;
import com.clarus.cms.vo.AnimationImages;
import com.clarus.cms.vo.FlashAnimation;
import com.clarus.cms.vo.Image;
import com.clarus.cms.vo.TreeNodeContentType;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.ws.ContentService;
import com.clarus.transport.Agent;
import com.clarus.web.form.ContentForm;
import com.clarus.web.util.Util;


public class ContentController {

	protected Log log = LogFactory.getLog(this.getClass());
	private ContentService contentService;
	private ContentForm contentForm;
	private Image contentImage;
	private FlashAnimation animationFlash; 
	private AnimationImages animationImages;
	private String message;
	private Boolean success;
	private Integer animationIndex;
	private Boolean error;
	
	
	public List<SelectItem> getAnimationTypes(){
		AnimationType[] animationTypes = AnimationType.values();
		List<SelectItem> anims = new ArrayList<SelectItem>();
		for( AnimationType animationType : animationTypes ){
			anims.add(new SelectItem(animationType, animationType.name()));
		}
		return anims;
	}
	
	public void setAnimationTypes( List<SelectItem> items ){
		
	}
	
	public List<SelectItem> getLanguages(){
		Language[] langs = Language.values();
		List<SelectItem> languages = new ArrayList<SelectItem>();
		for( Language language : langs ){
			languages.add(new SelectItem(language, language.name()));
		}
		return languages;
	}
	
	public void setLanguages( SelectItem[] languajes ){
		
	}
	
	public String getEditorLanguages(){
		Language[] langs = Language.values();
		String languages = "";
		
		String selLang =  FacesContext.getCurrentInstance().getViewRoot().getLocale().getLanguage().toUpperCase();
		if( contentForm.getSelectedContent()!= null && contentForm.getSelectedContent().getLanguage() != null ){
			selLang = contentForm.getSelectedContent().getLanguage().name();
		}
		for( Language language : langs ){
			if( language.name().equals(selLang) ){
				languages +="+";
			}
			languages += language.name() + "=" + language.name().toLowerCase()+",";
		}
		return languages.substring( 0, languages.length() - 1 );
	}
	
	public void setEditorLanguages( String lang ){
		
	}
	
	
	public String editContent(){
		Integer idContent = contentForm.getSelectedContent().getIdContent();
		Content selContent = null;
		try{
			selContent = contentService.findContentsById(idContent);
		}catch (Exception e) {
			log.error("Error al obtener el contenido " + idContent, e);
		}
		List<Animation> animations =  null;
		try{
			animations = contentService.findContentAnimations(idContent);
		}catch (Exception e) {
			log.error("Error al obtener las aniumaciones para el contenido " + idContent, e);
		}
		contentForm.setSelectedContent(selContent);
		contentForm.setSelectedContentAnimation(animations);
		
		animationImages.setImages(new ArrayList<Image>());
		if( animations != null ){
			for( Animation animation : animations ){
				if( contentForm.getSelectedContent().getAnimationType().equals(AnimationType.SLIDESHOW) ){
					Image image = new Image();
					image.setValue(animation.getData());
					image.setPreferedHeight(animationImages.getPreferedHeight());
					animationImages.getImages().add(image);
				}else{
					animationFlash.setValue(animation.getData());
				}
			}
		}
		if( selContent != null ){
			contentImage.setValue(selContent.getImage());
		}
		return "ContentController:editContent";
	}
	
	public String addContent(){
		contentForm.setSelectedContentAnimation(new ArrayList<Animation>());
		contentForm.setSelectedContent(new Content());
		contentImage.setValue(new byte[0]);
		animationImages.setImages(new ArrayList<Image>());
		return "ContentController:addContent";
	}
	
	
	public String saveContent(){
		try{
			
			contentForm.getSelectedContent().setImage(contentImage.getValue());
			contentForm.getSelectedContent().setIdContentType(contentForm.getSelectedContentType().getIdContentType());
			Content savedContent = contentService.saveContent(contentForm.getSelectedContent());
			contentForm.setSelectedContent(savedContent);
			int origAnimationsNumber  = contentForm.getSelectedContentAnimation().size();
			if( contentForm.getSelectedContent().getAnimationType().equals(AnimationType.SLIDESHOW) ){
				int newAnimationsNumber = animationImages.getSize();
				
				if( origAnimationsNumber > newAnimationsNumber ){
					for( int i = origAnimationsNumber; i > newAnimationsNumber  ; i--){
						Animation animation = contentForm.getSelectedContentAnimation().get( i - 1 );
						contentService.deleteContentAnimation(animation);
						contentForm.getSelectedContentAnimation().remove( i-1 );
					}
				}
				
				for( int i = 0; i < newAnimationsNumber ; i++){
					Image image = animationImages.getImages().get(i);
					Animation animation = null;
					if( i < origAnimationsNumber ){
						animation = contentForm.getSelectedContentAnimation().get(i);
						contentForm.getSelectedContentAnimation().set(i, animation );
					}else{
						animation = new Animation();
						contentForm.getSelectedContentAnimation().add(i,animation);
					}
					animation.setExtension("jpg");
					animation.setIdContent(savedContent.getIdContent());
					animation.setOrder(i);
					animation.setData(image.getValue());			
					Animation savedAnimation = contentService.saveContentAnimation(animation); 
					animation.init(savedAnimation);
				}
			}else{
				
				for( int i = origAnimationsNumber; i > 0  ; i--){
					Animation animation = contentForm.getSelectedContentAnimation().get( i - 1 );
					contentService.deleteContentAnimation(animation);
					contentForm.getSelectedContentAnimation().remove( i-1 );
				}
				Animation animation = new Animation();
				contentForm.getSelectedContentAnimation().add(animation);
				animation.setExtension("swf");
				animation.setIdContent(savedContent.getIdContent());
				animation.setOrder(0);
				animation.setData(animationFlash.getValue());			
				Animation savedAnimation = contentService.saveContentAnimation(animation); 
				animation.init(savedAnimation);
			}
			
			error = Boolean.FALSE;
			message = Util.loadErrorMessage("labels.labels", "saveSuccesful");
		}catch (Exception e) {
			log.error( "Error al guardar el contenido", e );
			error = Boolean.TRUE;
			message = Util.loadErrorMessage("labels.labels", "saveError");
		}
		
		return "ContentController:saveContent";
	}
	
	
	public String deleteContents(){
		if( contentForm.getContentList() != null ){
			for( Agent<Content> agentContent : contentForm.getContentList()  ){
				if ( agentContent.getSelected() ){
					try{
						contentService.deleteContentAnimationsByContent(agentContent.getValue().getIdContent());
						contentService.deleteContent(agentContent.getValue());
					}catch (Exception e) {
						log.error("Error al borrar los contenidos", e);
					}
						
				}
			}
		}
		listContent();
		return "ContentController:deleteContents";
	}
	
	
	public String listContent(){
		animationImages.setImages(new ArrayList<Image>());
		contentImage.setValue(new byte[0]);
		animationFlash.setValue(new byte[0]);

		List<TreeNodeContentType> nodes = null;
		try{
			nodes = contentService.findContentTypeTree();
		}catch (Exception e) {
			log.error( "Error al obtener los contentTypes" , e);
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
		
		contentForm.setContentList(null);
		contentForm.setContentTypeTree(base);
		if( contentForm.getSelectedContentType() != null && contentForm.getSelectedContentType().getIdContentType() != null){
			List<Content> contentList = null;
			try{
				contentList = contentService.findContentsByContentType(contentForm.getSelectedContentType().getIdContentType());
			}catch (Exception e) {
				log.error("Error al obtener el contenido " + contentForm.getSelectedContentType().getIdContentType(), e);
			}
				
	        contentForm.setContentList(new ArrayList<Agent<Content>>());
	        if( contentList != null ){
		        for( Content content : contentList ){
		        	contentForm.getContentList().add(new Agent<Content>(content));
		        }
	        }
		}
		return "ContentController:listContent";
	}
	
	
	@SuppressWarnings("unchecked")
	public void processSelection(NodeSelectedEvent event) {
        HtmlTree tree = (HtmlTree) event.getComponent();
        Agent<ContentType> agent = (Agent<ContentType>) tree.getRowData();
        contentForm.setSelectedContentType(agent.getValue());
        
        List<Content> contentList = null;
        
        try{
        	contentList = contentService.findContentsByContentType(agent.getValue().getIdContentType());
        }catch (Exception e) {
			log.error("Error al obtener el contenido " + agent.getValue().getIdContentType(), e);
		}
        contentForm.setContentList(new ArrayList<Agent<Content>>());
        if( contentList != null ){
	        for( Content content : contentList ){
	        	contentForm.getContentList().add(new Agent<Content>(content));
	        }
        }

    }
	

	public ContentService getContentService() {
		return contentService;
	}

	public void setContentService(ContentService contentService) {
		this.contentService = contentService;
	}

	public ContentForm getContentForm() {
		return contentForm;
	}

	public void setContentForm(ContentForm contentForm) {
		this.contentForm = contentForm;
	}
	
	public Boolean nodeOpened(UITree tree){
		return Boolean.TRUE;
	}
	
	
	 public void paint(OutputStream out, Object data) throws IOException{
		 out.write(contentImage.getValue());
	 }

	 public void paintAnimation(OutputStream out, Object data) throws IOException{
		 Integer index = (Integer)data;
		 Image image = animationImages.getImages().get(index);
		 out.write(image.getValue());
	 }
	 
	 public void paintFlash(OutputStream out, Object data) throws IOException{
		 out.write(animationFlash.getValue());
	 }
	 
	 
	public Image getContentImage() {
		return contentImage;
	}

	public void setContentImage(Image contentImage) {
		this.contentImage = contentImage;
	}
	
	public void listener(UploadEvent event) throws Exception{
	        UploadItem item = event.getUploadItem();
	        contentImage.setValue(item.getData());
    }
	 
	public void listenerAnimation(UploadEvent event) throws Exception{
	        UploadItem item = event.getUploadItem();
	        Image image = new Image();
	        image.setValue(item.getData());
	        image.setPreferedHeight(animationImages.getPreferedHeight());
	        animationImages.getImages().add(image);
	}  
	
	public void listenerAnimationFlash(UploadEvent event) throws Exception{
        UploadItem item = event.getUploadItem();
        animationFlash.setValue(item.getData());
	}  
	
	 
	 
	public Long getDummy(){
		return Math.round( Math.random() * 100000000 ); 
	}

	public String getMessage() {
		return message;
	}

	public void setMessage(String message) {
		this.message = message;
	}

	public Boolean getSuccess() {
		return success;
	}

	public void setSuccess(Boolean success) {
		this.success = success;
	}

	public AnimationImages getAnimationImages() {
		return animationImages;
	}

	public void setAnimationImages(AnimationImages animationImages) {
		this.animationImages = animationImages;
	}

	public Integer getAnimationIndex() {
		return animationIndex;
	}

	public void setAnimationIndex(Integer animationIndex) {
		this.animationIndex = animationIndex;
	}

	public void moveLeft(){
		if( animationIndex == 0 ){
			return;
		}
		Image image = animationImages.getImages().get(animationIndex);
		animationImages.getImages().remove(animationIndex.intValue());
		animationImages.getImages().add(animationIndex-1, image);
	}
	
	public void moveRight(){
		if( animationIndex == animationImages.getImages().size() - 1 ){
			return;
		}
		Image image = animationImages.getImages().get(animationIndex);
		animationImages.getImages().remove(animationIndex.intValue());
		animationImages.getImages().add(animationIndex + 1, image);
	}
	
	public void deleteAnimationImage(){
		animationImages.getImages().remove(animationIndex.intValue());
	}

	public Boolean getError() {
		return error;
	}

	public void setError(Boolean error) {
		this.error = error;
	}

	public FlashAnimation getAnimationFlash() {
		return animationFlash;
	}

	public void setAnimationFlash(FlashAnimation animationFlash) {
		this.animationFlash = animationFlash;
	}
}
