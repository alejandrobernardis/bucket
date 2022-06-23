package com.clarus.transport;

import java.io.Serializable;

public class Agent<T> implements Serializable{

	private static final long serialVersionUID = 1L;
	private Boolean selected;
	private String type;
	private T value;
	
	public Agent() {
	}
	
	public Agent( T value ){
		this.value=value;
	}
	
	public Agent( T value, String type ){
		this.value = value;
		this.type = type;
	}
	
	public Boolean getSelected() {
		return selected;
	}
	public void setSelected(Boolean selected) {
		this.selected = selected;
	}
	
	public T getValue() {
		return value;
	}
	public void setValue(T value) {
		this.value = value;
	}
	public String getType() {
		return type;
	}
	public void setType(String type) {
		this.type = type;
	}
	
	
}
