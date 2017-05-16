import os
import keystoneclient.v2_0.client as ksclient_v2
from keystoneauth1.identity import v3
from keystoneauth1 import session
from keystoneclient.v3 import client as ksclient_v3
from keystoneauth1.identity import v2
import novaclient.client as nova
import glanceclient.v2.client as glance
import cinderclient.v3.client as cinder_v3
import neutronclient.v2_0.client as neutron


class ClientManager(object):

    CWD = os.getcwd()

    def __init__(self, username, password, auth_url, project_name,
                 user_domain_id="default",
                 project_domain_id="default"):
        self.credentials = {'username': username,
                            'password': password,
                            'auth_url': auth_url,
                            'project_name': project_name,
                            'user_domain_id': user_domain_id,
                            'project_domain_id': project_domain_id
                      }
        self.keystone_version = 2 if auth_url.find("/v2.0") != -1 else 3

    def _get_session_for_service(self):
        if self.keystone_version == 3:
            auth = v3.Password(**self.credentials)
            return session.Session(auth=auth)
        elif self.keystone_version == 2:
                auth = v2.Password(
                    auth_url=self.credentials['auth_url'],
                    username=self.credentials['username'],
                    password=self.credentials['password'],
                    tenant_name=self.credentials['project_name'])
                return session.Session(auth=auth)
        else:
            raise RuntimeError("Not supported keystone version")

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
        if self.keystone_version == 3:
            session = self._get_session_for_service()
            return ksclient_v3.Client(session=session)
        elif self.keystone_version == 2:
            session = self._get_session_for_service()
            return ksclient_v2.Client(session=session)

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
        session = self._get_session_for_service()
        nova_client = nova.Client("2.1", session=session)
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
        session = self._get_session_for_service()
        glance_client = glance.Client(session = session)
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
        session =  self._get_session_for_service()
        cinder_client = cinder_v3.Client(session = session)
        return cinder_client

    def get_neutron_client(self):
        """
        """
        neutron_client = neutron.Client(**self.creds)
        return neutron_client







