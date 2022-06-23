package com.clarus.cms.ws;

import java.util.List;

import com.clarus.cms.vo.model.User;

public interface UserService {
	User findUserByCredentials( String userName, String password );
	List<User> findUsers( );
	User findUserById( Integer id );
	User saveUser( User user );
	void deleteUsers( List<User> users );
	User findUserByUsername( String userName );
}
