# Copyright (c) 2012-2013, Mark Peek <mark@peek.org>
# Copyright (c) 2014, Andy Botting <andy.botting@theguardian.com>
# All rights reserved.
#
# See LICENSE file for full license.


from troposphere import AWSObject, AWSProperty
from troposphere.validators import boolean, integer, network_port


class BlockDeviceMapping(AWSProperty):
    props = {
        'delete_on_termination': (boolean, False),
        'device_name': (basestring, True),
        'snapshot_id': (basestring, False),
        'volume_id': (basestring, False),
        'volume_size': (integer, False),
    }


class Network(AWSProperty):
    props = {
        'fixed_ip': (basestring, False),
        'network': (basestring, False),
        'port': (network_port, False),
    }


class FloatingIP(AWSObject):
    resource_type = "OS::Nova::FloatingIP"

    props = {
        'pool': (basestring, False),
    }


class FloatingIPAssociation(AWSObject):
    resource_type = "OS::Nova::FloatingIPAssociation"

    props = {
        'floating_ip': (basestring, True),
        'server_ip': (basestring, True),
    }


class KeyPair(AWSObject):
    resource_type = "OS::Nova::KeyPair"

    props = {
        'name': (basestring, True),
        'public_key': (basestring, False),
        'save_private_key': (boolean, False),
    }


class Server(AWSObject):
    resource_type = "OS::Nova::Server"

    props = {
        'admin_pass': (basestring, False),
        'admin_user': (basestring, False),
        'availability_zone': (basestring, False),
        'block_device_mapping': (list, False),
        'config_drive': (basestring, False),
        'diskConfig': (basestring, False),
        'flavor': (basestring, False),
        'flavor_update_policy': (basestring, False),
        'image': (basestring, True),
        'image_update_policy': (basestring, False),
        'key_name': (basestring, False),
        'metadata': (dict, False),
        'name': (basestring, False),
        'personality': (dict, False),
        'networks': (list, True),
        'reservation_id': (basestring, False),
        'scheduler_hints': (dict, False),
        'security_groups': (list, False),
        'software_config_transport': (basestring, False),
        'user_data': (basestring, False),
        'user_data_format': (basestring, False),
    }

    def validate(self):
        if 'diskConfig' in self.resource:
            diskConfig = self.resource['diskConfig']
            if diskConfig not in ['AUTO', 'MANUAL']:
                raise ValueError(
                    "The diskConfig attribute "
                    "must be either AUTO or MANUAL")

        if 'flavor_update_policy' in self.resource:
            flavor_update_policy = self.resource['flavor_update_policy']
            if flavor_update_policy not in ['RESIZE', 'REPLACE']:
                raise ValueError(
                    "The flavor_update_policy attribute "
                    "must be either RESIZE or REPLACE")

        if 'image_update_policy' in self.resource:
            image_update_policy = self.resource['flavor_update_policy']
            if image_update_policy not in ['REBUILD', 'REPLACE',
                                           'REBUILD_PRESERVE_EPHEMERAL']:
                raise ValueError(
                    "The image_update_policy attribute "
                    "must be either REBUILD, REPLACE or "
                    "REBUILD_PRESERVE_EPHEMERAL")

        if 'software_config_transport' in self.resource:
            sct = self.resource['software_config_transport']
            if sct not in ['POLL_SERVER_CFN', 'POLL_SERVER_HEAT']:
                raise ValueError(
                    "The software_config_transport attribute "
                    "must be either POLL_SERVER_CFN or POLL_SERVER_HEAT")

        if 'user_data_format' in self.resource:
            user_data_format = self.resource['user_data_format']
            if user_data_format not in ['HEAT_CFNTOOLS', 'RAW']:
                raise ValueError(
                    "The user_data_format attribute "
                    "must be either HEAT_CFNTOOLS or RAW")

        return True
