import sys
import os
from setuptools import setup, find_packages
name = 'qaclassifier'
version='1.0.4'
package_dir = {name: name}

os.system('pip install git+https://git@github.com/clips/pattern.git@development#egg=Pattern')

if sys.version_info < (3, 3):
  required.append('backports.shutil_get_terminal_size')
setup(
  name=name,
  version=version,
  license='MIT',
  package_dir=package_dir
)