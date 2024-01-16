from django.contrib.auth import get_user_model
from django.shortcuts import reverse
from django.db import models
from django.template.defaultfilters import slugify


class Article(models.Model):
    author = models.ForeignKey(to=get_user_model(), related_name='article', on_delete=models.CASCADE)
    title = models.CharField(max_length=255, unique=True, db_index=True)
    slug = models.SlugField(max_length=255, editable=False, db_index=True)
    content = models.TextField()
    create_data = models.DateTimeField(editable=False, auto_now_add=True)
    update_data = models.DateTimeField(editable=False, auto_now=True)

    def __str__(self):
        return self.title[:50]

    def get_absolute_url(self):
        return reverse('detail_article', kwargs={'slug': self.slug})

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class Comment(models.Model):
    user = models.ForeignKey(to=get_user_model(), on_delete=models.CASCADE, related_name='comments')
    article = models.ForeignKey(to='Article', on_delete=models.CASCADE, related_name='comments')
    comment = models.CharField(max_length=5000)
    create_data = models.DateTimeField(editable=False, auto_now_add=True)

    class Meta:
        ordering = ['-create_data', ]

    def __str__(self):
        return self.comment[:50]
