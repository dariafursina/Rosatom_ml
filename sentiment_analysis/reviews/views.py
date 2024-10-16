from django.shortcuts import render
from keras_preprocessing.sequence import pad_sequences
from keras_preprocessing.text import Tokenizer
from tensorflow.python.keras.models import load_model

from .forms import ReviewForm
from .models import Review

# Параметры, которые использовались при обучении модели
max_words = 10000
maxlen = 200

# Загрузка обученной модели
model = load_model('Django/sentiment_analysis/reviews/ml_model/movie_review_model.h5')  # Путь к сохраненной модели
tokenizer = Tokenizer(num_words=max_words)  # Это тот же токенизатор, что использовался при обучении


# Функция для предобработки текста
def preprocess_text(text, tokenizer):
    sequence = tokenizer.texts_to_sequences([text])
    padded_sequence = pad_sequences(sequence, maxlen=maxlen)
    return padded_sequence


# Функция для предсказания
def predict_sentiment(text):
    # Предобработка текста
    processed_text = preprocess_text(text, tokenizer)

    # Предсказание с использованием обученной модели
    prediction = model.predict(processed_text)

    # Определение класса (положительный/отрицательный) и вычисление рейтинга
    sentiment = "positive" if prediction >= 0.5 else "negative"
    rating = int(prediction * 10)  # Преобразуем вероятность в рейтинг

    return sentiment, rating


# Представление для создания отзыва
def review_create(request):
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review_text = form.cleaned_data['review_text']
            sentiment, rating = predict_sentiment(review_text)

            # Сохранение отзыва в базе данных
            review = Review(review_text=review_text, rating=rating, sentiment=sentiment)
            review.save()

            return render(request, 'reviews/review_success.html', {'review': review})
    else:
        form = ReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})
