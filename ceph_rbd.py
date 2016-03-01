import rados


class RadosClient(object):

    def __init__(self, conf_file, keyring_key, ceph_pool_names):

        try:
            self.the_cluster = rados.Rados(conffile=conf_file,conf=keyring_key)
            print "\nlibrados version: " + str(self.the_cluster.version())
            print "Will attempt to connect to: " + str(self.the_cluster.conf_get('mon initial members'))
            self.the_cluster.connect()
            print "Connected to cluster:" + str(self.the_cluster.get_cluster_stats())

            self.pool = dict()
            for p in ceph_pool_names:
                self._get_pool_client(p)
        except Exception as e:
            print e.message
            raise RuntimeError("Failed connect to cluster")

    def _get_pool_client(self, pool_name):
        try:
            ioctx = self.the_cluster.open_ioctx(pool_name)
            self.pool.update({pool_name: ioctx})
        except Exception:
            raise RuntimeError("Unable to connect to pool")

    def get_ioctx(self, pool_name):
        return self.pool[pool_name]






