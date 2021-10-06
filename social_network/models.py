from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from social_network.utilities import get_timestamp_path


class PostUser(AbstractUser):
    is_activated = models.BooleanField(default=True, db_index=True, verbose_name='Is this account activated?')
    date_last_request = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Last request to server')

    class Meta(AbstractUser.Meta):
        pass


class Post(models.Model):
    title = models.CharField(max_length=40,
                             verbose_name='Title')
    content = models.TextField(verbose_name='Content')

    image = models.ImageField(blank=True, upload_to=get_timestamp_path,
                              verbose_name='Image', null=True)

    is_active = models.BooleanField(default=True, db_index=True,
                                    verbose_name='Is post active')
    created_at = models.DateTimeField(auto_now_add=True, db_index=True,
                                      verbose_name='Post created at')
    author = models.ForeignKey(PostUser, on_delete=models.CASCADE,
                               verbose_name='Author')

    # todo ?
    def like_count(self):
        return self.likereaction_set.all().filter(reaction='like').count()

    def unlike_count(self):
        return self.likereaction_set.all().filter(reaction='unlike').count()

    def __str__(self):
        return "\"{}\" by {}".format(self.title, self.author)


class LikeReaction(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE,
                             verbose_name='Like and unlike')
    author = models.ForeignKey(PostUser, on_delete=models.CASCADE,
                               verbose_name='Who (un)liked')
    reacted = models.DateTimeField(auto_now_add=True,
                                   db_index=True,
                                   verbose_name='Date of reaction')

    LIKE = 'like'
    UNLIKE = 'unlike'
    REACTION = [
        (LIKE, 'Like'),
        (UNLIKE, 'Not like')
    ]
    reaction = models.CharField(
        max_length=6,
        choices=REACTION,
        default=LIKE,
        verbose_name='user reaction'
    )
