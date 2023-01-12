from src.extraction import *
from src.full_extraction import *
from src.generator import *
from src.patterns import *
from config import GenerationConfig
from pathlib import Path, PosixPath


import argparse


def run_generation(args):
    """
    Generation function using the previous generation functions
    """

    cfg = GenerationConfig(args.dir / 'config.yml')

    if cfg.generation.do_extraction:
        if not os.path.exists(args.dir / 'extracted'):
            os.mkdir(str(args.dir / 'extracted'))

        extract(str(args.dir / 'extracted'), cfg.generation.dataset.train_file, None)

    generator = Algo1(str(args.dir / 'extracted/patterns_None.txt'), str(args.dir / 'extracted/lists_None.txt'), with_intent=False, seed=cfg.generation.seed)

    generated = generator.generate_corpus(size=cfg.generation.size)
    f = open(cfg.generation.save_dir / f'{cfg.generation.size // 1000}k.trn', 'w')
    f.writelines(generated)
    f.close()



if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("dir", type=str, help="str. Directory where a config file is found")
    args = parser.parse_args()

    args.dir = Path(args.dir)
    run_generation(args)