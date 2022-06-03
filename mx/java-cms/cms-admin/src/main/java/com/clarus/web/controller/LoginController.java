package com.clarus.web.controller;

import javax.faces.context.FacesContext;
import javax.servlet.http.HttpServletRequest;

import com.clarus.cms.vo.model.User;
import com.clarus.cms.ws.UserService;

public class LoginController{
	private UserService userService;
	private String username;
	private String password;
	private User logedUser;
	private Boolean error = Boolean.FALSE;
	private ContentController contentCtrl;
	
	
	
	
	public String login(){
		User validateUser = userService.findUserByCredentials( username, password );
		if( validateUser != null ){
			logedUser.init(validateUser);
			error = Boolean.FALSE;
			
			contentCtrl.listContent();
			
			return "LoginController:login:OK";
		}
		
		logedUser.clean();
		error = Boolean.TRUE;
		return "LoginController:login:ERROR";
		
	}
	
	
	public String logout(){
		logedUser.clean();
		HttpServletRequest req = (HttpServletRequest)FacesContext.getCurrentInstance().getExternalContext().getRequest();
		req.getSession().invalidate();
		return "LoginController:logout";
	}
	
	
	
	public UserService getUserService() {
		return userService;
	}

	public void setUserService(UserService userService) {
		this.userService = userService;
	}

	public User getLogedUser() {
		return logedUser;
	}

	public void setLogedUser(User logedUser) {
		this.logedUser = logedUser;
	}



	public String getUsername() {
		return username;
	}



	public void setUsername(String username) {
		this.username = username;
	}



	public String getPassword() {
		return password;
	}



	public void setPassword(String password) {
		this.password = password;
	}



	public Boolean getError() {
		return error;
	}



	public void setError(Boolean error) {
		this.error = error;
	}


	public ContentController getContentCtrl() {
		return contentCtrl;
	}


	public void setContentCtrl(ContentController contentCtrl) {
		this.contentCtrl = contentCtrl;
	}

	
	
	
	
}
