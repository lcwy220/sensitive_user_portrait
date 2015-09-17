from redis import StrictRedis
from rediscluster import RedisCluster

if __name__ == '__main__':
    """
    for i in [94, 95, 96]:
        for j in [7380]:
            startup_nodes = [{"host": '219.224.135.%s'%i, "port": '%s'%j}]
            print startup_nodes
            weibo_redis = RedisCluster(startup_nodes = startup_nodes)

            weibo_redis.flushall()
    print "finish flushing!"
    """
    startup_nodes = [{"host": '219.224.135.96', "port": '7380'}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    startup_nodes = [{"host": '219.224.135.94', "port": '7379'}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    startup_nodes = [{"host": '219.224.135.95', "port": '7379'}]
    weibo_redis = RedisCluster(startup_nodes = startup_nodes)
    weibo_redis.flushall()

    r = StrictRedis(host="219.224.135.97", port="7380")
    r.flushall()

    print "ok"
    """
    startup_nodes = [{"host": '219.224.135.94', "port": '7379'}]
    r =  RedisCluster(startup_nodes = startup_nodes)
    r.flushall()
    """
