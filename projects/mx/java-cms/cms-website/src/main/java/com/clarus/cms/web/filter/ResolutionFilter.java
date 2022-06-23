package com.clarus.cms.web.filter;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.RequestDispatcher;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.lang.StringUtils;
import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.clarus.cms.vo.Config;
import com.clarus.cms.model.catalog.Language;;

public class ResolutionFilter implements Filter {
	
	String resolutionPage;

	protected final Log log = LogFactory.getLog(getClass());
	
	private FilterConfig filterConfig = null;
	
	public void destroy() {
		

	}

	public void init(FilterConfig filterConfig) throws ServletException {
		this.filterConfig = filterConfig;
	}
	
	public void doFilter(ServletRequest request, ServletResponse response,
			FilterChain filterChain) throws IOException, ServletException {

		HttpServletRequest httpServletRequest = (HttpServletRequest) request;
		HttpServletResponse httpServletResponse = (HttpServletResponse) response;

		
		
		String resolutionPage = filterConfig.getInitParameter("resolutionPage");
		
		log.info(resolutionPage);
		
		Config config = (Config)httpServletRequest.getSession().getAttribute("config");
		if( config == null  ){
			config = new Config();
			httpServletRequest.getSession().setAttribute("config", config);
		}
		
		String lang = httpServletRequest.getParameter("lang");
		if(StringUtils.isBlank(lang) ){
			if( StringUtils.isBlank( config.getLocale()) ){
				config.setLocale("ES");
			}
		}else{
			Language language = Language.valueOf(lang.toUpperCase());
			config.setLocale(language.toString());
		}
		
		if( config.getWidth() == null || config.getHeight() == null ){
			String width = httpServletRequest.getParameter("width");
			String height = httpServletRequest.getParameter("height");
			if( StringUtils.isEmpty(width) || StringUtils.isEmpty(height) ){
				RequestDispatcher dispatcher = httpServletRequest.getRequestDispatcher(resolutionPage);
				dispatcher.forward(httpServletRequest, httpServletResponse);
				return;
			}else{
				config.setHeight(new Integer(height));
				config.setWidth(new Integer(width));
			}
		}

		filterChain.doFilter(request, response);
	}

	public String getResolutionPage() {
		return resolutionPage;
	}

	public void setResolutionPage(String resolutionPage) {
		this.resolutionPage = resolutionPage;
	}

}
