#!/bin/bash
path=/Volumes/Development/Projects/eclipse/sh-kirika-clarus-server-scripts/source/virtualhost;
sed -e "s/@domain@/domain.com.ar/g" $path/virtualhost.conf > $path/test.txt.old;
sed -e "s/@path@/ar\/com\/domain/g" $path/test.txt.old > $path/test.txt;