import credentials


manager = credentials.ClientManager(username="admin",
                                   password="qum5net",
                                   auth_url="http://10.35.160.139:35357/v2.0",
                                   tenant_name="admin"
                                   )
keystone = manager.get_keystone_client()
#print type(keystone.tenants.list())



nova = manager.get_nova_client()
#print nova.images.list()

glance = manager.get_glance_client()

#i = glance .images.create()
# image create returns a dictionary
#print i
# glance list =  returns a dictionary
#for v in glance.images.list():
#    print v['id']

cinder = manager.get_cinder_client()
c = cinder.volumes.create("1")
# cinder create returns an object
# print c

# cinder list = return an object
#for v in cinder.volumes.list():
#    print v.id


neutron = manager.get_neutron_client()
# neutron list returns a dictionary
n = neutron.list_networks()
print n
