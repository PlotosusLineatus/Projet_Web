from genomeBact.models import testClass
import os, glob, sys
from ruamel.yaml import YAML


def run():
	print("debug")
	yaml = YAML()
	yaml.register_class(testClass)

	yaml.dump([testClass('field1', "bonjour")], sys.stdout)