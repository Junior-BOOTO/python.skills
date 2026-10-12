"""Un seul lancement, sans transfert manuel : collecte, analyse, modèle."""
import sys
from collecter import main as collect
from analyser_modeliser import main as model
if __name__=='__main__':
    collect('--refresh' in sys.argv)
    model()
