package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Lob;
import javax.persistence.Table;


@Entity
@Table(name="ANIMATIONS")
public class Animation implements Serializable {

	private static final long serialVersionUID = 1L;
	private Integer idAnimation;
	private Integer idContent;
	private Integer order;
	private String extension;
	private byte[] data;
	
	public void init( Animation animation ){
		this.idAnimation = animation.idAnimation;
		this.idContent = animation.idContent;
		this.order = animation.order;
		this.extension = animation.extension;
		this.data = animation.data;
	}
	


	@Id @Column(name ="ID_ANIMATION") @GeneratedValue(strategy=GenerationType.IDENTITY)
	public Integer getIdAnimation() {
		return idAnimation;
	}
	public void setIdAnimation(Integer idAnimation) {
		this.idAnimation = idAnimation;
	}
	
	@Column(name ="ID_CONTENT", nullable=false)
	public Integer getIdContent() {
		return idContent;
	}
	public void setIdContent(Integer idContent) {
		this.idContent = idContent;
	}
	
	@Column(name ="DISPLAY_ORDER", nullable=false)
	public Integer getOrder() {
		return order;
	}
	public void setOrder(Integer order) {
		this.order = order;
	}
	
	@Column(name ="EXTENSION", nullable=false)
	public String getExtension() {
		return extension;
	}
	public void setExtension(String extension) {
		this.extension = extension;
	}
	
	@Column(name ="DATA", nullable=false)
	@Lob
	public byte[] getData() {
		return data;
	}
	public void setData(byte[] data) {
		this.data = data;
	}
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("Animation [extension=");
		builder.append(extension);
		builder.append(", idAnimation=");
		builder.append(idAnimation);
		builder.append(", idContent=");
		builder.append(idContent);
		builder.append(", order=");
		builder.append(order);
		builder.append("]");
		return builder.toString();
	}

		
}
