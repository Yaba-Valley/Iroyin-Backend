from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from news.models import News, Interest


class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_staffuser(self, email, password):
        """
        Creates and saves a staff user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_active = True
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_active = True
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):

    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )

    objects = UserManager()

    is_active = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)

    first_name = models.CharField(max_length=100, verbose_name='First Name')
    last_name = models.CharField(max_length=100, verbose_name='Last Name')
    newsSeen = models.ManyToManyField(
        to=News, related_name='readers', verbose_name='News Seen By User')
    newInteractedWith = models.ManyToManyField(
        to=News, related_name='readers_interacted', verbose_name='News User Interacted With')
    interests = models.ManyToManyField(to=Interest, related_name='users')
    saved_news = models.ManyToManyField(to = News, related_name = 'savers', verbose_name="news saved")
    liked_news = models.ManyToManyField(to = News, related_name = 'likers', verbose_name = 'news liked')
    disliked_news = models.ManyToManyField(to = News, related_name = 'dislikers', verbose_name = 'news disliked')
    shared_news = models.ManyToManyField(to = News, related_name = 'sharers', verbose_name = 'news shared')

    USERNAME_FIELD = 'email'

    def get_full_name(self):
        return "%s %s" % (self.first_name, self.last_name)

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.get_full_name()

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    def __str__(self):
        return self.email
