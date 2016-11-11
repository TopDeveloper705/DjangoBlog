from django.db import models
from django.core.urlresolvers import reverse
from django.conf import settings


class Article(models.Model):
    """文章"""
    STATUS_CHOICES = (
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    title = models.CharField('标题', max_length=200)
    body = models.TextField('正文')
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    pub_time = models.DateTimeField('发布时间', blank=True, null=True,
                                    help_text="不指定发布时间则视为草稿，可以指定未来时间，到时将自动发布。")
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='o')
    commentstatus = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS)
    summary = models.CharField('摘要', max_length=200, blank=True, help_text="可选，若为空将摘取正文的前300个字符。")
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)

    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-pub_time']
        verbose_name = "文章"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:detail', kwargs={'article_id': self.pk})

    def get_category_tree(self):
        names = []

        def parse(category):
            names.append((category.name, category.get_absolute_url()))
            if category.parent_category:
                parse(category.parent_category)

        parse(self.category)
        return names

    def save(self, *args, **kwargs):
        self.summary = self.summary or self.body[:settings.ARTICLE_SUB_LENGTH]
        super().save(*args, **kwargs)

    def viewed(self):
        self.views += 1
        self.save(update_fields=['views'])


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)
    parent_category = models.ForeignKey('self', verbose_name="父级分类", blank=True, null=True)

    class Meta:
        ordering = ['name']
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def get_absolute_url(self):
        return reverse('blog:category_detail', kwargs={'category_name': self.name})

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名', max_length=30)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag_detail', kwargs={'tag_name': self.name})

    def get_article_count(self):
        return Article.objects.filter(tags__name=self.name).distinct().count()

    class Meta:
        ordering = ['name']
        verbose_name = "标签"
        verbose_name_plural = verbose_name


class Links(models.Model):
    """友情链接"""
    name = models.CharField('链接名称', max_length=30)
    link = models.URLField('链接地址')
    sequence = models.IntegerField('排序', unique=True)
    created_time = models.DateTimeField('创建时间', auto_now_add=True)
    last_mod_time = models.DateTimeField('修改时间', auto_now=True)

    class Meta:
        ordering = ['sequence']
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
