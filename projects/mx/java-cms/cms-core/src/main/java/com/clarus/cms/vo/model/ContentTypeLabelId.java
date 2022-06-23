package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Embeddable;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;

import org.hibernate.validator.NotNull;

import com.clarus.cms.model.catalog.Language;

@Embeddable
public class ContentTypeLabelId implements Serializable{
	
	private static final long serialVersionUID = 1L;
	private Integer idContentType;
	private Language language;
	
	
	public void init (ContentTypeLabelId id){
		this.setIdContentType(id.getIdContentType());
		this.setLanguage(id.getLanguage());
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
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("ContentTypeLabelId [idContentType=");
		builder.append(idContentType);
		builder.append(", language=");
		builder.append(language);
		builder.append("]");
		return builder.toString();
	}
	
	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result
				+ ((idContentType == null) ? 0 : idContentType.hashCode());
		result = prime * result
				+ ((language == null) ? 0 : language.hashCode());
		return result;
	}
	
	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		ContentTypeLabelId other = (ContentTypeLabelId) obj;
		if (idContentType == null) {
			if (other.idContentType != null)
				return false;
		} else if (!idContentType.equals(other.idContentType))
			return false;
		if (language == null) {
			if (other.language != null)
				return false;
		} else if (!language.equals(other.language))
			return false;
		return true;
	}
	
	
	
}
