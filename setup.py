# Copyright 2018 Google LLC
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     https://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from setuptools import setup

setup(name='kasane',
      version='0.1',
      description='A simple kubernets deployment manager',
      url='https://github.com/google/kasane',
      author='Vladimir Pouzanov',
      author_email='farcaller@gmail.com',
      license='Apache-2',
      packages=['kasane'],
      install_requires=[
        'click',
        'ruamel.yaml',
        'requests',
        'jinja2',
        'jsonnet',
      ],
      entry_points = {
        'console_scripts': ['kasane=kasane.cmd:main'],
      },
      zip_safe=False)
