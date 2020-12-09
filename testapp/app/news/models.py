from django.db import models


class Category(models.Model):
    name = models.CharField('name', max_length=50)

    class Meta:
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return "{0}".format(self.name)


class Tag(models.Model):
    TYPE_GENERIC = 1
    TYPE_SPECIFIC = 2
    TYPE_CHOICES = (
        (TYPE_GENERIC, 'generic', ),
        (TYPE_SPECIFIC, 'specific', ),
    )
    name = models.CharField('verbose name', max_length=30)
    type = models.IntegerField(choices=TYPE_CHOICES, default=TYPE_GENERIC)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('name',)


class News(models.Model):
    ARCHIVED = 0
    DRAFT = 1
    PUBLISHED = 2

    STATUS_CHOICES = (
        (ARCHIVED, 'archived', ),
        (DRAFT, 'draft', ),
        (PUBLISHED, 'published', ),
    )

    category = models.ForeignKey(
        Category,
        verbose_name='category',
        on_delete=models.CASCADE,
        related_name='news',
    )
    date = models.DateField('date')
    datetime = models.DateTimeField('datetime', blank=True, null=True, help_text='insert date')
    title = models.CharField('main title', max_length=50, help_text='please insert a cool title')
    link = models.URLField('link', blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    content = models.TextField(verbose_name='content', help_text='html is supported')
    tags = models.ManyToManyField(Tag, through='NewsTag', verbose_name='all tags')
    share = models.BooleanField(default=False)
    status = models.IntegerField(choices=STATUS_CHOICES, default=DRAFT)
    attachments_summary = models.TextField('attachments summary', blank=True)
    videos_summary = models.TextField('videos summary', blank=True)

    class Meta:
        verbose_name = "news"
        verbose_name_plural = "news"

    def __str__(self):
        return '{0}'.format(self.title)


class Attachment(models.Model):
    news = models.ForeignKey(
        News,
        verbose_name='news',
        on_delete=models.CASCADE,
        related_name='attachments',
    )
    file = models.FileField(upload_to='news/img')
    caption = models.TextField()

    class Meta:
        verbose_name = "attachment"
        verbose_name_plural = "attachments"

    def __str__(self):
        return '{0}'.format(self.caption)


class Video(models.Model):
    news = models.ForeignKey(
        News,
        verbose_name='news',
        on_delete=models.CASCADE,
        related_name='videos',
    )
    code = models.CharField('video code', max_length=50)
    caption = models.TextField()
    author_email = models.EmailField(blank=True, null=True)

    class Meta:
        verbose_name = "video"
        verbose_name_plural = "videos"

    def __str__(self):
        return '{0}'.format(self.caption)


class NewsTag(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    news = models.ForeignKey(News, on_delete=models.CASCADE)

    created_on = models.DateTimeField('created on', auto_now_add=True)

    def __str__(self):
        return "{} on {}".format(self.tag, self.news)

    class Meta:
        ordering = ('created_on',)
