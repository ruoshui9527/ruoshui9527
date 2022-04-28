import paramiko
import datetime
import time
# pip install paramiko -i https://mirrors.aliyun.com/pypi/simple/
# ssh-keygen; ssh-copy-id
# python3 name.py

def sftp():
    try:
        print('upload jar begin -----------')
        tran = paramiko.Transport((ip,port))
        tran.connect(username=name,pkey=private)
        sftp = paramiko.SFTPClient.from_transport(tran)
        sftp.put(local_path + '/web.jar',ftp_path + '/web.jar')
        sftp.put(local_path + '/report.jar',ftp_path + '/report.jar')
        tran.close()
        print('upload jar finish-------')
    except:
        tran.close()

def ssh(cmdList):
    try:
        print('join ssh ----------')
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=ip,username=name,port=port,pkey=private)
        channel = ssh.invoke_shell()
        if root =='y':
           print('no root ----------------')
           channel.send('export LANG=C')
           channel.send('\n')
           channel.send('su -')
           channel.send('\n')
           buff = ''
           while not buff.endswith('Password: '):
               print('begin change root -----------')
               resp = channel.recv(9999)
               buff += resp.decode('utf-8')

           channel.send(root_pwd)
           channel.send('\n')
           buff = ''
           while not buff.endswith('# '):
               print('end change root ------------')
               resp = channel.recv(9999)
               buff += resp.decode('utf-8')
               print('提示符号----' + buff)
        print('join for cmdList----------------')
        for cmd in cmdList:
            channel.send(cmd)
            channel.send('\n')
            print('cmd------------' + cmd)
            buff = ''
            while not buff.endswith('# '):
                resp = channel.recv(9999)
                buff += resp.decode('utf-8')
                print(buff)

        print(buff)
        ssh.close()
    except:
        ssh.close()



if __name__ == '__main__':
    private = paramiko.RSAKey.from_private_key_file('/home/ps/.ssh/id_rsa')
    timestamp=datetime.datetime.strftime(datetime.datetime.now(),'%Y%m%d%H%M%S')
    from ip import pool

    for host in pool:
        ip = host.get("host")
        root_pwd = host.get("root_pwd")
        port = int(host.get("port") if ('port' in host) else "22")
        name = host.get("name") if ('name' in host) else "ps"
        local_path = host.get("local_path") if ('local_path' in host) else "/home/ps/update"
        update_path = host.get("update_path")
        root = host.get("is_root") if ('is_root' in host) else "n"

        if name == 'ps':
            ftp_path = '/home/ps'
        else:
            ftp_path = host.get("path")

        sftp()

        cmdList = [
            'cd ' + update_path,
            'mv web/app.jar web/bak/app.jar-' + timestamp,
            'mv report/app.jar report/bak/app.jar-' + timestamp,
            'cp ' + ftp_path + '/web.jar web/app.jar' ,
            'cp ' + ftp_path + '/report.jar report/app.jar' ,
            'docker-compose restart *; docker-compose restart nginx'
            ]
        ssh(cmdList)
