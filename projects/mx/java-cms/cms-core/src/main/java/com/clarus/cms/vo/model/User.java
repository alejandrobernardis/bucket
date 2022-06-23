package com.clarus.cms.vo.model;

import java.io.Serializable;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.EnumType;
import javax.persistence.Enumerated;
import javax.persistence.GeneratedValue;
import javax.persistence.GenerationType;
import javax.persistence.Id;
import javax.persistence.Table;

import org.hibernate.validator.Length;
import org.hibernate.validator.NotEmpty;
import org.hibernate.validator.NotNull;
import org.hibernate.validator.Pattern;

import com.clarus.cms.model.catalog.Role;

@Entity
@Table(name="USERS")
public class User implements Serializable {


	private static final long serialVersionUID = 1L;
	
	private Integer idUser;
	private String username;
	private String password;
	private String firstName;
	private String secondaryLastName;
	private String primaryLastName;
	private String email;
	private Role role;
	private Boolean active;
	
	@Id @Column(name ="ID_USER") @GeneratedValue(strategy=GenerationType.IDENTITY)
	public Integer getIdUser() {
		return idUser;
	}
	public void setIdUser(Integer idUser) {
		this.idUser = idUser;
	}

	@NotEmpty
	@Length(min=4,max=45)
	@Column(name ="USERNAME", nullable=false, length=45, unique=true)
	public String getUsername() {
		return username;
	}
	public void setUsername(String username) {
		this.username = username;
	}
	
	@NotEmpty
	@Length(min=6,max=45)
	@Column(name ="PASSWORD", nullable=false, length=45)
	public String getPassword() {
		return password;
	}
	public void setPassword(String password) {
		this.password = password;
	}
	
	@NotEmpty
	@Length(min=1,max=160)
	@Column(name ="FIRST_NAME", nullable=false, length=160)
	public String getFirstName() {
		return firstName;
	}
	public void setFirstName(String firstName) {
		this.firstName = firstName;
	}
	

	@Length(min=0,max=80)
	@Column(name ="SECONDARY_LAST_NAME", nullable=true, length=80)
	public String getSecondaryLastName() {
		return secondaryLastName;
	}
	public void setSecondaryLastName(String secondaryLastName) {
		this.secondaryLastName = secondaryLastName;
	}
	
	@NotEmpty
	@Length(min=1,max=80)
	@Column(name ="PRIMARY_LAST_NAME", nullable=false, length=80)
	public String getPrimaryLastName() {
		return primaryLastName;
	}
	public void setPrimaryLastName(String primaryLastName) {
		this.primaryLastName = primaryLastName;
	}
	
	@Pattern(regex="[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*@(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?")
	@NotEmpty
	@Length(min=1,max=80)
	@Column(name ="EMAIL", nullable=false, length=80)
	public String getEmail() {
		return email;
	}
	public void setEmail(String email) {
		this.email = email;
	}
	
	@NotNull
	@Enumerated(EnumType.STRING) @Column(name ="ROLE", nullable=false, length=10)
	public Role getRole() {
		return role;
	}
	public void setRole(Role role) {
		this.role = role;
	}
	
	@NotNull
	@Column(name ="ACTIVE", nullable=false)
	public Boolean getActive() {
		return active;
	}
	public void setActive(Boolean active) {
		this.active = active;
	}
	
	public void clean( ){
		this.setFirstName(null);
		this.setIdUser(null);
		this.setPrimaryLastName(null);
		this.setSecondaryLastName(null);
		this.setPassword(null);
		this.setUsername(null);
		this.setEmail(null);
		this.setRole(null);
		this.setActive(null);
	}
	
	public void init( User user ){
		this.setFirstName(user.getFirstName());
		this.setIdUser(user.getIdUser());
		this.setPrimaryLastName(user.getPrimaryLastName());
		this.setSecondaryLastName(user.getSecondaryLastName());
		this.setPassword(user.getPassword());
		this.setUsername(user.getUsername());
		this.setEmail(user.getEmail());
		this.setRole(user.getRole());
		this.setActive(user.getActive());
	}
	
	
	
	@Override
	public String toString() {
		StringBuilder builder = new StringBuilder();
		builder.append("User [");
		builder.append("idUser=");
		builder.append(idUser);
		builder.append(", username=");
		builder.append(username);
		builder.append(", password=");
		builder.append("******");		
		builder.append(", firstName=");
		builder.append(firstName);
		builder.append(", primaryLastName=");
		builder.append(primaryLastName);
		builder.append(", secondaryLastName=");
		builder.append(secondaryLastName);
		builder.append(", email=");
		builder.append(email);
		builder.append(", role=");
		builder.append(role);
		builder.append(", active=");
		builder.append(active);
		builder.append("]");
		return builder.toString();
	}
	
	
}

