#!/usr/bin/env python3
# encoding: utf-8
import os
import sys
import atexit
import signal
import argparse


def cmd():
    doc = """
            this is system for analyze data from weather 
            written by qingluan
    """
    parser = argparse.ArgumentParser(usage=" how to use this ", description=doc)
    parser.add_argument("-d", "--daemon", default=None, help="daemon start operator\n[moniter, rpc, test]")
    parser.add_argument("--start", default=False, action="store_true")
    parser.add_argument("--stop", default=False, action="store_true")
    parser.add_argument("-a", "--auth-token", default="hello", help="rpc server authentication's token")
    parser.add_argument("-p", "--rpc-port", default=17000, help="rpc server port ")
    parser.add_argument("-H", "--host", default="localhost", help="rpc server bind ip")
    parser.add_argument("-c", "--rpc-client", default=False, action='store_true',help="rpc client to connect to remote rpc , this is interact mode")
    return parser.parse_args()


def daemonize(pidfile, *, stdin='/dev/null',
              stdout='/dev/null',
              stderr='/dev/null'):
    if os.path.exists(pidfile):
            raise RuntimeError('Already running')
    # First fork (detaches from parent)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #1 failed.')
    os.chdir('/')
    os.umask(0)
    os.setsid()
    # Second fork (relinquish,session leadership)
    try:
        if os.fork() > 0:
            raise SystemExit(0)
    except OSError as e:
        raise RuntimeError('fork #2 failed.')
    # Flush I/O buffers
    sys.stdout.flush()
    sys.stderr.flush()
    # Replace file descriptors for stdin, stdout, and stderr
    with open(stdin, 'rb', 0) as f:
        os.dup2(f.fileno(), sys.stdin.fileno())
    with open(stdout, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stdout.fileno())
    with open(stderr, 'ab', 0) as f:
        os.dup2(f.fileno(), sys.stderr.fileno())
        # Write the PID file
    with open(pidfile, 'w') as f:
        print(os.getpid(), file=f)
    # Arrange to have the PID file removed on exit/signal
    atexit.register(lambda: os.remove(pidfile))
    # Signal handler for termination(required)

    def sigterm_handler(signo, frame):
        raise SystemExit(1)
    signal.signal(signal.SIGTERM, sigterm_handler)


def test(): 
    import time
    sys.stdout.write('Daemon started with pid {}\n'.format(os.getpid()))
    while True:
        sys.stdout.write('Daemon Alive! {}\n'.format(time.ctime()))
        time.sleep(10)


def run(func):
    PID_F = os.path.join("/var/run/", func.__name__ + ".pid")
    LOG_F = os.path.join("/var/log/", func.__name__ + ".normal.log")
    ERROR_F = os.path.join("/var/log/", func.__name__ + ".error.log")
    try:
        print(func.__name__)
        daemonize(PID_F, stdout=LOG_F, stderr=ERROR_F)
    except RuntimeError as e:
        print(e, file=sys.stderr)
        raise SystemExit(1)
    func()


def stop(func):
    PID_F = os.path.join("/var/run/", func.__name__ + ".pid")
    LOG_F = os.path.join("/var/log/", func.__name__ + ".normal.log")
    for i in [PID_F]:
        if os.path.exists(i):
            with open(i) as f:
                os.kill(int(f.read()), signal.SIGTERM)
        else:
            print("Not running : ", i, file=sys.stderr)
    raise SystemExit(1)
    from time import asctime
    print(asctime() ," -- stop --", file=LOG_F)


def main():
    args = cmd()
    func = None
    if args.daemon == "monitor":
        func = monitor

    if args.daemon == "rpc":
        from rpc.run import RPC_server_start
        from functools import partial
        func = partial(RPC_server_start, args.host, args.rpc_port)
        func.__name__ = "rpc"

    if args.daemon == "test":
        func = test

    if args.start and func:
        run(func)
    elif args.stop and func:
        stop(func)
    else:
        print("you must choose a operator : start/stop", file=sys.stderr)

    if args.rpc_client:
        from rpc import get_client, interact
        interact(get_client((args.host, args.rpc_port), args.auth_token.encode()))

if __name__ == "__main__":
    main()
