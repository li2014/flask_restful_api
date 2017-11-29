## 基本的flask api 接口设计
## 适用于移动端访问token验证
## 整个框架用的是flask + sqlalchemy + redis


##变成数据
----------
1. 首先安装alembic
2. 然后在工程目录下初始化migration
   alembic init my_migration
3. 这时候编辑一下alembic.ini，这是alembic的配置文件，基本只要修改一处就可以了。
   sqlalchemy.url = mysql://root:a12345678@127.0.0.1:3306/blog01?charset=utf8


## 一般的移动注册api接口可以分为3步
1. 提交电话号码，发送短信验证，
2. 验证短信
3. 密码提交，
4. 基本资料提交

看到上面register的4个步骤没有，这边要注意的是具体方法：

1. 步骤1：提交手机号码，验证。这个很基础，就不用说了，重要的是，发送过短信之后，要把短信验证码存在redis里面，以便下一个接口调用；其次，这个存储过程，一定要用pipeline，还要设置一个超时删除。想一想，假设你的程序在注册的过程中，崩掉，或者你中断程序，最起码不要影响其他程序，如果没有超时值，会产生很多的垃圾值，并且你还很难注意到。

2. 步骤2：从redis里找到之前存储的验证码，对比，成功就进入下一步。这边，我还设置了一个is_validate值，最主要是防止客户端同事在这步会出错，或者其他知道这个接口的人，直接用脚本访问后面的接口，这样会出现未知的错误。

3. 步骤3：验证一下密码是否符合要求，然后看一下上一步设置的is_validate是否存在，上面说了，防止恶意用户直接访问下面的接口，然后保存password到一个redis的hash值。这边主要为了方便客户端同事，不然下一个接口还要重新上传password值，客户端同事一定会恼火的。

4. 步骤4：提交基本资料，然后保存。这边最重要的是，不管注册成功失败，自己注意把redis里面的值清理干净。看看我上面的接口，所有这些临时注册值，都设置了一个超时值，超过时间，就清理掉。

   整个过程就完成了，可以去验证一下结果了。(其实这里还有缺陷，假设在第二步，我知道你这个接口，写个小脚本，暴力破解你的验证码，很快就能拿到的。这边可以做个小改动，在redis里面加一个值，访问一次，则添加1，超过一定次数，就返回错误代码。很简单，这边就不深入了)


##配置文件config
----------------

  如果哪天前端服务器的密码被别人知道了，或者网站有重大漏洞，被别人看到config.py文件，他岂不是知道所有数据库和redis的信息？那怎么做呢？其实也很简单，直接引用config.pyc文件即可，上传正式服务器的时候，把config.py文件给移除出去。


[博客地址](http://www.cnblogs.com/yueerwanwan0204/category/806842.html)

- flask开发restful api系列(8)-再谈项目结构
- flask开发restful api系列(7)-蓝图bulepoint管理api版本
- flask开发restful api系列(6)-整理配置到config
- flask开发restful api系列(5)-短信验证码
- flask开发restful api系列(4)--七牛图片服务
- flask开发restful api系列(3)--利用alembic进行数据库更改
- flask开发restful api系列(2)
- flask开发restful api系列(1)