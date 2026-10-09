---
title: "ssh&发送邮件"
created: 2026-10-09
updated: 2026-10-09
tags: [llm-wiki, migrated]
source: ["Input/rebuild_source_2026-10-09/01_工具/ssh&发送邮件.md"]
wiki_type: tools
topic: "数据科学工作流"
migrated_from: "01_工具/ssh&发送邮件.md"
review_status: structural
---

> 所属 Topic：[数据科学工作流](../../topics/%E6%95%B0%E6%8D%AE%E7%A7%91%E5%AD%A6%E5%B7%A5%E4%BD%9C%E6%B5%81.md) · 类型：工具

# python-ssh

http://www.paramiko.org

https://zhuanlan.zhihu.com/p/313718499

`paramiko`包

paramiko包含两个核心组件：SSHClient和SFTPClient。

- SSHClient的作用类似于Linux的ssh命令，是对SSH会话的封装，该类封装了传输(Transport)，通道(Channel)及SFTPClient建立的方法(open_sftp)，通常用于执行远程命令。
- SFTPClient的作用类似与Linux的sftp命令，是对SFTP客户端的封装，用以实现远程文件操作，如文件上传、下载、修改文件权限等操作。

```python
import paramiko

def get_ssh_connet(host, user_name, pass_word):
    # 实例化SSHClient
    client = paramiko.SSHClient()
    # 自动添加策略，保存服务器的主机名和密钥信息，如果不添加，那么不再本地know_hosts文件中记录的主机将无法连接
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    # 连接SSH服务端，以用户名和密码进行认证
    client.connect(hostname=host, port=22, username=user_name, password=pass_word)

    # 打开一个Channel并执行命令
    stdin, stdout, stderr = client.exec_command('df -h ')  # stdout 为正确输出，stderr为错误输出，同时是有1个变量有值
    # 打印执行结果
    print(stdout.read().decode('utf-8'))
    # 关闭SSHClient
    client.close()
```




# 阿里云发送邮件

https://www.cnblogs.com/ppzhang/p/10305517.html

