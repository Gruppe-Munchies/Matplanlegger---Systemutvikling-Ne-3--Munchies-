from flask import Blueprint, render_template, session, request, redirect
from flask_login import current_user


from backend.auth.forms import LoginForm, UserGroupSelector
from backend.auth.queries import fetchAllUserGroupsUserHas

mainpage = Blueprint('mainpage', __name__, static_folder="static", template_folder="templates")


@mainpage.route('/')
def index():
    print(session.get('key'))
    form = LoginForm()
    # print(f"current user: {current_user}")
    is_logged_in = False
    print(session.get('group_to_use'))
    # TODO: Må vell legge inn usertype pr group i profilsiden egentlig.
    groups = fetchAllUserGroupsUserHas(current_user.id)
    # TODO:Bør flyttes til nav

    form = UserGroupSelector(request.form)
    # choice = [(0,"Velg gruppe å samhandle som")]
    choice = []

    for i in fetchAllUserGroupsUserHas(current_user.id):
        choice.append((i.iduserGroup, i.groupName))

    form.idOgNavn.choices = choice

    if request.method == 'POST' and form.validate():
        selectFieldGroup = form.idOgNavn.data  # Får tilbake group_id her

        # oppdaterer den halvglobale verdien
        # backend.auth.views.current_group = selectFieldGroup
        session['group_to_use'] = selectFieldGroup
        return redirect(request.referrer)
    #########   Slutt valg av group    #############
    form.idOgNavn.data = session.get('group_to_use', 0)  # setter standard til den aktive
    return render_template('index.html', form=form, groups=groups )


