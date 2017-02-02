import sys
from setuptools import setup, find_packages
name = 'qaclassifier'
version='0.0.1'
package_dir = {name: name}
required=['pattern']
if sys.version_info < (3, 3):
  required.append('backports.shutil_get_terminal_size')
setup(
  name=name,
  version=version,
  license='MIT',
  package_dir=package_dir,
  install_requires=required
)