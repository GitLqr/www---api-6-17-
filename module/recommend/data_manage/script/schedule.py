import time, os, sys, datetime

def TIMEOUT_COMMAND(command, timeout):
    import subprocess, datetime, os, time, signal
    cmd = command.split(" ")
    start = datetime.datetime.now()
    process = subprocess.Popen(cmd, stdout=sys.stdout, stderr=sys.stderr)
    while process.poll() is None:
        time.sleep(10)
        now = datetime.datetime.now()
        if (now - start).seconds > timeout:
            os.kill(process.pid, signal.SIGKILL)
            os.waitpid(-1, os.WNOHANG)
            print 'run timeout ... '
            return False
    return True

def schedule(cmd, sleep_time, timeout):
    while True:
        start_time = datetime.datetime.now()
        print 'schedule start time:' , start_time
        if timeout > 0:
            TIMEOUT_COMMAND(cmd, timeout)
        else:
            os.system(cmd)
        end_time = datetime.datetime.now()
        print 'schedule end time:' , end_time
        run_time = (end_time - start_time).seconds
        if run_time < sleep_time:
            time.sleep(sleep_time - run_time)
        else:
            print 'warn: run time too long , run time : %s(s), sleep time: %s(s)' % (run_time, sleep_time)

if __name__ == '__main__':
    if len(sys.argv) < 4:
        print 'schedule input error'
        sys.exit()
    cmd = ''
    for i in range(1, len(sys.argv) - 2):
        cmd += ' ' + sys.argv[i]
    sleep_time = int(sys.argv[-2])
    time_out = int(sys.argv[-1])
    schedule(cmd, sleep_time, time_out)
