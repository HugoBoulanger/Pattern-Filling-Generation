# Pattern Generation

Create a directory and place a config.yml file in it (see default.yml).

Then launch using python generate.py 'directory/path'

requirements : numpy, matplotlib

Data needs to be in the following format :

BOS y a-t-il la possibilité sauna EOS	O O O O O B-hotel-services 1


with first half being the sentence surrounded by BOS and EOS, and the second half being the BIO tags with an O added at the beginning and the eventual class at the end.