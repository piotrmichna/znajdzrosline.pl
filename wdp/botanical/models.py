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

    def __str__(self):
        return self.lac_name


class BotSystCultivar(models.Model):
    species = models.ForeignKey(BotSystSpecies, on_delete=models.CASCADE)
    cultivar = models.CharField(max_length=32, null=False, verbose_name='Odmiana')

    def __str__(self):
        return self.cultivar


class PlantBodyType(models.Model):
    body_type = models.CharField(max_length=32, null=False)
    lp = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return self.body_type


class PlantDescriptions(models.Model):
    botanical = models.TextField()
    cultivation = models.TextField()
    destiny = models.TextField()


class PlntLibraries(models.Model):
    genus = models.ForeignKey(BotSystGenus, on_delete=models.CASCADE)
    species = models.ForeignKey(BotSystSpecies, on_delete=models.CASCADE, null=True)
    cultivar = models.ForeignKey(BotSystCultivar, on_delete=models.CASCADE, null=True)
    body_type = models.ForeignKey(PlantBodyType, on_delete=models.CASCADE, null=True)
    edible = models.BooleanField(default=False)
    description = models.OneToOneField(PlantDescriptions, on_delete=models.CASCADE, null=True)

    # plant= PlnatLibraries.objects.filter(body_type__body_type='Drzewo iglaste', genus__lac_name='Acer')

    def edible_show(self):
        if self.edible:
            return 'Tak'
        else:
            return 'Nie'
