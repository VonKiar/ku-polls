import datetime
from django.db import models
from django.utils import timezone


class Question(models.Model):
    """Question class containing question attributes and question's related function."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField(
        'date ended', default=timezone.now() + datetime.timedelta(days=1))

    def __str__(self):
        """Return question as text string."""
        return self.question_text

    def was_published_recently(self):
        """Check if the poll was published recently."""
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now

    def is_published(self):
        """Check if the poll is live."""
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check that the poll is available to vote."""
        now = timezone.now()
        return (self.is_published()) and (now < self.end_date)

    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = 'Published recently?'


class Choice(models.Model):
    """Choice class containing choice attributes."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        """Return choice as text string."""
        return self.choice_text
