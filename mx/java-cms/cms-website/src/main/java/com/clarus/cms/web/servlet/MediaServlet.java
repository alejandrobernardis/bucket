package com.clarus.cms.web.servlet;

import java.io.BufferedInputStream;
import java.io.InputStream;
import java.io.OutputStream;
import java.util.Arrays;

import javax.servlet.http.HttpServlet;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.springframework.web.context.WebApplicationContext;
import org.springframework.web.context.support.WebApplicationContextUtils;

import com.clarus.cms.model.catalog.AcceptedFileExtension;
import com.clarus.cms.model.catalog.MediaType;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.ws.ContentService;

public class MediaServlet extends HttpServlet {
	private static final long serialVersionUID = -5591195088872947982L;
	protected Log log = LogFactory.getLog(getClass());

	public void doGet(javax.servlet.http.HttpServletRequest request, javax.servlet.http.HttpServletResponse response) {

		try {
			byte[] bytes = new byte[0];
			OutputStream out = response.getOutputStream();
			WebApplicationContext wac = WebApplicationContextUtils.getRequiredWebApplicationContext(getServletContext());

			ContentService contentService = (ContentService) wac.getBean("contentService", ContentService.class);

			String parameter = request.getRequestURI().replaceFirst(request.getContextPath() + request.getServletPath() + "/","");
			
			String[] elements = parameter.split("\\.");
			String[] parameters = elements[0].split("\\/");
			String extension = elements[1].toUpperCase();
			String media = parameters[0].toUpperCase();
			Integer mediaId = -1;
			if( parameters.length > 1 ){
				mediaId = new Integer(parameters[1]);
			}

			
			//log.info(parameter);

			AcceptedFileExtension fileExtension = AcceptedFileExtension.valueOf(extension);
			MediaType mediaType = MediaType.valueOf(media); 

			response.setContentType(fileExtension.getMimeType());
			
			switch( mediaType ) {
				case CONTENT:
					Content content = null;
					if( mediaId > 0 ){
						content = contentService.findContentsById(mediaId);
					}
					
					if(content != null && content.getImage()!=null && content.getImage().length > 0){
						bytes = content.getImage();
					}else{
						byte[] img = new byte[2000];
						int readBytes = 0; 
						InputStream is = getClass().getResourceAsStream("/img/dot." + fileExtension.toString().toLowerCase());
						BufferedInputStream bis = new BufferedInputStream(is);
						readBytes = bis.read(img);
						bytes = Arrays.copyOf( img, readBytes );
						img = null;
					}
					content = null;
					break;
					
				case ANIMATION:
					Animation animation = contentService.findContentAnimation(mediaId);
					if( animation != null && animation.getData() != null && animation.getData().length > 0 ){
						bytes = animation.getData();
					}else{
						byte[] img = new byte[5000];
						int readBytes = 0; 
						InputStream is = MediaServlet.class.getResourceAsStream("/img/dot." + fileExtension.toString().toLowerCase());
						readBytes = is.read(img);
						bytes = Arrays.copyOf( img, readBytes );
						img = null;
					}
					animation = null;
					break;
				case PUBLICATION:
					Publication publication = contentService.findPublication(mediaId);
					if( publication != null && publication.getImage() != null && publication.getImage().length > 0 ){
						bytes = publication.getImage();
					}else{
						byte[] img = new byte[5000];
						int readBytes = 0; 
						InputStream is = MediaServlet.class.getResourceAsStream("/img/dot." + fileExtension.toString().toLowerCase());
						readBytes = is.read(img);
						bytes = Arrays.copyOf( img, readBytes );
						img = null;
					}
					publication = null;
					break;
				case PUBLICATION_PAGE:
					PublicationPage page = contentService.findPublicationPage(mediaId);
					if( page != null && page.getImage() != null && page.getImage().length > 0 ){
						bytes = page.getImage();
					}else{
						byte[] img = new byte[5000];
						int readBytes = 0; 
						InputStream is = MediaServlet.class.getResourceAsStream("/img/dot." + fileExtension.toString().toLowerCase());
						readBytes = is.read(img);
						bytes = Arrays.copyOf( img, readBytes );
						img = null;
					}
					publication = null;
					break;
			}
			
			out.write(bytes);
			bytes = null;

		} catch (Exception e) {
			log.error("Error al obtener el medio", e);
		}

	}
}
