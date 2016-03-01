import os
import keystoneclient.v2_0.client as ksclient
import novaclient.client as nova
import glanceclient.v2.client as glance
import cinderclient.v2.client as cinder
import neutronclient.v2_0.client as neutron


class ClientManager(object):

    CWD = os.getcwd()

    def __init__(self, username, password, auth_url, tenant_name):
        self.creds = {'username': username,
                      'password': password,
                      'auth_url': auth_url,
                      'tenant_name': tenant_name
                      }
        self._get_nova_creds()

    def _get_nova_creds(self):
        self.nova_creds = {"username": self.creds['username'],
                           "api_key": self.creds['password'],
                           "auth_url": self.creds['auth_url'],
                           "project_id": self.creds['tenant_name']
                           }

    def _get_keystone_token(self):
        keystone = ksclient.Client(**self.creds)
        return keystone.auth_token

    def get_keystone_client(self):
        """
        keystone objects keystone.
        keystone_client.endpoints
        keystone_client.extensions
        keystone_client.roles
        keystone_client.services
        keystone_client.tokens
        keystone_client.users
        keystone_client.tenants
        keystone_client.ec2
        """
        token = self._get_keystone_token()
        keystone_client = ksclient.Client(endpoint=self.creds['auth_url'],
                                          token=token)
        return keystone_client

    def get_nova_client(self):
        """
        nova_client.flavors
        nova_client.flavor_access
        nova_client.images
        nova_client.limits
        nova_client.servers
        nova_client.versions
        nova_client.api_version
        nova_client.agents
        nova_client.dns_domains
        nova_client.dns_entries
        nova_client.cloudpipe
        nova_client.certs
        nova_client.floating_ips
        nova_client.floating_ip_pools
        nova_client.fping
        nova_client.volumes
        nova_client.volume_snapshots
        nova_client.volume_types
        nova_client.keypairs
        nova_client.networks
        nova_client.quota_classes
        nova_client.quotas
        nova_client.security_groups
        nova_client.security_group_rules
        nova_client.security_group_default_rules
        nova_client.usage
        nova_client.virtual_interfaces
        nova_client.aggregates
        nova_client.hosts
        nova_client.hypervisors
        nova_client.hypervisor_stats
        nova_client.services =
        nova_client.fixed_ips
        nova_client.floating_ips_bulk
        nova_client.os_cache
        nova_client.availability_zones
        nova_client.server_groups
        """

        nova_client = nova.Client("2", **self.nova_creds)
        return nova_client

    def get_glance_client(self):
        """
        glance_client.images
        glance_client.image_tags
        glance_clientimage_members
        glance_client.tasks
        glance_client.metadefs_resource_type
        glance_client.metadefs_property
        glance_client.metadefs_object
        glance_client.metadefs_tag
        glance_client.metadefs_namespace
        """
        token = self._get_keystone_token()
        services = self.get_keystone_client().services.list()
        the_id = None
        admin_url = None
        for service in services:
            if service.type == "image":
                the_id = service.id
        endpoints = self.get_keystone_client().endpoints.list()
        for endpoint in endpoints:
            if endpoint.service_id == the_id:
                admin_url = endpoint.adminurl
        glance_client = glance.Client(endpoint=admin_url, token=token)
        return glance_client

    def get_cinder_client(self):
        """
        cinder_client.limits
        cinder_client.volumes
        cinder_client.volume_snapshots
        cinder_client.volume_types
        cinder_client.volume_type_access
        cinder_client.volume_encryption_types
        cinder_client.qos_specs
        cinder_client.quota_classes
        cinder_client.quotas
        cinder_client.backups
        cinder_client.restores
        cinder_client.transfers
        cinder_client.services
        cinder_client.consistencygroups
        cinder_client.cgsnapshots
        cinder_client.availability_zones
        cinder_client.pools
        cinder_client.capabilities
        """
        cinder_client = cinder.Client(**self.nova_creds)
        return cinder_client

    def get_neutron_client(self):
        """
        """
        neutron_client = neutron.Client(**self.creds)
        return neutron_client







