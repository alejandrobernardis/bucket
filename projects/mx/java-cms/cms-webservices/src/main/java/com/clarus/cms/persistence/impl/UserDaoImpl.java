package com.clarus.cms.persistence.impl;

import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hibernate.criterion.DetachedCriteria;
import org.hibernate.criterion.Restrictions;
import org.springframework.dao.support.DataAccessUtils;
import org.springframework.orm.hibernate3.support.HibernateDaoSupport;

import com.clarus.cms.persistence.UserDao;
import com.clarus.cms.vo.model.User;

public class UserDaoImpl extends HibernateDaoSupport implements UserDao {

	protected Log log = LogFactory.getLog(getClass());
	
	public User findUserByCredentials( String userName, String password ){
		DetachedCriteria criteria = DetachedCriteria.forClass(User.class);
		criteria.add(Restrictions.eq("username", userName));
		criteria.add(Restrictions.eq("password", password));
		criteria.add(Restrictions.eq("active", Boolean.TRUE));
		User user = (User)DataAccessUtils.uniqueResult(getHibernateTemplate().findByCriteria(criteria));
	    return user; 
	}
	
	@SuppressWarnings("unchecked")
	public List<User> findUsers(){
		DetachedCriteria criteria = DetachedCriteria.forClass(User.class);
		List<User> users = getHibernateTemplate().findByCriteria(criteria);
		return users;
	}
	
	public User findUserById( Integer id ){
		User user = (User)getHibernateTemplate().get(User.class, id);
		return user;
	}
	
	public User findUserByUsername( String userName ){
		DetachedCriteria criteria = DetachedCriteria.forClass(User.class);
		criteria.add(Restrictions.eq("username", userName));
		User user = (User)DataAccessUtils.uniqueResult(getHibernateTemplate().findByCriteria(criteria));
	    return user; 
	}
	
	
	public User saveOrUpdateUser( User user ){
		getHibernateTemplate().saveOrUpdate(user);
		return user;
	}
	
	
	public void deleteUsers( List<User> users  ){
		for ( User user : users ){
			getHibernateTemplate().delete(user);
		}
	}
	
	
	
}
