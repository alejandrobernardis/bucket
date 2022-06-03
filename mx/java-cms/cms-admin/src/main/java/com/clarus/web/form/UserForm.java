package com.clarus.web.form;

import java.io.Serializable;
import java.util.List;

import com.clarus.cms.model.catalog.Role;
import com.clarus.cms.vo.model.User;
import com.clarus.transport.Agent;

public class UserForm implements Serializable {

	private static final long serialVersionUID = 8676212211972982986L;
	
	private List<Agent<User>> users;

	private User selectedUser = new User();
	
	private Boolean selectedFilterActive;
	private Role selectedFilterRole;
	
	public User getSelectedUser() {
		return selectedUser;
	}

	public void setSelectedUser(User selectedUser) {
		this.selectedUser = selectedUser;
	}
	
	public List<Agent<User>> getUsers() {
		return users;
	}

	public void setUsers(List<Agent<User>> users) {
		this.users = users;
	}

	public Boolean getSelectedFilterActive() {
		return selectedFilterActive;
	}

	public void setSelectedFilterActive(Boolean selectedFilterActive) {
		this.selectedFilterActive = selectedFilterActive;
	}

	public Role getSelectedFilterRole() {
		return selectedFilterRole;
	}

	public void setSelectedFilterRole(Role selectedFilterRole) {
		this.selectedFilterRole = selectedFilterRole;
	}


}
