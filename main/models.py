import random
from django.db import models


class FormModel(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название формы")

    def __str__(self):
        return self.name


class FieldModel(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название поля")
    slug = models.SlugField(unique=True, verbose_name="Название переменной")
    form = models.ForeignKey(FormModel, verbose_name="Форма", on_delete=models.CASCADE, related_name='fields')
    # field Type
    # required

    def __str__(self):
        return f'id{self.id}'


class Document(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название документа")
    file_name = models.CharField(max_length=255, verbose_name="Название файла")
    text = models.TextField(verbose_name="Текст документа для генерации в контейнере")
    html_text = models.TextField(verbose_name="Текст документа для отображения на странице завершения html")

    def __str__(self):
        return f'id{self.id}'


class Message(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название письма")
    topic = models.CharField(max_length=255, verbose_name="Тема письма")
    text = models.TextField(verbose_name="Текст письма в html")

    def __str__(self):
        return f'id{self.id}'


class EndPage(models.Model):

    name = models.CharField(max_length=255, verbose_name="Название страницы")
    html_text = models.TextField(verbose_name="Текст страницы завершения в html")

    def __str__(self):
        return f'id{self.id}'


class ApplicationForm(models.Model):
    name = models.CharField(max_length=255, verbose_name="Название анкеты")
    slug = models.SlugField(unique=True, verbose_name="уникальная ссылка для доступа")
    form = models.OneToOneField(FormModel, verbose_name="Форма", on_delete=models.CASCADE)
    document = models.OneToOneField(Document, verbose_name="Документ", on_delete=models.CASCADE)
    message = models.OneToOneField(Message, verbose_name="Электронные сообщение", on_delete=models.CASCADE)
    end_page = models.OneToOneField(EndPage, verbose_name="Страница завершения", on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class FilledApplicationForm(models.Model):

    application_form = models.ForeignKey(ApplicationForm, verbose_name='Анкета', on_delete=models.CASCADE,
                                         related_name='filled_forms')
    values = models.JSONField(null=True)
    email = models.EmailField(verbose_name='Емаил')
    code = models.PositiveSmallIntegerField(default=random.randint(1000, 9999))
    signification = models.CharField(max_length=255, null=True, blank=True)
    # info about client

    def __str__(self):
        return str(self.id)






