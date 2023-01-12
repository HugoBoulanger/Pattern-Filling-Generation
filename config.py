

from pathlib import Path, PosixPath
from typing import Union, Text

import yaml

from box import Box


class GenerationConfig:
    """
    Dot-based access to configuration parameters saved in a YAML file.
    """
    def __init__(self, file: Union[Path, Text]):
        """
        Load the parameters from the YAML file.
        If no path are given in the YAML file for bert_checkpoint and seqeval, the corresponding objects will be load
        if used (needs an internet connection).
        """
        self.file = file
        # get a Box object from the YAML file
        with open(str(file), 'r') as ymlfile:
            cfg = Box(yaml.safe_load(ymlfile), default_box=True, default_box_attr=None)

        # manually populate the current Config object with the Box object (since Box inheritance fails)
        for key in cfg.keys():
            setattr(self, key, getattr(cfg, key))

        self.generation.dataset.train_file = file.parent / Path(self.generation.dataset.train_file)

        self.generation.save_dir = file.parent / Path(self.generation.save_dir)

        #self.seed = getattr(self.train, "seed", None)


    def save(self):
        # print([a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))])
        d = {}
        for attr, value in self.__dict__.items():
            print(attr, value, type(value))
            if type(value) == Box:
                d[attr] = {}
                for k, v in value.items():
                    if type(v) in [Path, PosixPath]:
                        d[attr][k] = str(v.relative_to(self.file.parent))
                    else:
                        d[attr][k] = v

        cfg_w = Box(d)
        cfg_w.to_yaml(filename=self.file)
