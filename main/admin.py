from django.contrib import admin
from . import models


class FieldInline(admin.TabularInline):

    model = models.FieldModel


class FormAdmin(admin.ModelAdmin):
    inlines = [FieldInline, ]


class FilledAdmin(admin.ModelAdmin):
    readonly_fields = [
        'application_form',
        'values',
        'email',
        'code',
        'signification',
    ]


admin.site.register(models.FormModel, FormAdmin)
admin.site.register(models.ApplicationForm)
admin.site.register(models.FieldModel)
admin.site.register(models.Message)
admin.site.register(models.Document)
admin.site.register(models.EndPage)
admin.site.register(models.FilledApplicationForm, FilledAdmin)








