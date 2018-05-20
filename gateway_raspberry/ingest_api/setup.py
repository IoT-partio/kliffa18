from setuptools import setup

setup(
    name='ingest_api',
    packages=['ingest_api'],
    include_package_data=True,
    install_requires=[
        'flask', 'jsonschema'
    ],
    setup_requires=[
        'pytest-runner',
    ],
    tests_require=[
        'pytest',
    ],
)