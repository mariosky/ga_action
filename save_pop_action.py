
import os
from cloudant.client import Cloudant
from cloudant.error import CloudantException
from cloudant.result import Result, ResultByKey

serviceUsername = os.environ['CLOUDANTUSER']
servicePassword = os.environ['CLOUDANTPASS']
serviceURL = os.environ['CLOUDANTURL']

print serviceUsername
print servicePassword
print serviceURL

client = Cloudant(serviceUsername, servicePassword, url=serviceURL)
client.connect()

