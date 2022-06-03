package com.clarus.cms.vo;

import java.util.ArrayList;
import java.util.List;

public class AnimationImages {

	private Integer preferedHeight;
	
	
	List<Image> images = new ArrayList<Image>();

	public List<Image> getImages() {
		return images;
	}

	public void setImages(List<Image> images) {
		this.images = images;
	}

	public Integer getPreferedHeight() {
		return preferedHeight;
	}

	public void setPreferedHeight(Integer preferedHeight) {
		this.preferedHeight = preferedHeight;
	}
	
	public Integer getSize(){
		return images.size();
	}

		
}
