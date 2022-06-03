#!/bin/bash   

declare -a user=( carlos.anaya mairia.arnal pamela.baltazar alejandro.bernardis anabel.castro adriana.chavez mariana.delvalle paola.escalante luis.esparza fabiola.gomez amira.gomez sebastian.grassi jaime.kalb ana.larios mauricio.luna isabel.menendez monica.olivares carlos.oropeza andrea.ortega carlos.padilla ana.perez santiago.salido mariana.sanchez aldo.tabe esperanza.tapia regina.vergara );

declare -a pass=( 7ac2-12BEa8B7dB5 ff-12BEa8B7dB6 a-12BEa8B7dB7 a5aE-12BEa8B7dB8 EdfB-12BEa8B7dBa 678-12BEa8B7dBa 48E-12BEa8B7dBB 9-12BEa8B7dBc 757-12BEa8B7dBd 7-12BEa8B7dBE 8-14-12BEa8B7dBf 5E11-12BEa8B7dc faf-12BEa8B7dc1 ad82-12BEa8B7dc1 aa1-12BEa8B7dc2 9-12BEa8B7dc3 2-12BEa8B7dc4 d572-12BEa8B7dc5 4cE5-12BEa8B7dc6 6c-12BEa8B7dc8 ca92-12BEa8B7dc8 9-12BEa8B7dc9 3f66-12BEa8B7dca 8f9-12BEa8B7dcB B-9-12BEa8B7dcc B8Bc-12BEa8B7dcd );

echo `pwd`;

for (( i = 0 ; i < ${#user[@]}; i++ ))
do
	CFG_USERNAME_TEST=`egrep -i "^${user[$i]}:" /etc/passwd`;
	if [ "${#CFG_USERNAME_TEST}" -eq "0" ];then
		ftpuseradd -u ${user[$i]} -p ${pass[$i]}
		echo "Add: -u ${user[$i]} -p ${pass[$i]}" >> /data/scripts/source/ftp/create-users.log;
	else
		echo "Cancel: -u ${user[$i]} -p ${pass[$i]}" >> /data/scripts/source/ftp/create-users.log;
	fi
done