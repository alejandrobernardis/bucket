package com.clarus.web.controller;

import java.util.ArrayList;
import java.util.List;

import javax.faces.model.SelectItem;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;

import com.clarus.cms.model.catalog.Role;
import com.clarus.cms.vo.model.User;
import com.clarus.cms.ws.UserService;
import com.clarus.transport.Agent;
import com.clarus.web.form.UserForm;
import com.clarus.web.util.Util;

public class UserController {

	private UserForm userForm;
	private UserService userService;
	private User logedUser;
	private String message;
	private Boolean error;
	protected Log log = LogFactory.getLog(getClass());
	
	public String listUser(){
		List<User> users = userService.findUsers();
		List<Agent<User>> agentes = new ArrayList<Agent<User>>(); 
		if( users != null ){
			for( User user : users ){
				agentes.add(new Agent<User>(user));
			}
		}
		userForm.setUsers( agentes );
		return "UserController:listUser";
	}
	
	
	public String addUser(){
		userForm.getSelectedUser().clean();
		return "UserController:addUser";
	}
	
	public String editUser(){
		Integer id = userForm.getSelectedUser().getIdUser();
		User selUser = userService.findUserById(id);
		userForm.getSelectedUser().init(selUser);
		return "UserController:edditUser";
	}
	
	public String deleteUsers(){
		List<User> usersToDelete = new ArrayList<User>();
		for( Agent<User> user : userForm.getUsers() ){
			if( user.getSelected() != null && user.getSelected()){
				usersToDelete.add(user.getValue());
			}
		}
		userService.deleteUsers(usersToDelete);
		listUser();
		return "UserController:deleteUsers";
	}
	
	public String saveUser(){
		try{
			
			User validateUname = userService.findUserByUsername( userForm.getSelectedUser().getUsername() );
			if( validateUname != null && !validateUname.getIdUser().equals( userForm.getSelectedUser().getIdUser() ) ){
				 
				Util.addFacesMessageForId("username" , "labels.labels", "nameExists");
				error = null;
				return "UserController:saveUser";
			}
			
			User savedUser = userService.saveUser(userForm.getSelectedUser() );
			userForm.getSelectedUser().init(savedUser);
			error = Boolean.FALSE;
			message = Util.loadErrorMessage("labels.labels", "saveSuccesful");
		}catch (Exception e) {
			error = Boolean.TRUE;
			message = Util.loadErrorMessage("labels.labels", "saveError");
		}
		return "UserController:saveUser";
	}
	
	
	@SuppressWarnings("unchecked")
	public boolean filterByActive(Object current) {		
		Agent<User> currentUser = (Agent<User>)current;		 
		if (userForm.getSelectedFilterActive() == null ) {
			return true;
		}
		if (userForm.getSelectedFilterActive().equals( currentUser.getValue().getActive() )) {
			return true;
		}else {
			return false; 
		}
	}
	
	@SuppressWarnings("unchecked")
	public boolean filterByRole(Object current) {		
		Agent<User> currentUser = (Agent<User>)current;		 
		if (userForm.getSelectedFilterRole() == null ) {
			return true;
		}
		if (userForm.getSelectedFilterRole().equals( currentUser.getValue().getRole() )) {
			return true;
		}else {
			return false; 
		}
	}
	
	public SelectItem[] getRoles(){
		Role[] roles = Role.values();
		SelectItem[] items = new SelectItem[roles.length];
		for( int i = 0; i < roles.length; i++ ){
			Role role = roles[i]; 
			items[i] = new SelectItem(role, role.name());
		}
		return items;
		
	}
	
	
	public UserForm getUserForm() {
		return userForm;
	}

	public void setUserForm(UserForm userForm) {
		this.userForm = userForm;
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


	public String getMessage() {
		return message;
	}


	public void setMessage(String message) {
		this.message = message;
	}


	public Boolean getError() {
		return error;
	}


	public void setError(Boolean error) {
		this.error = error;
	}

	
}
