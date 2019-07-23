from pkgversion import list_requirements, pep440_version, write_setup_py
from setuptools import find_packages

write_setup_py(
    name='settings-vial',
    version=pep440_version(),
    description="Python settings for cloud environments",
    long_description=open('README.md').read(),
    author="Charles David de Moraes",
    author_email='charles.moraes@kpn.com',
    url='https://github.com/kpn/settings-vial',
    install_requires=list_requirements('requirements/requirements-base.txt'),
    packages=find_packages(exclude=['settings_vial.tests*']),
    tests_require=['tox'],
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ]
)
