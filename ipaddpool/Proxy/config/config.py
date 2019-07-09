class Config():
    # 连接地址
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:root@127.0.0.1:3306/pool'
    # 记录所有发到标准输出(stderr)的语句
    SQLALCHEMY_ECHO = True
    # 数据追踪
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    # 调试模式
    DEBUG = True
    SECRET_KEY = "ProxyPool"
    # 定时任务接口
    SCHEDULER_API_ENABLED = True
