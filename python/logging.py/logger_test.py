#import logging包
import logging
import time
  
#创建一个logger
logger=logging.getLogger('')
#设置logger的等级，大于等于这个等级的信息会被输出，其他会被忽略
logger.setLevel(logging.DEBUG)
  
#Handler是英文翻译为处理者，用于输出到不同的地方：Stream为控制台，File为文件
#以下创建的是输出到文件的handler，并把等级设为DEBUG
fh=logging.FileHandler('test.log')
fh.setLevel(logging.DEBUG)
  
#以下创建的是输出到控制台的handler，并把等级设为DEBUG
sh=logging.StreamHandler()
sh.setLevel(logging.DEBUG)
  
#下面指定了handler的信息输出格式，其中asctime,name,levelname，message都是logging的关键字
formatter=logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
sh.setFormatter(formatter)
  
#把Handler加入到logger中，可理解为给处理者在logger中安排了职位
logger.addHandler(fh)
logger.addHandler(sh)

#常和装饰器一起使用
def log(func):
    def wrapper(*args, **kwargs):
        start_time=time.time()
        logging.debug("start:{0}".format(func.__name__))
        ret=func(*args,**kwargs)
        end_time=time.time()
        logging.debug("end:{0},cost {1} seconds".format(func.__name__,end_time-start_time))
        return ret
    return wrapper
@log
def run_thing():
    print("do something here")
run_thing()