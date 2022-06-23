package com.clarus.cms.persistence.impl;

import java.util.ArrayList;
import java.util.List;

import org.apache.commons.logging.Log;
import org.apache.commons.logging.LogFactory;
import org.hibernate.Criteria;
import org.hibernate.Hibernate;
import org.hibernate.Query;
import org.hibernate.SQLQuery;
import org.hibernate.Session;
import org.hibernate.criterion.DetachedCriteria;
import org.hibernate.criterion.Order;
import org.hibernate.criterion.Projections;
import org.hibernate.criterion.Restrictions;
import org.hibernate.transform.Transformers;
import org.springframework.dao.support.DataAccessUtils;
import org.springframework.orm.hibernate3.support.HibernateDaoSupport;

import com.clarus.cms.model.catalog.Language;
import com.clarus.cms.persistence.ContentDao;
import com.clarus.cms.vo.ContentTypeDisplay;
import com.clarus.cms.vo.model.Animation;
import com.clarus.cms.vo.model.Content;
import com.clarus.cms.vo.model.ContentType;
import com.clarus.cms.vo.model.ContentTypeLabel;
import com.clarus.cms.vo.model.Publication;
import com.clarus.cms.vo.model.PublicationPage;
import com.clarus.cms.vo.model.Store;

public class ContentDaoImpl extends HibernateDaoSupport implements ContentDao {

	protected Log log = LogFactory.getLog(this.getClass());
	
	
	public boolean hasContents( Integer idContentType ) throws Exception{
		Session session = null;
		try{
			session = getSession();
			Criteria criteria = session.createCriteria(Content.class);
			criteria.add(Restrictions.eq("idContentType", idContentType));
			criteria.setProjection(Projections.rowCount());
			Integer numContents = (Integer) criteria.uniqueResult();
			return numContents > 0;
		}catch (Exception e) {
			log.error("Error al buscar los contenidos ",e);
			throw e;
		}finally{
			if( session != null ){
				session.close();
			}
		}
	}
	
	@SuppressWarnings("unchecked")
	public ContentType getDefaultPublishedContentType( Language lang ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(ContentType.class);
			criteria.add(Restrictions.isNull("idContentTypeParent"));
			criteria.add(Restrictions.eq("active", true));
			criteria.addOrder(Order.asc("order"));
			List<ContentType> result = getHibernateTemplate().findByCriteria(criteria);
			if( result != null && result.size() > 0 ){
				for( ContentType ct : result ){
					Content c = getPublishedContent(ct.getIdContentType(), lang);
					if( c != null ){
						return ct;
					}
				}
				
			}
			return null;
		}catch (Exception e) {
			log.error("Error al buscar getDefaultPublishedContentType ",e);
			throw e;
		}
	}
	
	
	@SuppressWarnings("unchecked")
	public List<ContentTypeDisplay> getActiveContentTypes( Language language )throws Exception{
		Session session = getSession();
		StringBuffer sql = new StringBuffer();
		sql.append(" select ");
		sql.append(" t.id_content_type as idContentType, ");
		sql.append(" t.id_content_type_parent as idContentTypeParent, ");
		sql.append(" t.display_order as displayOrder, ");
		sql.append(" t.label as contentTypeLabel, ");
		sql.append(" count(c.id_content) as childNum ");
		sql.append(" from ( ");
		sql.append(" select ");
		sql.append(" ct.id_content_type, ");
		sql.append(" ct.id_content_type_parent, ");
		sql.append(" ct.display_order, ");
		sql.append(" cl.label ");
		sql.append(" from CONTENT_TYPES ct ");
		sql.append(" inner join ");
		sql.append(" CONTENT_TYPE_LABELS cl on ");
		sql.append(" ct.id_content_type = cl.id_content_type ");
		sql.append(" where ");
		sql.append(" ct.active = :active ");
		sql.append(" and cl.language = :language ");
		sql.append(" ) t left outer join ( ");
		sql.append(" select c.id_content_type, c.id_content ");
		sql.append(" from CONTENTS c ");
		sql.append(" where c.active = :active ");
		sql.append(" and c.language = :language) c on ");
		sql.append(" c.id_content_type = t.id_content_type ");
		sql.append(" group by  t.id_content_type, ");
		sql.append(" t.id_content_type_parent, ");
		sql.append(" t.display_order, ");
		sql.append(" t.label ");

		try{
			SQLQuery query = session.createSQLQuery(sql.toString());
			query.setInteger("active", 1);
			query.setString("language", language.getValue());
			
			query.addScalar("idContentType", Hibernate.INTEGER);
			query.addScalar("idContentTypeParent", Hibernate.INTEGER);
			query.addScalar("displayOrder", Hibernate.INTEGER);
			query.addScalar("contentTypeLabel", Hibernate.STRING);
			query.addScalar("childNum", Hibernate.INTEGER);
			
			query.setResultTransformer(Transformers.aliasToBean(ContentTypeDisplay.class));
			List<ContentTypeDisplay> ctdl = query.list();;
			return ctdl;
		}catch (Exception e) {
			log.error("Error al buscar getActiveContentTypes ",e);
			throw e;
		}finally{
			session.close();
		}
	}
	
	
	
	
	
	
	@SuppressWarnings("unchecked")
	public Content getPublishedContent(Integer contentType, Language language ) throws Exception{
		StringBuffer sql = new StringBuffer();
		sql.append(" select ");
		sql.append(" c.idContent as idContent, ");
		sql.append(" c.idContentType as idContentType, ");
		sql.append(" c.language as language, ");
		sql.append(" c.shortDesc as shortDesc,  ");
		sql.append(" c.animationType as animationType,  ");
		sql.append(" c.active as active, ");
		sql.append(" c.text as text, ");
		sql.append(" c.text2 as text2, ");
		sql.append(" c.metaKewords as metaKewords, ");
		sql.append(" c.metaDescription as metaDescription, ");
		sql.append(" c.pageTitle as pageTitle ");
		sql.append(" from ");
		sql.append(" Content c ");
		sql.append(" where ");
		sql.append(" c.language = :language ");
		sql.append(" and  c.idContentType = :contentType ");
		sql.append(" and c.active = :active ");
		
		Session session = null;
		try{
			session = getSession();
			
			Query query = session.createQuery(sql.toString());
			
			query.setParameter("language", language);
			query.setBoolean("active", Boolean.TRUE);
			query.setInteger("contentType", contentType);
			query.setResultTransformer(Transformers.aliasToBean(Content.class ));
			

			List<Content> result = query.list();
			if( result != null && result.size() > 0 ){
				return result.get(0);
			}
			return null;
		}catch (Exception e) {
			log.error("Error en getPublishedContent ",e);
			throw e;
		}finally{
			if ( session != null ){
				session.close();
			}
		}
	}
	
	
	
	@SuppressWarnings("unchecked")
	public List<Publication> getPublishedPublications(Integer contentType) throws Exception{
		StringBuffer sql = new StringBuffer();
		sql.append(" select ");
		sql.append(" p.idPublication as idPublication, ");
		sql.append(" p.idContentType as idContentType, ");
		sql.append(" p.imageType as imageType, ");
		sql.append(" p.active as active,  ");
		sql.append(" p.order as order ");
		sql.append(" from ");
		sql.append(" Publication p ");
		sql.append(" where ");
		sql.append(" p.idContentType = :contentType ");
		sql.append(" and p.active = :active ");
		sql.append(" order by p.order asc");
		
		Session session = null;
		try{
			session = getSession();
			
			Query query = session.createQuery(sql.toString());
			
			query.setBoolean("active", Boolean.TRUE);
			query.setInteger("contentType", contentType);
			query.setResultTransformer(Transformers.aliasToBean(Publication.class ));
			

			List<Publication> result = query.list();
			if( result == null || result.size() == 0 ){
				return null;
			}
			return result;
		}catch (Exception e) {
			log.error("Error en getPublishedPublications ",e);
			throw e;
		}finally{
			if ( session != null ){
				session.close();
			}
		}
	}
	
	
	@SuppressWarnings("unchecked")
	public List<PublicationPage> getPublishedPublicationPages(Integer publication) throws Exception{
		StringBuffer sql = new StringBuffer();
		sql.append(" select ");
		sql.append(" p.idPublicationPage as idPublicationPage, ");
		sql.append(" p.idPublication as idPublication, ");
		sql.append(" p.imageType as imageType, ");
		sql.append(" p.order as order ");
		sql.append(" from ");
		sql.append(" PublicationPage p ");
		sql.append(" where ");
		sql.append(" p.idPublication = :publication ");
		sql.append(" order by p.order asc");
		
		Session session = null;
		try{
			session = getSession();
			
			Query query = session.createQuery(sql.toString());
			
			query.setInteger("publication", publication);
			query.setResultTransformer(Transformers.aliasToBean(PublicationPage.class ));
			

			List<PublicationPage> result = query.list();
			if( result == null || result.size() == 0 ){
				return null;
			}
			return result;
		}catch (Exception e) {
			log.error("Error en getPublishedPublicationPages ",e);
			throw e;
		}finally{
			if ( session != null ){
				session.close();
			}
		}
	}
	
	
	@SuppressWarnings("unchecked")
	public Content getContent(Integer idContent ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(Content.class);
			criteria.add(Restrictions.eq("idContent", idContent));
			List <Content> result = getHibernateTemplate().findByCriteria(criteria);
			if( result != null && result.size() > 0 ){
				return result.get(0);
			}
			return null;
		}catch (Exception e) {
			log.error("Error en getContent " + idContent,e);
			throw e;
		}
	}
	
	
	
	@SuppressWarnings("unchecked")
	public List<ContentType> findAllContentTypes() throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(ContentType.class);
			criteria.addOrder(Order.asc("idContentTypeParent"));
			criteria.addOrder(Order.asc("idContentType"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findAllContentTypes " ,e);
			throw e;
		}
	}
	
	@SuppressWarnings("unchecked")
	public List<ContentType> findParentContentTypes() throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(ContentType.class);
			criteria.add(Restrictions.isNull("idContentTypeParent"));
			criteria.addOrder(Order.asc("contentTypeName"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findParentContentTypes " ,e);
			throw e;
		}
	}
	
	public ContentType saveOrUpdateContentType( ContentType contentType ) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(contentType);
			return contentType;
		}catch (Exception e) {
			log.error("Error en saveOrUpdateContentType "  + contentType ,e);
			throw e;
		}
	}
	
	public void deleteContentType( ContentType contentType  ) throws Exception{
		try{
			getHibernateTemplate().delete(contentType);
		}catch (Exception e) {
			log.error("Error en deleteContentType "  + contentType ,e);
			throw e;
		}
	}
	
	public ContentType findContentTypeByName( String name ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(ContentType.class);
			criteria.add(Restrictions.eq("contentTypeName", name));
			ContentType ct = (ContentType)DataAccessUtils.uniqueResult(getHibernateTemplate().findByCriteria(criteria));
			return ct;
		}catch (Exception e) {
			log.error("Error en findContentTypeByName "  + name ,e);
			throw e;
		}
		
	}
	
	@SuppressWarnings("unchecked")
	public List<ContentTypeLabel> findContentTypeLabelsForContent( Integer idConentType ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(ContentTypeLabel.class);
			criteria.add(Restrictions.eq("id.idContentType", idConentType));
			criteria.addOrder(Order.asc("id.language"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findContentTypeLabelsForContent "  + idConentType ,e);
			throw e;
		}
	}
	
	public ContentTypeLabel saveContentTypeLabel( ContentTypeLabel contentTypeLabel ) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(contentTypeLabel);
			return contentTypeLabel;
		}catch (Exception e) {
			log.error("Error en saveContentTypeLabel "  + contentTypeLabel ,e);
			throw e;
		}
	}
	
	public void deleteContentTypeLabel( ContentTypeLabel contentTypeLabel ) throws Exception{
		try{
			getHibernateTemplate().delete(contentTypeLabel);
		}catch (Exception e) {
			log.error("Error en deleteContentTypeLabel "  + contentTypeLabel ,e);
			throw e;
		}
	}
	
	
	@SuppressWarnings("unchecked")
	public List<Content> findContentsByContentType( Integer idContentType ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(Content.class);
			criteria.add(Restrictions.eq("idContentType", idContentType));
			criteria.addOrder(Order.asc("active"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findContentsByContentType"  + idContentType ,e);
			throw e;
		}
	}
	
	public Content findContentsById( Integer idContent ) throws Exception{
		try{
			return  (Content)getHibernateTemplate().get(Content.class, idContent);
		}catch (Exception e) {
			log.error("Error en findContentsById "  + idContent ,e);
			throw e;
		}
	}
	
	
	
	@SuppressWarnings("unchecked")
	public List<Animation> findContentAnimationsForWeb( Integer idContent ) throws Exception{
		StringBuffer sql = new StringBuffer();
		sql.append(" SELECT ");
		sql.append(" a.idAnimation as idAnimation, ");
		sql.append(" a.idContent as idContent, ");
		sql.append(" a.order as order, ");
		sql.append(" a.extension as extension  ");
		sql.append(" FROM ");
		sql.append(" Animation a ");
		sql.append(" where ");
		sql.append(" a.idContent = :idContent ");
		
		Session session = null;
		
		List<Animation> result = new ArrayList<Animation>();
		
		try{
			session = getSession();
			
			Query query = session.createQuery(sql.toString());
			query.setInteger("idContent", idContent);
			query.setResultTransformer(Transformers.aliasToBean(Animation.class ));
			result = query.list();
			return result;
		}catch (Exception e) {
			log.error("Error en findContentAnimationsForWeb "  + idContent ,e);
			throw e;
		}finally{
			if ( session != null ){
				session.close();
			}
		}
		
		
	}
	
	
	@SuppressWarnings("unchecked")
	public List<Animation> findContentAnimations( Integer idContent ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(Animation.class);
			criteria.add(Restrictions.eq("idContent", idContent));
			criteria.addOrder(Order.asc("order"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findContentAnimations "  + idContent ,e);
			throw e;
		}
	}
	
	public void deleteContentAnimation( Animation animation ) throws Exception{
		try{
			getHibernateTemplate().delete(animation);
		}catch (Exception e) {
			log.error("Error en deleteContentAnimation "  + animation ,e);
			throw e;
		}
	}
	
	public Animation saveContentAnimation( Animation animation ) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(animation);
			return animation;
		}catch (Exception e) {
			log.error("Error en saveContentAnimation "  + animation ,e);
			throw e;
		}
	}
	
	public Content saveContent( Content content ) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(content);
			return content;
		}catch (Exception e) {
			log.error("Error en saveContent "  + content ,e);
			throw e;
		}
	}
	
	public void deleteContent( Content content  ) throws Exception{
		try{
			getHibernateTemplate().delete(content);
		}catch (Exception e) {
			log.error("Error en deleteContent "  + content ,e);
			throw e;
		}
	}
	
	
	public void deleteContentAnimationsByContent( Integer contentId ) throws Exception{
		Session session = null;
		try{
			session = getSession();
			String sql = "delete Animation an where an.idContent = :contentId";
			Query query = session.createQuery(sql);
			query.setInteger("contentId", contentId);
			query.executeUpdate();
		}catch (Exception e) {
			log.error("Error en deleteContentAnimationsByContent "  + contentId ,e);
			throw e;
		}finally{
			if( session != null )
				session.close();
		}
	}
	
	public Animation findContentAnimation( Integer idAnimation ) throws Exception{
		try{
			return (Animation)getHibernateTemplate().get(Animation.class, idAnimation);
		}catch (Exception e) {
			log.error("Error en findContentAnimation "  + idAnimation ,e);
			throw e;
		}
	}
	
	
	
	@SuppressWarnings("unchecked")
	public List<Store> findStores( Integer idContentType ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(Store.class);
			criteria.add(Restrictions.eq("idContentType", idContentType));
			criteria.addOrder(Order.asc("order"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findStores "  + idContentType ,e);
			throw e;
		}
	}
	
	
	@SuppressWarnings("unchecked")
	public List<Store> getPublishedStores( Integer idContentType ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(Store.class);
			criteria.add(Restrictions.eq("idContentType", idContentType));
			criteria.add(Restrictions.eq("active", Boolean.TRUE));
			criteria.addOrder(Order.asc("order"));
			List<Store> result = getHibernateTemplate().findByCriteria(criteria);
			if( result == null || result.size() == 0 ){
				return null;
			}
			return result;
		}catch (Exception e) {
			log.error("Error en getPublishedStores "  + idContentType ,e);
			throw e;
		}
	}

	
	
	
	
	public Store saveStore(Store store) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(store);
			return store;
		}catch (Exception e) {
			log.error("Error en saveStore "  + store ,e);
			throw e;
		}
	}
	
	public Store findStore( Integer idStore ) throws Exception{
		try{
			return (Store)getHibernateTemplate().get(Store.class, idStore);
		}catch (Exception e) {
			log.error("Error en findStore "  + idStore ,e);
			throw e;
		}
	}
	
	public void deleteStore( Store store ) throws Exception{
		try{
			getHibernateTemplate().delete(store);
		}catch (Exception e) {
			log.error("Error en deleteStore "  + store ,e);
			throw e;
		}
	}
	
	
	public Publication findPublication( Integer idPublication ) throws Exception{
		try{
			return (Publication)getHibernateTemplate().get(Publication.class, idPublication);
		}catch (Exception e) {
			log.error("Error en findPublication "  + idPublication ,e);
			throw e;
		}
	}
	
	public void deletePublication( Publication publication ) throws Exception{
		try{
			getHibernateTemplate().delete(publication);
		}catch (Exception e) {
			log.error("Error en deletePublication "  + publication ,e);
			throw e;
		}
	}
	
	public Publication savePublication( Publication publication ) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(publication);
			return publication;
		}catch (Exception e) {
			log.error("Error en savePublication "  + publication ,e);
			throw e;
		}
	}
	
	@SuppressWarnings("unchecked")
	public List<Publication> findPublications( Integer idContentType ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(Publication.class);
			criteria.add(Restrictions.eq("idContentType", idContentType));
			criteria.addOrder(Order.asc("order"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findPublications "  + idContentType ,e);
			throw e;
		}
	}
	
	
	public PublicationPage findPublicationPage( Integer idPublicationPage ) throws Exception{
		try{
			return (PublicationPage)getHibernateTemplate().get(PublicationPage.class, idPublicationPage);
		}catch (Exception e) {
			log.error("Error en findPublicationPage "  + idPublicationPage ,e);
			throw e;
		}
	}
	
	public void deletePublicationPage( PublicationPage publicationPage ) throws Exception{
		try{
			getHibernateTemplate().delete(publicationPage);
		}catch (Exception e) {
			log.error("Error en deletePublicationPage "  + publicationPage ,e);
			throw e;
		}
	}
	
	public PublicationPage savePublicationPage( PublicationPage publicationPage ) throws Exception{
		try{
			getHibernateTemplate().saveOrUpdate(publicationPage);
			return publicationPage;
		}catch (Exception e) {
			log.error("Error en savePublicationPage "  + publicationPage ,e);
			throw e;
		}
	}
	
	@SuppressWarnings("unchecked")
	public List<PublicationPage> findPublicationPages( Integer idPublication ) throws Exception{
		try{
			DetachedCriteria criteria = DetachedCriteria.forClass(PublicationPage.class);
			criteria.add(Restrictions.eq("idPublication", idPublication));
			criteria.addOrder(Order.asc("order"));
			return getHibernateTemplate().findByCriteria(criteria);
		}catch (Exception e) {
			log.error("Error en findPublicationPages "  + idPublication ,e);
			throw e;
		}
	}
	
	
}

