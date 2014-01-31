import os
import time
from keystoneclient.v2_0 import client as kclient
from novaclient.v1_1 import client as nclient

from glanceclient import client as gclient

# Fetch credentials

OS_USERNAME = os.environ['OS_USERNAME']
OS_PASSWORD = os.environ['OS_PASSWORD']
OS_TENANT_NAME = os.environ['OS_TENANT_NAME']
OS_AUTH_URL = os.environ['OS_AUTH_URL']

# Initialize clients

nova_client = nclient.Client(OS_USERNAME,
                             OS_PASSWORD,
                             OS_TENANT_NAME,
                             OS_AUTH_URL)

keystone_client = kclient.Client(username=OS_USERNAME,
                                 password=OS_PASSWORD,
                                 tenant_name=OS_TENANT_NAME,
                                 auth_url=OS_AUTH_URL)

keystone_client.authenticate()

OS_AUTH_TOKEN = keystone_client.auth_token
OS_IMAGE_ENDPOINT = keystone_client.service_catalog.url_for(
    service_type='image',
    endpoint_type='publicURL')

glance_client = gclient.Client('1', endpoint=OS_IMAGE_ENDPOINT,
                               token=OS_AUTH_TOKEN)

images = glance_client.images.list()

# Create image

image_prefix = 'ubuntu'
flavor_small = nova_client.flavors.list()[1]

for image in images:
    if image.name.startswith(image_prefix):
        image_id = image.id
        break

nova_client.servers.create(name='ubuntu_small_' + str(time.time()),
                           image=image_id,
                           flavor=flavor_small)
