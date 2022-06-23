package com.clarus.cms.util;

import java.util.Comparator;

import com.clarus.cms.vo.TreeNodeContentTypeDisplay;

public class ComparatorContentTypeDisplayTreeNode implements Comparator<TreeNodeContentTypeDisplay>{
	public int compare(TreeNodeContentTypeDisplay ct1, TreeNodeContentTypeDisplay ct2) {
		return ct1.getContentTypeDisplay().getDisplayOrder() - ct2.getContentTypeDisplay().getDisplayOrder();
	}
}

	