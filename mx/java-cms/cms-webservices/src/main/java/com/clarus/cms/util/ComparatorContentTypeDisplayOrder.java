package com.clarus.cms.util;

import java.util.Comparator;

import com.clarus.cms.vo.ContentTypeDisplay;

public class ComparatorContentTypeDisplayOrder implements Comparator<ContentTypeDisplay>{
	public int compare(ContentTypeDisplay ct1, ContentTypeDisplay ct2) {
		return ct1.getDisplayOrder() - ct2.getDisplayOrder();
	}
}

	