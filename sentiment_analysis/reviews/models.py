from django.db import models


class Review(models.Model):
    review_text = models.TextField()  # Текст отзыва
    rating = models.IntegerField()  # Оценка от 1 до 10
    sentiment = models.CharField(max_length=10)  # Положительный или отрицательный отзыв

    def __str__(self):
        return self.review_text
