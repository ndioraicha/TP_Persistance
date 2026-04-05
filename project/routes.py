from flask import Blueprint, request, jsonify, render_template, redirect
from extensions import db
from models import Electeur, Candidat, Vote

main = Blueprint('main', __name__)

# Page principale
@main.route('/')
def index():
    candidats = Candidat.query.all()
    return render_template('index.html', candidats=candidats)


# Inscription
@main.route('/register', methods=['POST'])
def register():
    try:
        nom = request.form.get('nom')
        email = request.form.get('email')
        password = request.form.get('password')

        if not nom or not email or not password:
            return "❌ Tous les champs sont obligatoires"

        # vérifier si email existe déjà
        exist = Electeur.query.filter_by(email=email).first()
        if exist:
            return "❌ Email déjà utilisé"

        electeur = Electeur(nom=nom, email=email)
        electeur.set_password(password)

        db.session.add(electeur)
        db.session.commit()

        return redirect('/')

    except Exception as e:
        return f"Erreur inscription: {e}"


# Vote
@main.route('/vote', methods=['POST'])
def voter():
    try:
        electeur_id = request.form.get('electeur_id')
        candidat_id = request.form.get('candidat_id')

        if not electeur_id or not candidat_id:
            return "❌ Données manquantes"

        electeur = Electeur.query.get(electeur_id)

        if not electeur:
            return "❌ Électeur introuvable"

        if electeur.has_voted:
            return "❌ Vous avez déjà voté"

        vote = Vote(
            electeur_id=electeur_id,
            candidat_id=candidat_id
        )

        electeur.has_voted = True

        db.session.add(vote)
        db.session.commit()

        return "✅ Vote enregistré"

    except Exception as e:
        return f"Erreur vote: {e}"


# Résultats (version HTML)
@main.route('/results')
def results():
    resultats = db.session.query(
        Candidat.nom,
        db.func.count(Vote.id).label('total')
    ).outerjoin(Vote).group_by(Candidat.nom).all()

    return render_template('result.html', resultats=resultats)