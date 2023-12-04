from app import cocktailRecommender

from . import bar
from app.models import CocktailDTO
from flask_login import login_required
from flask_paginate import get_page_args, Pagination
from flask_babel import gettext

from .forms import EvalForm, SimpleForm
from flask import request, render_template, flash, url_for, redirect, session



@bar.route('/cocktail/<name>?<ask_eval>', methods=["GET", "POST"])
def cocktail(name, ask_eval):

    for c in cocktailRecommender.case_base.get_all_cocktails():
        print(c.ingredient_quantity_unit)
        print('----------')

    form = EvalForm()
    cocktail = cocktailRecommender.get_recommended_cocktail() if ask_eval == 'True' else cocktailRecommender.get_cocktail(name)
    if cocktail is not None:
        print(cocktail.ingredient_quantity_unit)
        cocktailDTO = CocktailDTO(cocktail)
        if form.validate_on_submit():
            value = request.form.getlist('option')
            if len(value) == 0:
                error = (gettext('You must select an opinion.'))
                return render_template('bar/cocktail.html', cocktail=cocktailDTO, ask_eval=str(ask_eval), form=form, error = error)
            cocktailRecommender.set_user_evaluation(value[0])
            flash(gettext('Thanks for your opinion! We are going to keep improving :)'))
            return render_template('bar/cocktail.html', cocktail=cocktailDTO, ask_eval=str(False), form=form)
        else:
            return render_template('bar/cocktail.html', cocktail=cocktailDTO, ask_eval=str(ask_eval), form=form)
    else:
        return render_template('404.html', name=name)

def get_cocktail_pagination(cocktail_list, per_page=10, offset=0):
    return cocktail_list[offset: offset + per_page]

@bar.route('/cocktails', methods=['GET'])
def cocktails():

    cocktail_list = cocktailRecommender.get_all_cocktails()
    cocktail_list = [CocktailDTO(c) for c in cocktail_list]
    cocktail_list = sorted(cocktail_list, key=lambda x: x.name)


    page, per_page, offset = get_page_args(page_parameter='page',
                                           per_page_parameter='per_page')
    total = len(cocktail_list)
    pagination_cocktails = get_cocktail_pagination(cocktail_list, offset=offset, per_page=per_page)
    pagination = Pagination(page=page, per_page=per_page, total=total,
                            css_framework='bootstrap4')

    return render_template('bar/cocktails.html',
                           cocktails=pagination_cocktails,
                           page=page,
                           per_page=per_page,
                           pagination=pagination,
                           )

@bar.route('/specially4you', methods=['GET', 'POST'])
@login_required
def specially4you():

    #I have ommited the traslation of the flask-login_requiered, so it asks to login in english in the spanish version
    form = SimpleForm()
    error = ""
    if form.validate_on_submit():
        if len(form.fruits_cb.data) + len(form.alco_cb.data) + len(form.nonalco_cb.data) + len(form.others_cb.data) < 2:
            error = (gettext("You must select at least two ingredients"))
            return render_template('bar/specially4you.html', form=form, error = error)
        else:

            response = [form.fruits_cb.data, form.alco_cb.data, form.nonalco_cb.data, form.others_cb.data]
            user_query = [val.lower() for sublist in response for val in sublist]
            print('USER QUERY ', user_query)


            cocktail = cocktailRecommender.get_recommendation(user_query)


            if cocktail.name is None:
                return render_template('bar/no_recommendation.html', user_query=user_query)
            else:
                return redirect(url_for('bar.cocktail', name=cocktail.name, ask_eval=True))
    return render_template('bar/specially4you.html', form=form, error=error)
