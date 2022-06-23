#!/bin/bash
ROOT_PATH=`pwd`/data/_dumps
mongo localhost:27017/c8 --eval 'printjson(db.dropDatabase())'
mongoimport --db c8 --collection devices --file ${ROOT_PATH}/devices.json
mongoimport --db c8 --collection profiles --file ${ROOT_PATH}/profiles.json
mongoimport --db c8 --collection activity.games --file ${ROOT_PATH}/activity.games.json
mongoimport --db c8 --collection activity.session --file ${ROOT_PATH}/activity.session.json
mongoimport --db c8 --collection activity.store --file ${ROOT_PATH}/activity.store.json
