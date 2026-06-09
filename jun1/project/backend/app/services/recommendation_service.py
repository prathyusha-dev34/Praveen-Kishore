from collections import Counter

from app.models.user_preference import UserPreference


def save_user_preferences(
    db,
    user_id,
    favorites,
    searches,
    viewed_movies
):

    genres = []

    for movie in favorites:

        if movie.genre:

            genres.extend(
                movie.genre.split(",")
            )

    for movie in viewed_movies:

        if movie.genre:

            genres.extend(
                movie.genre.split(",")
            )

    for search in searches:

        genres.append(
            search.keyword
        )

    counter = Counter(genres)

    db.query(
        UserPreference
    ).filter(
        UserPreference.user_id == user_id
    ).delete()

    for genre, score in counter.most_common(5):

        preference = UserPreference(
            genre=genre.strip(),
            score=score,
            user_id=user_id
        )

        db.add(preference)

    db.commit()

    return [
        genre.strip()
        for genre, score
        in counter.most_common(5)
    ]