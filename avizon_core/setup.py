from setuptools import setup

setup(name='avizon_core',
      version='2.0.0',
      description='avizon main functions',
      author='maka',
      author_email='aviz@gmail.com',
      url='https://github.com/Makav3li94/avizon',
      setup_requires=['wheel'],
      install_requires=['psutil==5.9.4',
                        'redis==4.3.5',
                        'pytz==2022.6',
                        'numpy==1.24.2',
                        'python-crontab==3.0.0']
      )