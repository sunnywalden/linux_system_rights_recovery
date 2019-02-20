# filesystem_rights_recovery_tools

## 方案
### 方案简述
本项目通过ACL快速恢复centos 7文件系统权限。


## Installation

### dependency

requires [python] v2.7+ to run.

Install the dependencies and devDependencies and clone the project.

```
pip install -r requirements.txt

```


### 配置文件管理
 

#### 配置文件路径
config/config.ini

#### 配置文件说明

paths为需要修改权限的路径的列表，默认省略‘/’。del_paths为需要删除的文件与路径列表，同样默认省略'/'。regex为需要忽略的/proc路径下文件的正则匹配表达式。

```

[filesystem]
paths = [
        'var', 'usr', 'sys', 'srv', 'shell',
        'sbin', 'run', 'root', 'resource', 'opt',
        'mnt', 'media', 'lib64', 'lib', 'home',
        'etc', 'dev', 'data', 'boot', 'bin',
        'proc'
        ]
del_paths = [
        'log_path',
        'pid_path',
        'collector_textfile_directory',
        '{{',
        '}}',
        'node_exporter',
        'basic_metrics.prom'
        ]

regex = r'\d+'

```
 


### 权限备份
  
 进入main路径，运行filesystem_recovery_by_acl.py，指定方法参数为‘backup’。
 
 ```
 
 cd main
 
 python2 filesystem_recovery_by_acl.py backup 
 
```

### 权限恢复
  
  进入main路径，运行filesystem_recovery_by_acl.py，指定方法参数为‘restore’。
 
 ```
 
 cd main
 
 python2 filesystem_recovery_by_acl.py restore 
 
 
```

### 文件删除
  
进入main路径，运行delete_files.py。
 
 ```
 
 cd main
 
 python2 delete_files.py
 
```

