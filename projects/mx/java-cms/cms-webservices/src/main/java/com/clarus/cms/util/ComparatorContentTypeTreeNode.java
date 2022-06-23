package com.clarus.cms.util;

import java.util.Comparator;

import com.clarus.cms.vo.TreeNodeContentType;

public class ComparatorContentTypeTreeNode implements Comparator<TreeNodeContentType>{
	public int compare(TreeNodeContentType ct1, TreeNodeContentType ct2) {
		return ct1.getContentType().getOrder() - ct2.getContentType().getOrder();
	}
}

	