from setuptools import setup, find_packages

setup(
    name='nps-downloader',
    version='1.0.0',

    description="Downloads NPS data from the Promoter.io API to local files",

    install_requires=[
        'requests>=2.19.1',
        'click>=6.0',
        'wheel>=0.29'
    ],

    packages=find_packages(),

    author='Jose Rolland & Javier Crespo',
    license='MIT',

    entry_points={
        'console_scripts': [
            'download-nps-data=nps_downloader.cli:download_data'
        ]
    }
)
