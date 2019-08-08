# you need to add a signal that fires the .indexing() on each new instance 
# that is saved every time a user saves a new blog post. In elasticsearchapp 
# create a new file called signals.py and add this code:

from .models import Author
from django.db.models.signals import post_save
from django.dispatch import receiver


# Signal to save each new blog post instance into ElasticSearch
@receiver(post_save, sender=Author)
def index_post(sender, instance, **kwargs):
    print(instance)
    instance.indexing()
