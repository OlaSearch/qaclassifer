import sys
from setuptools import setup, find_packages
name = 'qaclassifier'
version='1.0.0'
package_dir = {name: name}

if sys.version_info < (3, 3):
  required.append('backports.shutil_get_terminal_size')
setup(
  name=name,
  version=version,
  license='MIT',
  package_dir=package_dir,
  dependency_links=[
    'git+ssh://git@github.com/clips/pattern.git@development#egg=Pattern'
  ]
)