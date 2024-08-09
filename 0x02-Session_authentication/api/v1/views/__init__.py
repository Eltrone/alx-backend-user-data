#!/usr/bin/env python3
"""Initialise les vues de l'API avec Blueprint pour les routes '/api/v1'."""

from flask import Blueprint

# Blueprint pour les vues de l'API, préfixé par '/api/v1'.
app_views = Blueprint("app_views", __name__, url_prefix="/api/v1")

# Importe les vues pour les endpoints index et users.
from api.v1.views.index import *
from api.v1.views.users import *

# Charge les données utilisateur depuis un fichier.
User.load_from_file()
