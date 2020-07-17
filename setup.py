from io import open  # for python 2.7: reading file with encoding
from os import path
from setuptools import setup, find_packages

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


setup(
    name="settings-vial",
    use_scm_version=True,
    setup_requires=["setuptools_scm"],
    description="Python settings for cloud environments",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Charles David de Moraes",
    author_email="charles.moraes@kpn.com",
    url="https://github.com/kpn/settings-vial",
    install_requires=[
        "python-dotenv>=0.10.3,<1.0.0"
    ],
    packages=find_packages(exclude=["settings_vial.tests*"]),
    tests_require=["tox"],
    include_package_data=True,
    zip_safe=False,
    license="Apache 2.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
