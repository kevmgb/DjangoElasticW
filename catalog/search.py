# create a connection from your Django application to ElasticSearch.
from elasticsearch_dsl.connections import connections
from elasticsearch_dsl import DocType, Text, Date, Search
from elasticsearch.helpers import bulk
from elasticsearch import Elasticsearch
from . import models

# Create a connection to ElasticSearch
connections.create_connection()

# ElasticSearch "model" mapping out what fields to index
# DocType works as a wrapper to enable you to write an index like a model
# Text and Date are the fields so that they get the correct format when they get indexed.

# formerly blogpostindex


class AuthorIndex(DocType):
    first_name = Text()
    last_name = Text()
    date_of_birth = Date()


# Inside the Meta you tell ElasticSearch what you want the index to be named.
# This will be a point of reference for ElasticSearch so that it knows what index 
# it’s dealing with when initializing it in the database and saving each new object instance created.

# Now we create the actual mapping of AuthorIndex in elasticsearch
# we can do this as well as create a way to do bulk indexing at the same time

# Bulk indexing function, run in shell


def bulk_indexing():
    # Since you only want to do bulk indexing whenever you change something in our model you init() the model which maps it into ElasticSearch. 
    AuthorIndex.init(index='author-index')
    es = Elasticsearch()
    # Then, you use the bulk and pass it an instance of Elasticsearch() which will create a connection to ElasticSearch.
    # You then pass a generator to actions= and iterate over all the author Post objects you have in your regular database and call the .indexing() method on each object. 
    bulk(client=es, actions=(b.indexing() for b in models.Author.objects.all().iterator()))
    # Why a generator? Because if you had a lot of objects to iterate over a generator would not have to first load them into memory.

# Simple search function

# find last_name by first_name
def search(first_name):
    s = Search(index='author-index').filter('term', first_name=first_name)
    response = s.execute()
    return response
