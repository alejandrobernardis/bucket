package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.EmbeddedId;
import javax.persistence.Entity;
import javax.persistence.Table;

import org.hibernate.validator.Length;
import org.hibernate.validator.NotEmpty;


@Entity
@Table(name="CONTENT_TYPE_LABELS")
public class ContentTypeLabel implements Serializable {
	private static final long serialVersionUID = 1L;
	private ContentTypeLabelId id;
	private String label;
	
	@EmbeddedId 
	public ContentTypeLabelId getId() {
		return id;
	}
	public void setId(ContentTypeLabelId id) {
		this.id = id;
	}
	
	@Length(min=1, max=60)
	@NotEmpty
	@Column(name ="LABEL", nullable=false, length=60 )
	public String getLabel() {
		return label;
	}
	public void setLabel(String label) {
		this.label = label;
	}
	
	
	public void init( ContentTypeLabel label ){
		this.getId().init(label.getId());
		this.setLabel( label.getLabel() );
	}
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("ContentTypeLabel [id=");
		builder.append(id);
		builder.append(", label=");
		builder.append(label);
		builder.append("]");
		return builder.toString();
	}
	
	
	
	
	
	
}
