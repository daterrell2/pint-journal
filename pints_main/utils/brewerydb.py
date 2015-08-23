'''
This module wraps GET requests to brewerydb.com  API.
It's adapted from the python service library linked to in the
BreweryDb API documentation:

    https://github.com/yarian/brewerydb

The original script defines the simple and single_param endpoints as methods
of the BreweryDb objects.

A few features I added:
    - Implemented requests_cache: API requests will be cached in CACHE_BACKEND (sqlite default)
        until CACHE_EXPIRE_AFTER seconds have passed (1 day default)

    - Added 'join_endpoints' for one-to-many requests.
        For example, to return all locations for a brewery, you can call

            BreweryDb.brewery_locations(<brewery_id>)

        Which makes the following API request:

            http://api.brewerydb.com/v2/<API_KEY>/brewery/<brewery_id>/locations

'''


import requests
import requests_cache
import __builtin__
import keyword
import time

DEFAULT_BASE_URI = "http://api.brewerydb.com/v2"
BASE_URI = ""
API_KEY = ""

CACHE_EXPIRE_AFTER = 60 * 60 * 24 # cache exipres daily
CACHE_NAME = 'brewerydb_cache'
CACHE_BACKEND = 'sqlite'

simple_endpoints = ["beers", "breweries", "categories", "events",
                    "featured", "features", "fluidsizes", "glassware",
                    "locations", "guilds", "heartbeat", "ingredients",
                    "search", "search/upc", "socialsites", "styles"]

single_param_endpoints = ["beer", "brewery", "category", "event",
                          "feature", "glass", "guild", "ingredient",
                          "location", "socialsite", "style", "menu"]

# my addition
join_endpoints = ["beer/breweries", "brewery/beers", "brewery/locations"]

class BreweryDb:

    @staticmethod
    def __make_simple_endpoint_fun(name):
        @staticmethod
        def _function(options={}):
            return BreweryDb._get("/" + name, options)
        return _function

    @staticmethod
    def __make_singlearg_endpoint_fun(name):
        @staticmethod
        def _function(id, options={}):
            return BreweryDb._get("/" + name + "/" + id, options)
        return _function


    # my addition
    @staticmethod
    def __make_join_endpoint_fun(name):
        name1, name2 = name.split("/")
        @staticmethod
        def _function(id, options={}):
            return BreweryDb._get("/" + "/".join([name1, id, name2]), options)
        return _function


    @staticmethod
    def _get(request, options):
        options.update({"key" : BreweryDb.API_KEY})
        now = time.ctime(int(time.time()))
        r = requests.get(BreweryDb.BASE_URI + request, params=options)
        print "Time: {0} / Used Cache: {1}".format(now, r.from_cache)
        return r.json()

    @staticmethod
    def configure(apikey, baseuri=DEFAULT_BASE_URI):
        print "Configuring BreweryDb API wrapper"
        BreweryDb.API_KEY = apikey
        BreweryDb.BASE_URI = baseuri
        for endpoint in simple_endpoints:
            fun = BreweryDb.__make_simple_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)
        for endpoint in single_param_endpoints:
            fun = BreweryDb.__make_singlearg_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)

        # my addition
        for endpoint in join_endpoints:
            fun = BreweryDb.__make_join_endpoint_fun(endpoint)
            setattr(BreweryDb, endpoint.replace('/', '_'), fun)
        print "Installing requests_cache"
        requests_cache.install_cache(cache_name=CACHE_NAME, backend=CACHE_BACKEND, expire_after=CACHE_EXPIRE_AFTER)

# my addition--potentially bad idea!!!
class BreweryDbObject(object):
    '''
    Unpacks API reutrned object (nested dict) into an object, with
    dict keys as attributes. Also recursively unpacks nested dicts
    as BreweryDbObjects

    Renames any attr that is  python keywords/ builtins to attr_
    '''
    def __init__(self, data = {}):

        for k, v in data.items():
            if k in dir(__builtin__) + keyword.kwlist:
                data[k+'_'] = v
                del data[k]

        for k, v in data.items():

            if isinstance(v, dict):
                setattr(self, k, BreweryDbObject(v))

            elif isinstance(v, (list, tuple)):
                setattr(self, k, [BreweryDbObject(i) if isinstance(i, dict) else i for i in v])

            else:
                setattr(self, k, v)


