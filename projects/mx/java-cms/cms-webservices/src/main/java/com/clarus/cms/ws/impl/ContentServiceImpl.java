package com.clarus.cms.ws.impl;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import com.clarus.cms.model.catalog.Language;
import com.clarus.cms.persistence.ContentDao;
import com.clarus.cms.util.ComparatorContentTypeDisplayOrder;
import com.clarus.cms.util.ComparatorContentTypeDisplayTreeNode;
import com.clarus.cms.util.ComparatorContentTypeOrder;
import com.clarus.cms.util.ComparatorContentTypeTreeNode;
import com.clarus.cms.vo.ContentTypeDisplay;
import com.clarus.cms.vo.TreeNodeContentType;
import com.clarus.cms.vo.TreeNodeContentTypeDisplay;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.ContentTypeLabel;
import com.clarus.cms.vo.model.ContentTypeLabelId;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.vo.model.Store;
import com.clarus.cms.ws.ContentService;

public class ContentServiceImpl implements ContentService{
	private ContentDao contentDao; 
	
	public boolean hasContents( Integer idContentType ) throws Exception{
		return contentDao.hasContents(idContentType);
	}

	
	public List<TreeNodeContentTypeDisplay> getActiveContentTypes( Language language ) throws Exception{
		
		List<ContentTypeDisplay> contentTypes = contentDao.getActiveContentTypes(language);
		
		List <TreeNodeContentTypeDisplay> nodes = new ArrayList<TreeNodeContentTypeDisplay>();
		
		List<ContentTypeDisplay> contentTypeChildren  = new ArrayList<ContentTypeDisplay>();
		
		if( contentTypes != null ){
			for ( ContentTypeDisplay contentType : contentTypes ){
				if( contentType.getIdContentTypeParent() == null ){
					nodes.add(new TreeNodeContentTypeDisplay(contentType));
				}else{
					contentTypeChildren.add(contentType);
				}
			}
		}
		
		
		if( nodes.size() > 0 ){
			TreeNodeContentTypeDisplay parentNode = nodes.get(0);
			if( contentTypeChildren != null ){
				for( ContentTypeDisplay ctchild : contentTypeChildren ){
					boolean found = true;
					if( !(parentNode.getContentTypeDisplay().getIdContentType()).equals(ctchild.getIdContentTypeParent()) ){
						found = false;
						for( TreeNodeContentTypeDisplay pNode:  nodes){
							if( pNode.getContentTypeDisplay().getIdContentType().equals( ctchild.getIdContentTypeParent() ) ){
								found = true;
								parentNode = pNode;
								break;
							}
						}
					}
					if( found ){
						parentNode.getChildren().add(ctchild);
					}
				}
			}
			for( TreeNodeContentTypeDisplay pNode:  nodes){
				Collections.sort(pNode.getChildren(), new ComparatorContentTypeDisplayOrder()); 
			}
			Collections.sort(nodes, new ComparatorContentTypeDisplayTreeNode());
		}
		return nodes;
		
	}
	
	public ContentType getDefaultPublishedContentType( Language lang  ) throws Exception{
		return contentDao.getDefaultPublishedContentType( lang );
	}
	
	
	
	public Content getPublishedContent( Integer contentType, Language language ) throws Exception{
		
		Content content = contentDao.getPublishedContent(contentType, language);
		if( content == null ){
			content = new Content();
		}
		return content;
	}

	public ContentDao getContentDao() {
		return contentDao;
	}

	public void setContentDao(ContentDao contentDao) {
		this.contentDao = contentDao;
	}
	
	
	public List<TreeNodeContentType> findContentTypeTree() throws Exception{
		List <TreeNodeContentType> nodes = new ArrayList<TreeNodeContentType>();
		
		List<ContentType> contentTypes = contentDao.findAllContentTypes();
		List<ContentType> contentTypeChildren  = new ArrayList<ContentType>();
		if( contentTypes != null ){
			for ( ContentType contentType : contentTypes ){
				if( contentType.getIdContentTypeParent() == null ){
					nodes.add(new TreeNodeContentType(contentType));
				}else{
					contentTypeChildren.add(contentType);
				}
			}
		}
		
		if( nodes.size() > 0 ){
			TreeNodeContentType parentNode = nodes.get(0);
			if( contentTypeChildren != null ){
				for( ContentType ctchild : contentTypeChildren ){
					boolean found = true;
					if( !(parentNode.getContentType().getIdContentType()).equals(ctchild.getIdContentTypeParent()) ){
						found = false;
						for( TreeNodeContentType pNode:  nodes){
							if( pNode.getContentType().getIdContentType().equals( ctchild.getIdContentTypeParent() ) ){
								found = true;
								parentNode = pNode;
								break;
							}
						}
					}
					if( found ){
						parentNode.getChildren().add(ctchild);
					}
				}
			}
			
			
			for( TreeNodeContentType pNode:  nodes){
				List<ContentType> children = pNode.getChildren(); 
				Collections.sort(children, new ComparatorContentTypeOrder()); 
			}
			Collections.sort(nodes, new ComparatorContentTypeTreeNode());
		}
		return nodes;
	}
	
	
	
	
	public List<ContentType> findParentContentTypes() throws Exception{
		return contentDao.findParentContentTypes();
	}

	public ContentType saveOrUpdateContentType( ContentType contentType ) throws Exception{
		return contentDao.saveOrUpdateContentType(contentType);
	}
	
	public void deleteContentType( ContentType contentType  ) throws Exception{
		contentDao.deleteContentType(contentType);
	}
	
	public ContentType findContentTypeByName( String name ) throws Exception{
		return contentDao.findContentTypeByName(name);
	}

	
	public ContentTypeLabel saveContentTypeLabel( ContentTypeLabel label ) throws Exception{
		label = contentDao.saveContentTypeLabel(label);
		return label;
	}
	
	public void deleteContentTypeLabel( ContentTypeLabel label ) throws Exception{
		contentDao.deleteContentTypeLabel(label);
	}
	
	
	public List<ContentTypeLabel> findContentTypeLabelsForContent( Integer idContentType ) throws Exception{
		
		HashMap<Language, ContentTypeLabel> labelMap = new HashMap<Language, ContentTypeLabel>();
		
		List<ContentTypeLabel> labels = contentDao.findContentTypeLabelsForContent( idContentType );
		
		if( labels != null ){
			for( ContentTypeLabel label: labels ){
				labelMap.put(label.getId().getLanguage(), label);
			}
		}
		for( Language allowedLang :  Language.values()){
			if( labelMap.get(allowedLang)==null ){
				ContentTypeLabel label = new ContentTypeLabel();
				ContentTypeLabelId id = new ContentTypeLabelId( );
				id.setLanguage(allowedLang);
				id.setIdContentType(idContentType);
				label.setId(id);
				labelMap.put( allowedLang, label );
			}
		}
		
		List<ContentTypeLabel> allLabels = new ArrayList<ContentTypeLabel>();
		allLabels.addAll(labelMap.values());
		
		return allLabels;
		
	}
	
	public List<Content> findContentsByContentType( Integer idConentType ) throws Exception{
		return contentDao.findContentsByContentType(idConentType);
	}
	
	public Content findContentsById( Integer idContent ) throws Exception{
		return contentDao.findContentsById( idContent );
	}
	
	public List<Animation> findContentAnimations( Integer idContent ) throws Exception{
		return contentDao.findContentAnimations( idContent );
	}
	
	public List<Animation> getAnimationsForWeb( Integer idContent ) throws Exception{
		List<Animation> animations = contentDao.findContentAnimationsForWeb( idContent );
		return animations;
	}

	public List<ContentType> findAllContentTypes() throws Exception{
		return contentDao.findAllContentTypes();
	}
	
	
	public void deleteContentAnimation( Animation animation ) throws Exception{
		contentDao.deleteContentAnimation(animation);
	}
	
	public Animation saveContentAnimation( Animation animation ) throws Exception{
		return contentDao.saveContentAnimation(animation);
	}
	
	public Content saveContent( Content content ) throws Exception{
		return contentDao.saveContent(content);
	}
	
	public void deleteContent( Content content  ) throws Exception{
		contentDao.deleteContent(content);
	}
	
	
	
	public void deleteContentAnimations( List<Animation> animations ) throws Exception{
		if( animations != null ){
			for( Animation animation : animations ){
				contentDao.deleteContentAnimation(animation);
			}
		}
	}
	
	public List<Animation> saveContentAnimations( List<Animation> animations ) throws Exception{
		if( animations != null ){
			for( Animation animation : animations ){
				animation.init(contentDao.saveContentAnimation(animation));
			}
		}
		return animations;
	}
	
	
	public void deleteContentAnimationsByContent( Integer contentId ) throws Exception{
		contentDao.deleteContentAnimationsByContent(contentId);
	}
	
	
	public Animation findContentAnimation( Integer idAnimation ) throws Exception{
		return contentDao.findContentAnimation( idAnimation );
	}
	
	
	public List<Store> findStores( Integer idContentType ) throws Exception{
		return contentDao.findStores( idContentType );
	}
	
	public Store saveStore(Store store) throws Exception{
		return contentDao.saveStore(store);
	}
	
	
	public Store findStore( Integer idStore ) throws Exception{
		return contentDao.findStore(idStore);
	}
	
	
	public void deleteStore( Store store ) throws Exception{
		contentDao.deleteStore(store);
	}
	
	public Publication findPublication( Integer idPublication ) throws Exception{
		return contentDao.findPublication( idPublication );
	}
	
	public void deletePublication( Publication publication ) throws Exception{
		contentDao.deletePublication( publication );
	}
	
	public Publication savePublication( Publication publication ) throws Exception{
		return contentDao.savePublication( publication );
	}
	
	public List<Publication> findPublications( Integer idContentType ) throws Exception{
		return contentDao.findPublications( idContentType );
	}
	
	public PublicationPage findPublicationPage( Integer idPublication ) throws Exception{
		return contentDao.findPublicationPage( idPublication );
	}
	
	public void deletePublicationPage( PublicationPage publicationPage ) throws Exception{
		contentDao.deletePublicationPage( publicationPage );
	}
	
	
	public PublicationPage savePublicationPage( PublicationPage publicationPage ) throws Exception{
		return contentDao.savePublicationPage( publicationPage );
	}
	
	public List<PublicationPage> findPublicationPages( Integer idPublicationPage ) throws Exception{
		return contentDao.findPublicationPages( idPublicationPage );
	}
	
	public List<Publication> getPublishedPublications(Integer contentType) throws Exception{
		return contentDao.getPublishedPublications(contentType);
	}
	
	public List<PublicationPage> getPublishedPublicationPages(Integer publication) throws Exception{
		return contentDao.getPublishedPublicationPages(publication);
	}
	
	public List<Store> getPublishedStores( Integer idContentType ) throws Exception{
		return contentDao.getPublishedStores(idContentType);
	}
}
