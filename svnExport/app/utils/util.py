# encoding:utf-8

import logging
import logging.config
from os import path
import paramiko
import csv
from StringIO import StringIO

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.ini')
logging.config.fileConfig(log_file_path)

# used to write logs
# util.WriteLog('infoLogger').warning('%s add user %s' % (session['username'], user_data['name']))
def WriteLog(logger_name):
    logger = logging.getLogger(logger_name)
    return logger


# used for paramiko ssh
def paramiko_command(host, cmd, username='op', password='xxxxx', port=22, timeout=10):
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=host,port=port,username=username,password=password,timeout=timeout)
        stdin,stdout,stderr = ssh.exec_command(cmd)
        cmd_result = stdout.read().strip('\n')
        ssh.close()
    except Exception,e:
        print e
        cmd_result = 1
    return cmd_result


# used for paramiko download a file
def paramiko_download(host, local_dir, remote_dir, filename, username='op', password='xxxxx', port=22, timeout=10):
    try:
        t = paramiko.Transport((host, port))
        t.connect(username=username, password=password)
        sftp = paramiko.SFTPClient.from_transport(t)
        # files = sftp.listdir(remote_dir)
        # for f in files:
        sftp.get(path.join(remote_dir,filename), path.join(local_dir, filename))
        t.close()
    except Exception,e:
        print e


# used for write csv
def write_csv(headers, rows): # rows = [ [], [], [] ]
    s = StringIO()
    s.write('\xEF\xBB\xBF')  # 写入BOM，解决EXCEL中文显示乱码
    csv_writer = csv.writer(s)
    csv_writer.writerow(headers)
    for row in rows:
        csv_writer.writerow(row)
    cxt = s.getvalue()
    s.close()
    return cxt


if __name__ == '__main__':
    WriteLog('infoLogger').info('this is info')