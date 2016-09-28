#!/usr/bin/env python3
import os
from subprocess import Popen ,PIPE
import pexpect
from .softtables import table
from .softtables import toptbale


def _shell_do(prefix,content,passwd=None):
    _content = " \"{}\" ".format(content)
    result = None
    res = 127
    if passwd:
        result = pexpect.spawn(prefix + _content,timeout=600)
        result.expect('password:')
        result.sendline(passwd+'\r')
        res = result.read().decode()
        if "not" in res.split():

            print("Err  ")
            return 1
        print("True ")
        return 0
        

    else:
        result = Popen(prefix + _content,stdout=PIPE,shell=True)
        res = result.wait()
        print (_content)
        out,err= result.communicate('qingluan\n')

        print(out)
#    result.stdout.readline()
    return res

def _shell_install(prefix,content,passwd=None):
    _content = " \"{}\" ".format(content)
    result = pexpect.spawn(prefix + _content,timeout=600)
    result.expect('password:')
    result.sendline(passwd)
    result.expect('y')
    result.sendline("yes")
    print(result.read().decode())


def _remote_copy(prefix,filename,path,passwd=None):
    _content = "scp {} {}  {}".format(prefix,filename,path)

    if passwd:
        result = pexpect.spawn(_content,timeout=600)
        result.expect('password:')
        result.sendline(passwd+"\r")
        res = result.readlines()
        print(res)
        for line in res:
            if b"not" in line.split():
                return 127
        return 0
    else:
        result = Popen(_content,stdout=PIPE,shell=True)
    return result.wait()




def checkout_soft(login_info,name,passwd=None):
    cmd = "{} -h ".format(name)

    user, ip,port = login_info
    ssh_cmd = "ssh -p {} {}@{}".format(port,user,ip)
    res = _shell_do(ssh_cmd,cmd,passwd)

    if res == 0: 
        return True 
    return False


def checkout_softs(login_info,names,passwd=None):
    return {name:checkout_soft(login_info,name,passwd) for name in names}


def top_install_soft(login_info,names,passwd=None):
    sys_version = checkout_softs(login_info,["apt-get","yum"],passwd)
    install_soft = "apt-get"
    for k in ["apt-get","yum"]:
        if sys_version[k]:
            install_soft = k

    user,ip,port = login_info
    unstall_softs = [toptbale[soft] for soft in names  ] 
    cmds = "{} install {}".format(install_soft," ".join(unstall_softs))
    ssh_cmd = "ssh -p {} {}@{} ".format(port,user,ip)
    res = _shell_install(ssh_cmd,cmds,passwd)
    return res



def normal_install_soft(login_info,softtables,passwd=None):
    cmds = " && ".join([table[soft] for soft in softtables ] )
    user,ip,port = login_info
    ssh_cmd = "ssh -p {} {}@{} ".format(port,user,ip)

    res = _shell_install(ssh_cmd,cmds,passwd)
    return res

def get_uninstall_softs(softs):
    uninstall = [ soft for soft in softs if not softs[soft] ]
    
    normal = [soft for soft in uninstall if soft in table]
    top  = list(set(uninstall) - set(normal))

    return [top,normal]

    
def copy_file(login_info,f,path,passwd=None):
    user,ip,port = login_info
    prefix = "-P  {}".format(port)
    path = " {}@{}:{} ".format(user,ip,path)
    
    return _remote_copy(prefix,f,path,passwd)

def run_shdowsocks(login_info,passwd=None):
    user,ip,port = login_info

    ssh_cmd = "ssh -p {} {}@{} ".format(port,user,ip)
    cmds = "ssserver -c ./default_config.json -d start "
    _shell_do(ssh_cmd,cmds,passwd)

def get_shadow_status(login_info,passwd=None):
    user,ip,port = login_info

    ssh_cmd = "ssh -p {} {}@{} ".format(port,user,ip)
    cmds = "ps aux | grep sss | egrep -v \"(grep|egrep)\""
    return _shell_do(ssh_cmd,cmds,passwd)
