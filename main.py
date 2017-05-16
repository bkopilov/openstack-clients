import credentials
import waiters

"""
import ceph_rbd
# name of pools to connect
# ceph_pools = ["yrabl-cinder", "yrabl-glance", "yrabl-nova"]
# keyring file
keyring_key = dict(keyring="ceph.client.admin.keyring")

# connect to cluster and initialize ioctx to pools
cluster = ceph_rbd.RadosClient(conf_file="ceph.conf",
                               keyring_key=keyring_key,
                               ceph_pool_names=ceph_pools)

rbd_client = cluster.get_rbd()
cinder_pool = cluster.get_ioctx("yrabl-cinder")
glance_pool = cluster.get_ioctx("yrabl-glance")
nova_pool = cluster.get_ioctx("yrabl-nova")

# example for RBD
print rbd_client.list(glance_pool)
# get pool info
#print cinder_pool.get_stats()
"""
manager = credentials.ClientManager(
    username="admin", password="qum5net",
    auth_url="http://192.168.100.230:5000/v2.0", project_name="admin")
keystone = manager.get_keystone_client()
# print keystone.users.list()
# print keystone.roles.list()

# nova
nova = manager.get_nova_client()
# print nova.servers.list()
# print nova.flavors.list()
server = nova.servers.create(name="kuku",
                             image="7bb61244-60b5-40db-bdd1-b9aca4cccbab",
                             flavor="1",
                             nics=[{
                                 "net-id":
                                     "d9663346-2739-4063-9e99-898e7dc072e1"}])
waiters.Waiter.wait_for_resource_status(function=nova.servers.list,
                                        waiter_id=server.__dict__['id'],
                                        client=nova,
                                        message="create instance",
                                        status="ACTIVE")


glance = manager.get_glance_client()
the_image_id = glance.images.create(name="test",
                                    visibility="public",
                                    container_format="bare",
                                    disk_format="qcow2")['id']

glance.images.upload(image_id=the_image_id, image_data=str("DDDDDDDDD"))
waiters.Waiter.wait_for_resource_status(function=glance.images.list,
                                        waiter_id=the_image_id,
                                        status='active',
                                        client=glance,
                                        message="glance_upload")


cinder = manager.get_cinder_client()
volume_id = cinder.volumes.create("1").__dict__['id']
waiters.Waiter.wait_for_resource_status(function=cinder.volumes.list,
                                        waiter_id=volume_id,
                                        client=cinder,
                                        message="cinder_create",
                                        status="available")

cinder.volumes.delete(volume=volume_id)
waiters.Waiter.wait_for_resource_deletion(function=cinder.volumes.list,
                                          waiter_id=volume_id,
                                          client=cinder,
                                          message="cinder_delete")

"""
backup_id = cinder.backups.create(volume_id).__dict__['id']
waiters.Waiter.wait_for_resource_status(function=cinder.backups.list,
                                        waiter_id=backup_id,
                                        client=cinder,
                                        message="cinder_backup_create",
                                        status="available")

restore_id = cinder.restores.restore(backup_id=backup_id,
                                     volume_id=volume_id)\
                                     .__dict__['volume_id']
waiters.Waiter.wait_for_resource_status(function=cinder.volumes.list,
                                        waiter_id=restore_id,
                                        client=cinder,
                                        status="available")


snapshot_id = cinder.volume_snapshots.create(volume_id).__dict__['id']
waiters.Waiter.wait_for_resource_status(function=cinder.volume_snapshots.list,
                                        waiter_id=snapshot_id,
                                        client=cinder,
                                        message="cinder_snapshot_create",
                                        status="available")


"""
