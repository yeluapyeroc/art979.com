from django.db import models

class Tag(models.Model):
    ## attributes
    keyword = models.CharField(max_length=30)
    total_ref = models.IntegerField(blank=True, default=0)
    font_size = models.IntegerField(blank=True, default=0)

    def __cmp__(self, other):
        return cmp(self.total_ref, other.total_ref)
