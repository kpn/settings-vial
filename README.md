# Settings Vial

Python settings for cloud environments

[![image](https://secure.travis-ci.com/kpn/settings-vial.svg?branch=master)](https://travis-ci.com/kpn/settings-vial?branch=master)
[![image](https://img.shields.io/codecov/c/github/kpn/settings-vial/master.svg)](https://codecov.io/github/kpn/settings-vial?branch=master)
[![image](https://img.shields.io/pypi/v/settings-vial)](https://pypi.python.org/pypi/settings-vial)
[![image](https://readthedocs.org/projects/settings-vial/badge/?version=latest)](https://settings-vial.readthedocs.org/en/latest/?badge=latest)

## Usage

``` shell
$ export MY_APP_TEST_VAR=42
```


``` python
>>> from settings_vial import Settings
>>> settings = Settings(env_prefix="MY_APP_")
>>> settings.load_env()
>>> setttings.TEST_VAR
42
```

## Features

- Loads prefixed environment variables (json encoded)
- Dynamic settings support (loads keys from callable instead)


## Installation

```shell
$ pip install settings_vial
```

## Running tests

```shell
$ make test
```

## Contributing

If you'd like to contribute, please follow this workflow:

1. Fork this repository
2. Clone your fork
3. Create and test your changes
4. Create a pull-request
5. Wait for review and approval from the repository collaborators

Contributions are always welcome.

## Support

If you need help or have bug reports, please file an issue in our [Issue Tracker](../../../issues).

## Versioning

This project uses SemVer 2 for versioning. For the versions available, see the tags on this repository.
