from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Exists, OuterRef
from apps.subscribe.models import PinnedPost
from django.utils import timezone


class Category(models.Model):
    name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=100,unique=True, blank=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'categories'
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name
    
    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args,**kwargs)

class PostManager(models.Manager):

    def get_queryset(self):
        return super().get_queryset().select_related('author', 'category')

    def feed(self):
        return self.get_queryset().filter(
            status='published'
        ).annotate(
            is_pinned=Exists(
                PinnedPost.objects.filter(post=OuterRef('pk'))
            )
        ).order_by('-is_pinned', '-created_at')


class Post(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)

    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        related_name='posts'
    )

    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='posts'
    )

    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    views_count = models.PositiveIntegerField(default=0)

    objects = PostManager()

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


    def save(self,*args,**kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args,**kwargs)

    def absolute_url(self):
        return reverse('post_detail',kwargs={'slug': self.slug})
    
    @property
    def comments_count(self):
        return self.comments.filter(is_active=True).count()
    

    def is_pinned_flag(self):
        return hasattr(self,'pin_info') and self.pin_info is not None

    @property
    def can_be_pinned_by_user(self):
        if self.status !='published':
            return False
        
        return True
    
    @property
    def can_be_pinned_by(self,user):
        if not user or not user.is_authenticated:
            return False
        
        if self.author != user:
            return False
        
        if self.status !='published':
            return False
        
        if not hasattr(user,'subscription') or not user.subscription.is_active:
            return False
        
        return True


    def increment_views(self):
        self.views_count += 1
        self.save(update_fields=['views_count'])


    def get_pinned_info(self):
        if self.is_pinned:
            return{
                'is_pinned': True,
                'pinned_at': self.pin_info.pinned_at,
                'pinned_by': {
                    'id': self.pin_info.user.id,
                    'username': self.pin_info.user.username,
                    'has_active_subscription': self.pin_info.user.subscription.is_active,
                }
            }
        return {'is_pinned':False}
