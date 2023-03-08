from django.db import models
from django.contrib.auth.models import User
from datetime import datetime, date
from tinymce.models import HTMLField
from PIL import Image
from django.utils.translation import gettext_lazy as _


class Preke(models.Model):
    pavadinimas = models.CharField('Pavadinimas', max_length=100)
    kaina = models.FloatField('Kaina')
    aprasymas = models.TextField('Aprašymas', max_length=1000, help_text='LEGO aprasymas', null=True, blank=True)
    nuotrauka = models.ImageField('Nuotrauka', upload_to='nuotraukos', null=True)

    def __str__(self):
        return f"{self.pavadinimas} ({self.kaina})"

    class Meta:
        verbose_name = "Preke"
        verbose_name_plural = "Prekes"


class Uzsakymas(models.Model):
    data = models.DateTimeField(verbose_name='Data', auto_now_add=True)
    preke_id = models.ForeignKey(verbose_name='Preke_id', to='Preke', on_delete=models.SET_NULL, null=True, blank=True)
    uzsakymo_numeris = models.CharField(verbose_name='Uzsakymo numeris', max_length=150, null=True)
    vartotojas = models.ForeignKey(to=User, verbose_name="User", on_delete=models.SET_NULL, null=True, blank=True)


    LOAN_STATUS = (
        ('p', 'Patvirtinta'),
        ('v', 'Vykdoma'),
        ('a', 'Atsaukta'),
        ('i', 'Ivykdyta'),
    )

    status = models.CharField(
        max_length=1,
        choices=LOAN_STATUS,
        blank=True,
        default='p',
        help_text='Statusas',
    )

    def suma(self):
        suma = 0
        eilutes = self.eilutes.all()
        for eilute in eilutes:
            suma += eilute.kaina()
        return suma


    def __str__(self):
        return f"{self.preke_id} ({self.uzsakymo_numeris})"


    class Meta:
        verbose_name = "Uzsakymas"
        verbose_name_plural = "Uzsakymai"

class Uzsakymo_eilute(models.Model):
    uzsakymas = models.ForeignKey(to='Uzsakymas', on_delete=models.CASCADE, related_name="eilutes")
    preke = models.ForeignKey(to='Preke', on_delete=models.SET_NULL, null=True)
    kiekis = models.IntegerField(verbose_name='Kiekis')


    def kaina(self):
        return self.preke.kaina * self.kiekis

    def __str__(self):
        return f"{self.preke} ({self.kiekis})"

    class Meta:
        verbose_name = "Uzsakymo eilute"
        verbose_name_plural = "Uzsakymo eilutes"

class Siuntimas(models.Model):
    uzsakymas = models.ForeignKey(to='Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True)
    adresas = models.CharField('Adresas', max_length=200)
    miestas = models.CharField('Miestas', max_length=100)
    telefonas = models.IntegerField(verbose_name='Telefonas')
    data = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.adresas}"

    class Meta:
        verbose_name = "Siuntimas"
        verbose_name_plural = "Siuntimai"

class Profilis(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nuotrauka = models.ImageField(default="profile_pics/default.png", upload_to="profile_pics")

    def __str__(self):
        return f"{self.user.username} profilis"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        img = Image.open(self.nuotrauka.path)
        if img.height > 100 or img.width > 100:
            output_size = (100, 100)
            img.thumbnail(output_size)
            img.save(self.nuotrauka.path)

class UzsakymasReview(models.Model):
    uzsakymas = models.ForeignKey('Uzsakymas', on_delete=models.SET_NULL, null=True, blank=True)
    vartotojas = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    content = models.TextField('Atsiliepimas', max_length=2000)

    class Meta:
        verbose_name = "Atsiliepimas"
        verbose_name_plural = 'Atsiliepimai'
        ordering = ['-date_created']
