#!/usr/bin/env python3
"""
Script principal pour tester la définition du modèle User.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from user import Base, User

# Configuration de la base de données (remplacer par votre chaîne de connexion)
# Utilisation d'une base de données en mémoire pour le test
engine = create_engine('sqlite:///:memory:')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Exemple d'ajout d'un utilisateur
new_user = User(email='test@example.com', hashed_password='hashed_password')
session.add(new_user)
session.commit()

# Affichage des informations sur les colonnes
print(User.__tablename__)
for column in User.__table__.columns:
    print(f"{column}: {column.type}")

# Fermeture de la session
session.close()
