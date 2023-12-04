from flask_login import login_required, current_user
import requests


from flask import Blueprint, flash, redirect, render_template, request, url_for
from ..client import Pokemon

pokemon_bp = Blueprint('pokemon', __name__, url_prefix='/pokemon')
@pokemon_bp.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        pokemon_name = request.form.get('pokemon_name')
        return redirect(url_for('pokemon.display_pokemon', name_or_id=pokemon_name))
    return render_template('pokemon_search.html')

@pokemon_bp.route('/pokemon/<name_or_id>')
def display_pokemon(name_or_id):
    poke_client = Pokemon()
    pokemon = poke_client.get_pokemon(name_or_id)

    if not pokemon:
        flash("Pokémon not found", "danger")
        return redirect(url_for('pokemon.search'))
    
    if pokemon:
        # Fetch evolution data
        evolutions = poke_client.get_pokemon_evolutions(pokemon['name'])
    # Fetch reviews and include logic to fetch replies if they are not embedded in the Review model
    reviews = Review.objects(pokemon_name=name_or_id).order_by('-posted_at')

    return render_template('pokemon_display.html', pokemon=pokemon, reviews=reviews, evolutions=evolutions)

from ..models import Review, Reply  # Import the Reply model

@pokemon_bp.route('/post_reply/<pokemon_name>', methods=['POST'])
@login_required
def post_reply(pokemon_name):
    content = request.form.get('reply_content')
    if content:
        new_reply = Review(author=current_user._get_current_object(), content=content, pokemon_name=pokemon_name)
        new_reply.save()
        flash('Your reply has been posted.', 'success')
    else:
        flash('Reply content is required.', 'danger')

    return redirect(url_for('pokemon.display_pokemon', name_or_id=pokemon_name))



@pokemon_bp.route('/reply_to_review/<review_id>', methods=['POST'])
@login_required
def reply_to_review(review_id):
    try:
        review = Review.objects.get(id=review_id)
    except Review.DoesNotExist:
        flash('Review not found.', 'danger')
        return redirect(url_for('some_route'))

    content = request.form.get('reply_content')
    if content:
        reply = Reply(content=content, author=current_user._get_current_object(), review=review)
        reply.save()

        # Add the reply to the review's replies list
        review.update(push__replies=reply)

        flash('Your reply has been posted.', 'success')
    else:
        flash('Reply content cannot be empty.', 'danger')

    return redirect(url_for('pokemon.display_pokemon', name_or_id=review.pokemon_name))


@pokemon_bp.route('/type/<type_name>')
def pokemon_by_type(type_name):
    poke_client = Pokemon()
    pokemons = poke_client.get_pokemon_by_type(type_name)

    return render_template('pokemon_by_type.html', type_name=type_name, pokemons=pokemons)


@pokemon_bp.route('/ability/<ability_name>')
def pokemon_by_ability(ability_name):
    poke_client = Pokemon()
    pokemons = poke_client.get_pokemon_by_ability(ability_name)

    return render_template('pokemon_by_ability.html', ability_name=ability_name, pokemons=pokemons)
