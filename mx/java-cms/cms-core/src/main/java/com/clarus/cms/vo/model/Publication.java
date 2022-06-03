package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;

import org.hibernate.validator.NotNull;

import com.clarus.cms.model.catalog.AcceptedFileExtension;

@Entity
@Table(name="PUBLICATIONS")
public class Publication implements Serializable {

	private static final long serialVersionUID = 3801440087424399174L;
	
	private Integer idPublication;
	private Integer idContentType;
	private AcceptedFileExtension imageType;
	private byte[] image = new byte[0];
	private Boolean active;
	private Integer order;
	
	
	@Id @Column(name="ID_PUBLICATION") @GeneratedValue(strategy=GenerationType.IDENTITY)
	public Integer getIdPublication() {
		return idPublication;
	}
	
	@NotNull
	@Column(name="ID_CONTENT_TYPE", nullable=false)
	public Integer getIdContentType() {
		return idContentType;
	}
	
	@NotNull
	@Enumerated(EnumType.STRING)
	@Column(name="IMAGE_TYPE", nullable=false, length=5)
	public AcceptedFileExtension getImageType() {
		return imageType;
	}
	
	@NotNull
	@Lob
	@Column(name="IMAGE", nullable=false)
	public byte[] getImage() {
		return image;
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
	
	
	public void setIdPublication(Integer idPublication) {
		this.idPublication = idPublication;
	}
	public void setIdContentType(Integer idContentType) {
		this.idContentType = idContentType;
	}
	public void setImageType(AcceptedFileExtension imageType) {
		this.imageType = imageType;
	}
	public void setImage(byte[] image) {
		this.image = image;
	}
	public void setActive(Boolean active) {
		this.active = active;
	}
	public void setOrder(Integer order) {
		this.order = order;
	}
	
	
}
