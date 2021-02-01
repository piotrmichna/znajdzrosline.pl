from django.db import models


class BotSystGenus(models.Model):
    lac_name = models.CharField(max_length=32, null=False, verbose_name='Nazwa łacińska')
    pl_name = models.CharField(max_length=32, null=False, verbose_name='Nazwa polska')
    hybrid = models.BooleanField(null=True, verbose_name='Mieszaniec')

    def __str__(self):
        return self.lac_name


class BotSystSpecies(models.Model):
    genus = models.ForeignKey(BotSystGenus, on_delete=models.CASCADE)
    lac_name = models.CharField(max_length=32, null=False, verbose_name='Nazwa łacińska')
    pl_name = models.CharField(max_length=32, null=False, verbose_name='Nazwa polska')
    hybrid = models.BooleanField(null=True, verbose_name='Mieszaniec')


class BotSystCultivar(models.Model):
    species = models.ForeignKey(BotSystSpecies, on_delete=models.CASCADE)
    cultivar = models.CharField(max_length=32, null=False, verbose_name='Odmiana')


class PlantBodyType(models.Model):
    body_type = models.CharField(max_length=32, null=False)
    lp = models.PositiveSmallIntegerField(default=0)
