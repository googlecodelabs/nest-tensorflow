#!/usr/bin/python
#
# Copyright 2017 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import urllib
import urllib2
import json
import os

nest_auth_url =         'https://home.nest.com/login/oauth2'
nest_access_token_url = 'https://api.home.nest.com/oauth2/access_token'

# Set your OAuth client ID and secret as environment variables. 
# See docker-compose.yml for an example of where they can be set 
# if not publishing that file.
client_id     = os.environ.get("CLIENT_ID", None)
client_secret = os.environ.get("CLIENT_SECRET", None)

def get_access_token(authorization_code):
    """Paste get_access_token(authorization_code) snippet below this line"""
    return

def authorization_url():
    query = urllib.urlencode({
        'client_id': client_id,
        'state':     'STATE'
    })
    return "{0}?{1}".format(nest_auth_url, query)
