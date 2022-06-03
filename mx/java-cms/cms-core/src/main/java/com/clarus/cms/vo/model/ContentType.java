package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.validator.Length;
import org.hibernate.validator.Min;
import org.hibernate.validator.NotEmpty;
import org.hibernate.validator.NotNull;


@Entity
@Table(name="CONTENT_TYPES")
public class ContentType implements Serializable {

	private static final long serialVersionUID = 1L;
	
	private Integer idContentType;
	private Integer idContentTypeParent;
	private String contentTypeName;
	private Integer order;
	private Boolean active;
	
	
	@Id @Column(name ="ID_CONTENT_TYPE") @GeneratedValue(strategy=GenerationType.IDENTITY)
	public Integer getIdContentType() {
		return idContentType;
	}
	public void setIdContentType(Integer idContentType) {
		this.idContentType = idContentType;
	}
	
	@NotEmpty
	@Length(min=1, max=50)
	@Column(name ="CONTENT_TYPE_NAME", nullable=false, length=50 ) 
	public String getContentTypeName() {
		return contentTypeName;
	}
	public void setContentTypeName(String contentTypeName) {
		this.contentTypeName = contentTypeName;
	}
	
	@NotNull
	@Column(name ="ACTIVE", nullable=false )
	public Boolean getActive() {
		return active;
	}
	public void setActive(Boolean active) {
		this.active = active;
	}
	
	
	@Column(name ="ID_CONTENT_TYPE_PARENT", nullable=true ) 
	public Integer getIdContentTypeParent() {
		return idContentTypeParent;
	}
	public void setIdContentTypeParent(Integer idContentTypeParent) {
		this.idContentTypeParent = idContentTypeParent;
	}
	
	@NotNull
	@Min(value=0)
	@Column(name ="DISPLAY_ORDER", nullable=false )
	public Integer getOrder() {
		return order;
	}
	public void setOrder(Integer order) {
		this.order = order;
	}
	
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("ContentType [active=");
		builder.append(active);
		builder.append(", contentTypeName=");
		builder.append(contentTypeName);
		builder.append(", idContentType=");
		builder.append(idContentType);
		builder.append(", idContentTypeParent=");
		builder.append(idContentTypeParent);
		builder.append(", order=");
		builder.append(order);
		builder.append("]");
		return builder.toString();
	}
	
	
		
	
}
