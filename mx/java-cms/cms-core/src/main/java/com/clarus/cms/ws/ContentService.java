package com.clarus.cms.ws;

import java.util.List;

import com.clarus.cms.model.catalog.Language;
import com.clarus.cms.vo.TreeNodeContentType;
import com.clarus.cms.vo.TreeNodeContentTypeDisplay;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.ContentTypeLabel;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.vo.model.Store;

public interface ContentService {
	boolean hasContents( Integer idContentType ) throws Exception;
	List<TreeNodeContentTypeDisplay> getActiveContentTypes( Language language ) throws Exception;
	ContentType getDefaultPublishedContentType( Language lang ) throws Exception;
	Content getPublishedContent( Integer contentType, Language language ) throws Exception;
	List<TreeNodeContentType> findContentTypeTree() throws Exception;
	List<ContentType> findParentContentTypes() throws Exception;
	List<ContentType> findAllContentTypes() throws Exception;
	ContentType saveOrUpdateContentType( ContentType contentType ) throws Exception;	
	void deleteContentType( ContentType contentType  ) throws Exception;
	ContentType findContentTypeByName( String name ) throws Exception;
	List<ContentTypeLabel> findContentTypeLabelsForContent( Integer idConentType ) throws Exception;
	ContentTypeLabel saveContentTypeLabel( ContentTypeLabel label ) throws Exception;
	void deleteContentTypeLabel(ContentTypeLabel label ) throws Exception;
	List<Content> findContentsByContentType( Integer idConentType ) throws Exception;
	Content findContentsById( Integer idContent ) throws Exception;
	List<Animation> findContentAnimations( Integer idContent ) throws Exception;
	void deleteContentAnimation( Animation animation ) throws Exception;	
	Animation saveContentAnimation( Animation animation ) throws Exception;
	Content saveContent( Content content ) throws Exception;
	void deleteContent( Content content  ) throws Exception;
	void deleteContentAnimations( List<Animation> animations ) throws Exception;
	List<Animation> saveContentAnimations( List<Animation> animations ) throws Exception;
	void deleteContentAnimationsByContent( Integer contentId ) throws Exception;
	Animation findContentAnimation( Integer idAnimation ) throws Exception;
	List<Animation> getAnimationsForWeb( Integer idContent ) throws Exception;
	List<Store> findStores( Integer idContentType ) throws Exception;
	Store saveStore(Store store) throws Exception;
	Store findStore( Integer idStore ) throws Exception;
	void deleteStore( Store store ) throws Exception;
	Publication findPublication( Integer idPublication ) throws Exception;
	void deletePublication( Publication publication ) throws Exception;
	Publication savePublication( Publication publication ) throws Exception;
	List<Publication> findPublications( Integer idContentType ) throws Exception;
	PublicationPage findPublicationPage( Integer idPublication ) throws Exception;
	void deletePublicationPage( PublicationPage publicationPage ) throws Exception;
	PublicationPage savePublicationPage( PublicationPage publicationPage ) throws Exception;
	List<PublicationPage> findPublicationPages( Integer idPublicationPage ) throws Exception;
	List<Publication> getPublishedPublications(Integer contentType) throws Exception;
	List<PublicationPage> getPublishedPublicationPages(Integer publication) throws Exception;
	List<Store> getPublishedStores( Integer idContentType ) throws Exception;
	
}
