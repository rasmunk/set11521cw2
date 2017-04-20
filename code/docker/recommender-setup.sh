#!/bin/bash

# TODO -> Parameterize -> cleanup repeats

#Initializes the containers and the network
## Move the mysql run out of initialize
function initialize()
{
    docker network create --subnet=172.18.0.0/16 recommender-network
    docker build -f Dockerfile.mysql \
        -t mysql .

    docker build -f Dockerfile.recommender-system \
        -t recommender-system .
}

## Starts the containers
function start()
{
    docker run -p 3306:3306 \
        --name mysql \
        --net recommender-network \
        --ip 172.18.0.2 \
        -e MYSQL_ROOT_PASSWORD=Passw0rd! \
        -e MYSQL_ROOT_HOST=172.18.0.2 \
        -d mysql
    docker exec /bin/sh -c 'mysql -u root -p Passw0rd! < /tmp/create_user.sql'

    docker run --name recommender-system \
        --net recommender-network \
        --ip 172.18.0.3 \
        --link mysql:mysql \
        -itd recommender-system
}

## Stops all running processes
function stop()
{
    docker rm -f $(docker ps -a -q)
}

## Removes all images and networks
function clean()
{
    docker rmi -f $(docker images -q)
    docker network rm $(docker network ls -q)
}

case "$1" in
    initialize)
        initialize
        ;;
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        stop
        start
        ;;
    clean)
        clean
        ;;    
    *)
        echo $"Usages: $0 {initialize|start|stop|restart|clean}"
        exit 1
esac
