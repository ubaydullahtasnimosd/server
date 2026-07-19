from django.db import models
import uuid
from Comment.models import Comment

class Quran_Life_Lessons(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quranLessonImg = models.CharField(max_length=3000, default='', null=True, blank=True, verbose_name='ছবি ইউআরএল')
    quranLessonName = models.CharField(max_length=1000, verbose_name='পাঠের শিরোনাম')
    quranLessonAuthor = models.CharField(max_length=300, default='উবায়দুল্লাহ তাসনিম', verbose_name='লেখকের নাম')
    quranLessonDescription = models.TextField(verbose_name='বিস্তারিত তথ্য', blank=True, null=True)
    quranLessonCreateAt = models.DateTimeField(auto_now_add=True, verbose_name='প্রকাশের তারিখ')
    quranLessonUpdateAt = models.DateTimeField(auto_now=True, verbose_name='সম্পাদনার তারিখ')

    def __str__(self):
        return f'{self.quranLessonName}'
    
    @property
    def comments(self):
        return Comment.objects.filter(content_type__model='quran_life_lessons', object_id=self.id)
    
    class Meta:
        verbose_name_plural = 'কুরআন থেকে জীবনের পাঠ'
