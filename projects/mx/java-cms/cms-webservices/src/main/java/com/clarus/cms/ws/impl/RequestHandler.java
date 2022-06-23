package com.clarus.cms.ws.impl;

import java.io.StringWriter;

import javax.xml.transform.Result;
import javax.xml.transform.Source;
import javax.xml.transform.Transformer;
import javax.xml.transform.TransformerConfigurationException;
import javax.xml.transform.TransformerException;
import javax.xml.transform.TransformerFactory;
import javax.xml.transform.dom.DOMSource;
import javax.xml.transform.stream.StreamResult;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.codehaus.xfire.MessageContext;
import org.codehaus.xfire.util.dom.DOMInHandler;
import org.codehaus.xfire.util.dom.DOMOutHandler;
import org.w3c.dom.Document;
import org.w3c.dom.Node;

public class RequestHandler {
	private final Log log= LogFactory.getLog(getClass());


	public void invoke(MessageContext arg0) throws Exception {
		// TODO Auto-generated method stub

		//Get Document to Soap Message
		Document docIn = null;
		try{
			docIn=(Document) arg0.getInMessage().getProperty(DOMInHandler.DOM_MESSAGE);
			log.info(docIn);
		}catch(Exception e){
			log.error(e.getMessage(), e );
		}
		Document docOut = null;
		try{
			docOut =(Document) arg0.getOutMessage().getProperty(DOMOutHandler.DOM_MESSAGE);
			log.info(docOut);
		}catch(Exception e){
			log.error(e.getMessage(), e );
		}
		
	}


	public String xmlToString(Node node) {
		try {
			Source source = new DOMSource(node);
			StringWriter stringWriter = new StringWriter();
			Result result = new StreamResult(stringWriter);
			TransformerFactory factory = TransformerFactory.newInstance();
			Transformer transformer = factory.newTransformer();
			transformer.transform(source, result);
			return stringWriter.getBuffer().toString();
		} catch (TransformerConfigurationException e) {
			log.error(e.getMessage(), e );
		} catch (TransformerException e) {
			log.error(e.getMessage(), e );
		}
		return null;
	}
}
