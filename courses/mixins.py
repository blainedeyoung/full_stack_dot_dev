from django.db import models, transaction


class NumberedModelMixin(models.Model):
    """Abstract model mixin that provides a title field and a number field that is automatically assigned and unique."""
    number = models.IntegerField(blank=True)
    title = models.CharField(max_length=100)

    class Meta:
        abstract = True
        ordering = ["number"]

    def save(self, *args, **kwargs):
        """Finds the highest number that exists and assigns the next number to the instance."""
        if not self.number:
            max_number = (
                self.__class__.objects.filter(
                    **self.get_number_filter_kwargs()).
                aggregate(models.Max('number')))['number__max']
            self.number = max_number + 1 if max_number else 1
        super().save(*args, **kwargs)

    @transaction.atomic
    def delete(self, *args, **kwargs):
        """Deletes the instance and renumbers the remaining instances."""
        filter_kwargs = self.get_number_filter_kwargs()
        super().delete(*args, **kwargs)

        # renumber the instances
        for i, instance in enumerate(self.__class__.objects.filter(**filter_kwargs).order_by('number'), start=1):
            instance.number = i
            instance.save()

    def __str__(self):
        return f"{self.number}: {self.title}"

    def get_number_filter_kwargs(self):
        raise NotImplementedError("Subclasses must implement get_number_filter_kwargs method.")
