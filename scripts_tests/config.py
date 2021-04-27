# -*- coding: utf-8 -*-
"""
Prépare l’accès aux éléments du paquet `parser_irisa` dans les scripts du dossier.
"""
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from parser_irisa import page, transcription, article, strop