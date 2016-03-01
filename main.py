import credentials
import waiters

manager = credentials.ClientManager(username="admin",
                                   password="redhat",
                                   auth_url="http://192.168.100.235:35357/v2.0",
                                   tenant_name="admin"
                                   )
keystone = manager.get_keystone_client()


glance = manager.get_glance_client()
the_image_id = glance.images.create(name="test",
                                 visibility="public",
                                 container_format="bare",
                                 disk_format="qcow2")['id']

glance.images.upload(image_id=the_image_id, image_data=str("DDDDDDDDD"))
waiters.Waiter.wait_for_resource_status(function=glance.images.get,
                                        waiter_id=the_image_id,
                                        status='active',
                                        image_id=the_image_id,
                                        client=glance,
                                        message="glance_upload",
                                        )


cinder = manager.get_cinder_client()
volume_id = cinder.volumes.create("1").__dict__['id']
waiters.Waiter.wait_for_resource_status(function=cinder.volumes.list,
                                        waiter_id=volume_id,
                                        client=cinder,
                                        message="cinder_create",
                                        status="available")
"""
backup_id = cinder.backups.create(volume_id).__dict__['id']
waiters.Waiter.wait_for_resource_status(function=cinder.backups.list,
                                        waiter_id=backup_id,
                                        client=cinder,
                                        message="cinder_backup_create",
                                        status="available")

restore_id = cinder.restores.restore(backup_id=backup_id, volume_id=volume_id)
waiters.Waiter.wait_for_resource_status(function=cinder.volumes.list,
                                        waiter_id=restore_id,
                                        client=cinder,
                                        status="available")
"""

snapshot_id = cinder.volume_snapshots.create(volume_id).__dict__['id']
waiters.Waiter.wait_for_resource_status(function=cinder.volume_snapshots.list,
                                        waiter_id=snapshot_id,
                                        client=cinder,
                                        message="cinder_snapshot_create",
                                        status="available")


# nova
nova = manager.get_nova_client()
server_id = nova.servers.create(name="kuku",
                                image="c1337089-016c-4513-961b-92d1ec3fd527",
                                flavor="1",
                                nics=[{"net-id": "e6316a57-be66-4e81-b73c-79f93ef2d71f"}]).__dict__['id']
waiters.Waiter.wait_for_resource_status(function=nova.servers.list,
                                        waiter_id=server_id,
                                        client=nova,
                                        message="create instance",
                                        status="ACTIVE")




#d = c.__dict__
#for key in d.items():
#    print key
# cinder create returns an object
# print c

# cinder list = return an object
#for v in cinder.volumes.list():
#    print v.id


#neutron = manager.get_neutron_client()
# neutron list returns a dictionary
#n = neutron.list_networks()
#print n
