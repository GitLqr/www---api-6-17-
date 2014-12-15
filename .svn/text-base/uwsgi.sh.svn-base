#! /bin/sh

export LD_LIBRARY_PATH="./:./lib:/lib:/lib64:/usr/lib:/usr/lib64:/usr/local/lib:/usr/local/lib64"

function killByName()
{
    pids=""
    if (( $# >= 2 )); then
        ps aux | grep "$1" | grep -v "$2" | grep -v "grep" 
	pids=`ps aux | grep "$1" | grep -v "$2" | grep -v "grep"| awk '{print $2}'`
    else
        ps aux | grep "$1" | grep -v "grep" 
	pids=`ps aux | grep "$1" | grep -v "grep"| awk '{print $2}'`
    fi

    for pid in $pids ; do
        echo "kill -9 $pid"
	kill -9 $pid
	sleep 0.2
    done
}

if [ "$1"x == "stop"x ] ; then
   killByName uwsgi uwsgi.sh
   sleep 0.5
   ps aux | grep "uwsgi" | grep -v "uwsgi.sh" | grep -v "grep" 

elif [ "$1"x == "restart"x ] ; then
   killByName uwsgi uwsgi.sh
   sleep 1
   ./uwsgi -x ./uwsgi.xml -d ./uwsgi.log
   sleep 0.3
   tail -n 30 ./uwsgi.log

else
   ./uwsgi -x ./uwsgi.xml -d ./uwsgi.log
   sleep 0.3
   tail -n 30 ./uwsgi.log
fi

