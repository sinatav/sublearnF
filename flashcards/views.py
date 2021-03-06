from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from flashcards.models import MovieSet, Flashcard
from django.http import JsonResponse
from django.utils import timezone


@login_required
def load_decks(request):
    premium = request.user.profile.premium_date
    if premium < timezone.now():
        return render(request, 'flashcards/decks.html', {'is_premium': False})
    movie_sets = request.user.movieset_set.all().order_by('-date_added')
    known_flash_cards = Flashcard.objects.filter(movie__user_id=request.user.id, times_remembered__gt=0).count()
    all_flash_cards = Flashcard.objects.filter(movie__user_id = request.user.id).count()
    context = {'movie_sets': movie_sets, 'title': 'Flashcard Decks', 'learnt_flashcards': known_flash_cards,
               'all_flashcards': all_flash_cards, 'is_premium': True}
    return render(request, 'flashcards/decks.html', context)


@login_required
def show_flashcards(request, set_id):
    premium = request.user.profile.premium_date
    if premium < timezone.now():
        return render(request, 'flashcards/set.html', {'is_premium': False})
    movie_set = get_object_or_404(MovieSet, id=set_id)
    context = {'set': movie_set, 'title': movie_set.movie_name + " Flashcards", 'is_premium': True}
    return render(request, 'flashcards/set.html', context)


@login_required()
def flashcard_result(request):
    flash_id = request.POST.get('id')
    result = request.POST.get('result')
    try:
        flashcard = Flashcard.objects.get(id=flash_id)
        if int(result) == 1:
            flashcard.times_remembered += 1
            flashcard.save()
        elif int(result) == 0:
            flashcard.times_failed += 1
            flashcard.save()
        else:
            data = {'response': 'error', 'error_message': 'unknown result.'}
            return JsonResponse(data)
        data = {'response': 'success', 'is_premium': True}
        return JsonResponse(data)
    except Flashcard.DoesNotExist:
        data = {'response': 'error', 'error_message': 'flash card not found.'}
        return JsonResponse(data)
