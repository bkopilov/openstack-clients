import credentials


manager = credentials.ClientManager(username="admin",
                                   password="qum5net",
                                   auth_url="http://10.35.160.139:35357/v2.0",
                                   tenant_name="admin"
                                   )
keystone = manager.get_keystone_client()



nova = manager.get_nova_client()
#print nova.images.list()

glance = manager.get_glance_client()
for v in glance.images.list():
    print v


cinder = manager.get_cinder_client()
cinder.volumes.create(1)
print cinder.volumes.list()


neutron = manager.get_neutron_client()
print neutron.list_networks()
