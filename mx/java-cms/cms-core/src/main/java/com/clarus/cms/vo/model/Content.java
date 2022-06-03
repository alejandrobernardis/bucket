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

import org.hibernate.validator.Length;
import org.hibernate.validator.NotEmpty;
import org.hibernate.validator.NotNull;

import com.clarus.cms.model.catalog.AnimationType;
import com.clarus.cms.model.catalog.Language;

@Entity
@Table(name="CONTENTS")
public class Content implements Serializable {

	private static final long serialVersionUID = 1L;
	private Integer idContent;
	private Integer idContentType;
	private Language language;
	private String shortDesc;
	private AnimationType animationType;
	private Boolean active;
	private byte[] image;
	private String text;
	private String text2;
	private String metaKewords;
	private String metaDescription;
	private String pageTitle;
	
	
	
	public void init(Content content){
		this.idContent = content.idContent;
		this.idContentType = content.idContentType;
		this.language = content.language;
		this.shortDesc = content.shortDesc;
		this.animationType = content.animationType;
		this.active = content.active;
		this.image = content.image;
		this.text = content.text;
		this.text2 = content.text2;
		this.metaDescription = content.metaDescription;
		this.metaKewords = content.metaKewords;
		this.pageTitle = content.pageTitle;
	}
	
	
	


	@Id @Column(name ="ID_CONTENT") @GeneratedValue(strategy=GenerationType.IDENTITY)
	public Integer getIdContent() {
		return idContent;
	}
	
	public void setIdContent(Integer idContent) {
		this.idContent = idContent;
	}
	
	@NotNull
	@Column(name ="ID_CONTENT_TYPE", nullable=false)
	public Integer getIdContentType() {
		return idContentType;
	}
	public void setIdContentType(Integer idContentType) {
		this.idContentType = idContentType;
	}
	
	@NotNull
	@Enumerated(EnumType.STRING)
	@Column(name ="LANGUAGE", nullable=false, length=2)
	public Language getLanguage() {
		return language;
	}
	public void setLanguage(Language language) {
		this.language = language;
	}
	
	@NotNull
	@Enumerated(EnumType.STRING)
	@Column(name ="ANIMATION_TYPE", nullable=false, length=10)
	public AnimationType getAnimationType() {
		return animationType;
	}
	public void setAnimationType(AnimationType animationType) {
		this.animationType = animationType;
	}
	
	@NotNull
	@Column(name ="ACTIVE", nullable=false)
	public Boolean getActive() {
		return active;
	}
	public void setActive(Boolean active) {
		this.active = active;
	}
	
	
	@NotNull
	@Lob
	@Column(name="IMAGE", nullable=false)
	public byte[] getImage() {
		return image;
	}
	public void setImage(byte[] image) {
		this.image = image;
	}
	
	@NotEmpty
	@Column(name="TEXT", nullable=false, length=2000)
	public String getText() {
		return text;
	}
	public void setText(String text) {
		this.text = text;
	}
	
	@Column(name="TEXT2", nullable=true, length=3000)
	public String getText2() {
		return text2;
	}
	public void setText2(String text2) {
		this.text2 = text2;
	}
	
	@NotEmpty
	@Length(min=1,max=255)
	@Column(name="SHORT_DESC", nullable=false, length=255)
	public String getShortDesc() {
		return shortDesc;
	}
	public void setShortDesc(String shortDesc) {
		this.shortDesc = shortDesc;
	}
	
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Content [animationType=");
		builder.append(animationType);
		builder.append(", idContent=");
		builder.append(idContent);
		builder.append(", idContentType=");
		builder.append(idContentType);
		builder.append(", language=");
		builder.append(language);
		builder.append(", active=");
		builder.append(active);
		builder.append(", text=");
		builder.append(text);
		builder.append("]");
		return builder.toString();
	}


	@NotEmpty
	@Length(min=1,max=500)
	@Column(name ="META_KEYWORDS", nullable=false, length=500)
	public String getMetaKewords() {
		return metaKewords;
	}

	public void setMetaKewords(String metaKewords) {
		this.metaKewords = metaKewords;
	}
	@NotEmpty
	@Length(min=1,max=250)
	@Column(name ="META_DESCRIPTION", nullable=false, length=250)
	public String getMetaDescription() {
		return metaDescription;
	}

	public void setMetaDescription(String metaDescription) {
		this.metaDescription = metaDescription;
	}
	
	@NotEmpty
	@Length(min=1,max=50)
	@Column(name ="PAGE_TITLE", nullable=false, length=50)
	public String getPageTitle() {
		return pageTitle;
	}

	public void setPageTitle(String pageTitle) {
		this.pageTitle = pageTitle;
	}

}
