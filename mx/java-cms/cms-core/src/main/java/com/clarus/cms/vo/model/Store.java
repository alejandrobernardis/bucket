package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.validator.NotEmpty;
import org.hibernate.validator.NotNull;

@Entity
@Table(name="STORES")
public class Store implements Serializable {
	private static final long serialVersionUID = 1L;
	
	
	private Integer idStore;
	private Integer idContentType;
	private Boolean active;
	private Integer order;
	private String address1;
	private String address2;
	private String name;
	private String mall;
	private String tels;
	
	@Id @Column(name="ID_STORE") @GeneratedValue(strategy=GenerationType.IDENTITY)
	public Integer getIdStore() {
		return idStore;
	}
	
	@NotNull
	@Column(name="ID_CONTENT_TYPE", nullable=false)
	public Integer getIdContentType() {
		return idContentType;
	}
	
	@NotNull
	@Column(name="ACTIVE", nullable=false)
	public Boolean getActive() {
		return active;
	}
	
	@NotNull
	@Column(name="DISPLAY_ORDER", nullable=false)
	public Integer getOrder() {
		return order;
	}
	
	@NotEmpty
	@Column(name="ADDRESS1", nullable=false, length=100)
	public String getAddress1() {
		return address1;
	}
	
	@Column(name="ADDRESS2", nullable=true, length=100)
	public String getAddress2() {
		return address2;
	}
	
	
	@NotEmpty
	@Column(name="NAME", nullable=false, length=45)
	public String getName() {
		return name;
	}
	
	@NotEmpty
	@Column(name="MALL", nullable=false, length=100)
	public String getMall() {
		return mall;
	}
	
	@NotEmpty
	@Column(name="TELS", nullable=false, length=60)
	public String getTels() {
		return tels;
	}
	
	
	public void setIdStore(Integer idStore) {
		this.idStore = idStore;
	}
	public void setIdContentType(Integer idContentType) {
		this.idContentType = idContentType;
	}
	public void setActive(Boolean active) {
		this.active = active;
	}
	public void setOrder(Integer order) {
		this.order = order;
	}
	public void setAddress1(String address1) {
		this.address1 = address1;
	}
	public void setAddress2(String address2) {
		this.address2 = address2;
	}
	public void setName(String name) {
		this.name = name;
	}
	public void setMall(String mall) {
		this.mall = mall;
	}
	public void setTels(String tels) {
		this.tels = tels;
	}

	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Store [active=");
		builder.append(active);
		builder.append(", address1=");
		builder.append(address1);
		builder.append(", address2=");
		builder.append(address2);
		builder.append(", idContentType=");
		builder.append(idContentType);
		builder.append(", idStore=");
		builder.append(idStore);
		builder.append(", mall=");
		builder.append(mall);
		builder.append(", name=");
		builder.append(name);
		builder.append(", order=");
		builder.append(order);
		builder.append(", tels=");
		builder.append(tels);
		builder.append("]");
		return builder.toString();
	}
	
	


}
