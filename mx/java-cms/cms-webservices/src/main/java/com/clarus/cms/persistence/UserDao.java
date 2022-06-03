package com.clarus.cms.persistence;

import java.util.List;

import com.clarus.cms.vo.model.User;

public interface UserDao {

	User findUserByCredentials( String userName, String password );
	List<User> findUsers();
	User findUserById( Integer id );
	User saveOrUpdateUser( User user );
	void deleteUsers( List<User> users  );
	User findUserByUsername( String userName );

}
