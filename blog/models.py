from django.db import models
from django.conf import settings
from core.models import User
# Create your models here.

class categories(models.Model):
    title = models.CharField(max_length = 100)
    keywords = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Categories'

class post(models.Model):
    title = models.CharField(max_length = 200)
    category = models.ForeignKey(categories, on_delete=models.CASCADE)
    content = models.TextField()
    date = models.DateField()
    published = models.BooleanField(default=1)
    main_image = models.ImageField()
    views = models.IntegerField(default=0)
    image1 = models.ImageField(blank=True, null=True)
    image2 = models.ImageField(blank=True, null=True)
    image3 = models.ImageField(blank=True, null=True)
    image4 = models.ImageField(blank=True, null=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-date',)
        
    def get_short_content(self):
        if len(self.content) > 500:
            short_content = self.content[:500]
            short_content += "..."
            return short_content
        return self.content


    def get_shortest_content(self):
        if len(self.content) > 200:
            short_content = self.content[:200]
            short_content += "..."
            return short_content
        return self.content

    def count_likes(self):
        count = like.objects.filter(post = self).count()
        return count

    def count_comments(self):
        count = comment.objects.filter(post = self).count()
        return count

class comment(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)
    image = models.ImageField(blank=True, null = True)
    date = models.DateField()
    comment_text = models.TextField()

    def __str__(self):
        return self.comment_text

    def get_username(self):
        username = self.user.username
        return username

    def get_profileimage(self):
        profileimage = 'http://placehold.it/50x50'
        return profileimage

class like(models.Model):
    post = models.ForeignKey(post, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

















