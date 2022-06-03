package com.clarus.web.filter;

import java.io.IOException;

import javax.servlet.Filter;
import javax.servlet.FilterChain;
import javax.servlet.FilterConfig;
import javax.servlet.ServletException;
import javax.servlet.ServletRequest;
import javax.servlet.ServletResponse;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.clarus.cms.vo.model.User;

public class SessionFilter implements Filter {
	
	private String timeoutPage =  "/pages/login.jsf" ; 
	private final Log log = LogFactory.getLog(getClass());
	
	public void destroy() {
		

	}

	public void doFilter(ServletRequest request, ServletResponse response,
			FilterChain filterChain) throws IOException, ServletException {

		HttpServletRequest httpServletRequest = (HttpServletRequest) request;
		HttpServletResponse httpServletResponse = (HttpServletResponse) response;

		String timeoutUrl = httpServletRequest.getContextPath() + timeoutPage;
		
		String requestedPage = httpServletRequest.getRequestURI();
		
			if ( (!isSessionValid(httpServletRequest) || !isUserLoged(httpServletRequest)) 
					&& !requestedPage.endsWith(timeoutPage)  ) {
				
					User logedUser = (User)httpServletRequest.getSession().getAttribute("logedUser");
					if( logedUser != null ){
						logedUser.clean();
					}
					httpServletRequest.getSession().invalidate();
					httpServletRequest.getSession(true);
					log.info("session is invalid! redirecting to timeoutpage : " + timeoutUrl);
					httpServletResponse.sendRedirect(timeoutUrl);
					return;
			}
		
		filterChain.doFilter(request, response);
	}

	public void init(FilterConfig arg0) throws ServletException {
		

	}

	  
	  private boolean isSessionValid ( HttpServletRequest httpServletRequest ) {
		   return httpServletRequest.getRequestedSessionId() != null && httpServletRequest.isRequestedSessionIdValid() ;		   
	  } 
	  
	 private boolean isUserLoged( HttpServletRequest httpServletRequest ){
		 User logedUser = (User)httpServletRequest.getSession().getAttribute("logedUser");
		 return logedUser != null && logedUser.getIdUser() != null; 
	 }
	  
}
