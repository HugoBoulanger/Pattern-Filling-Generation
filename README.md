# Pattern Generation

Create a directory and place a config.yml file in it (see default.yml).

Then launch using python generate.py 'directory/path'

requirements : numpy, matplotlib

Data needs to be in the following format :

BOS y a-t-il la possibilité sauna EOS	O O O O O B-hotel-services 1


with first half being the sentence surrounded by BOS and EOS, and the second half being the BIO tags with an O added at the beginning and the eventual class at the end.


Please cite : https://aclanthology.org/2020.jeptalnrecital-recital.4/

@inproceedings{boulanger2020evaluation,
  title={{\'E}valuation syst{\'e}matique d’une m{\'e}thode commune de g{\'e}n{\'e}ration (Systematic evaluation of a common generation method)},
  author={Boulanger, Hugo},
  booktitle={Actes de la 6e conf{\'e}rence conjointe Journ{\'e}es d'{\'E}tudes sur la Parole (JEP, 33e {\'e}dition), Traitement Automatique des Langues Naturelles (TALN, 27e {\'e}dition), Rencontre des {\'E}tudiants Chercheurs en Informatique pour le Traitement Automatique des Langues (R{\'E}CITAL, 22e {\'e}dition). Volume 3: Rencontre des {\'E}tudiants Chercheurs en Informatique pour le TAL},
  pages={43--56},
  year={2020}
}
