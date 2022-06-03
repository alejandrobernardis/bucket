package com.clarus.cms.ws.impl;

import java.util.List;

import com.clarus.cms.persistence.UserDao;
import com.clarus.cms.vo.model.User;
import com.clarus.cms.ws.UserService;

public class UserServiceImpl implements UserService{
	private UserDao userDao;

	public void deleteUsers( List<User> users ){
		userDao.deleteUsers(users);
	}
	
	public User findUserByCredentials( String userName, String password ){
		return userDao.findUserByCredentials(userName, password);
	}
	
	public List<User> findUsers( ){
		return userDao.findUsers();
	}
	
	public User saveUser( User user ){
		return userDao.saveOrUpdateUser(user);
	}
	
	public User findUserById( Integer id ){
		return userDao.findUserById(id);
	}
	
	public User findUserByUsername( String userName ){
		return userDao.findUserByUsername(userName);
	}
	
	public UserDao getUserDao() {
		return userDao;
	}

	public void setUserDao(UserDao userDao) {
		this.userDao = userDao;
	} 
	
	

}
