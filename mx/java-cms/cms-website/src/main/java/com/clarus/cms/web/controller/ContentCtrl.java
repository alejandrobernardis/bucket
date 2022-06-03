package com.clarus.cms.web.controller;

import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;

import javax.faces.event.PhaseEvent;
import javax.faces.event.PhaseId;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.lang.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.clarus.cms.model.catalog.Language;
import com.clarus.cms.vo.Config;
import com.clarus.cms.vo.TreeNodeContentTypeDisplay;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.vo.model.Store;
import com.clarus.cms.web.util.Util;
import com.clarus.cms.ws.ContentService;

public class ContentCtrl implements Serializable{
	private Log log = LogFactory.getLog(getClass());
	private static final long serialVersionUID = 1L;
	private ContentService contentSrvc;
	private ContentFrm contentFrm;
	private String template = "/templateContent.xhtml";
	private Config config;
	
	
	public void findPublicationPages(){
		List<PublicationPage> pages = null;
		try{
			pages = contentSrvc.getPublishedPublicationPages(contentFrm.getPublication());
		}catch (Exception e) {
			log.error( "Error al obtener las paginas de la publicacion" + contentFrm.getPublication(), e );
		}
		contentFrm.setPages( pages );
	}
	
	public void cleanPublicationPages(){
		contentFrm.setPages( new ArrayList<PublicationPage>() );
	}
	
	
	public String getTemplate() {
		return template;
	}

	public void setTemplate(String template) {
		this.template = template;
	}

	public void init(PhaseEvent event){
		 if (event.getPhaseId() == PhaseId.RENDER_RESPONSE) {
			Language lang = Language.valueOf(config.getLocale());
			String contentType = Util.getRequestParameter("content");
			Integer contenTypeToSearch = null;
			if( StringUtils.isBlank(contentType)){
				ContentType ct = null;
				try{
					ct = contentSrvc.getDefaultPublishedContentType( lang );
				}catch (Exception e) {
					log.error("Error al obtener el Contentype por default", e);
				}
				if( ct != null){
					contenTypeToSearch = ct.getIdContentType();
				}
			}else{
				contenTypeToSearch = new Integer(contentType);
			}

			contentFrm.setContentType(contenTypeToSearch);
			 
			Content ct = null;
			try{
				ct = contentSrvc.getPublishedContent(contenTypeToSearch,lang);
			}catch (Exception e) {
				log.error("Error al obtener el contenido del tipo " + contenTypeToSearch + " en idioma " + lang, e);
				HttpServletResponse resp =  (HttpServletResponse)event.getFacesContext().getExternalContext().getResponse();
				try{
					resp.sendError(404);
				}catch (Exception ex) {
					log.error("Error al setar el error 404");
				}
			}
			if( ct == null || ct.getIdContent() == null){
				HttpServletResponse resp =  (HttpServletResponse)event.getFacesContext().getExternalContext().getResponse();
				try{
					resp.sendError(404);
				}catch (Exception ex) {
					log.error("Error al setar el error 404");
				}
			}
			contentFrm.setContent(ct);
			List<TreeNodeContentTypeDisplay> menu = null;
			try{
				menu = contentSrvc.getActiveContentTypes(lang);
			}catch (Exception e) {
				log.error("Error al obtener el menu en idioma " + lang, e);
			}
			contentFrm.setMenu(menu);
			if( contentFrm.getContent().getIdContent() != null ){
				List<Animation> anims = null;
				try{
					anims = contentSrvc.getAnimationsForWeb(contentFrm.getContent().getIdContent());
				}catch (Exception e) {
					log.error("Error al obtener las animaciones para el contenido " + contentFrm.getContent().getIdContent(), e);
				}
				contentFrm.setListAnimation( anims );
			}else{
				List<Animation> temp = new ArrayList<Animation>();
				contentFrm.setListAnimation( temp );
			}
			
			List<Publication> pubs = null;
			try{
				pubs = contentSrvc.getPublishedPublications( contenTypeToSearch );
			}catch (Exception e) {
				log.error("Error al obtener la publicaciones para " + contenTypeToSearch, e);
			}
			contentFrm.setListPublication(pubs);
			List<Store> stores = null;
			try{
				stores = contentSrvc.getPublishedStores(contenTypeToSearch );
			}catch (Exception e) {
				log.error("Error al obtener las tiendas para " + contenTypeToSearch, e);
			}
			contentFrm.setStores(stores);
		 }
	}

	
	
	
	
	public Language[] getLanguages(){
		return Language.values();
	}
	
	public ContentService getContentSrvc() {
		return contentSrvc;
	}

	public void setContentSrvc(ContentService contentSrvc) {
		this.contentSrvc = contentSrvc;
	}

	public Config getConfig() {
		return config;
	}

	public void setConfig(Config config) {
		this.config = config;
	}

	public ContentFrm getContentFrm() {
		return contentFrm;
	}

	public void setContentFrm(ContentFrm contentFrm) {
		this.contentFrm = contentFrm;
	}
	
}
