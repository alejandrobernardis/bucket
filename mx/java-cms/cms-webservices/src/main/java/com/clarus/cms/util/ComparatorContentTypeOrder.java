package com.clarus.cms.util;

import java.util.Comparator;

import com.clarus.cms.vo.model.ContentType;

public class ComparatorContentTypeOrder implements Comparator<ContentType>{
	public int compare(ContentType ct1, ContentType ct2) {
		return ct1.getOrder() - ct2.getOrder();
	}
}

	