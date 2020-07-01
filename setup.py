from setuptools import find_packages, setup

setup(
    name='mingdfs',
    version='1.0.0',
    url='',
    license='',
    maintainer='zswj123',
    maintainer_email='congshi.hello@gmail.com',
    description='',
    long_description='',
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "flask-session",
        "redis",
        "pillow",
        "PyMySQL",
        "gevent",
        "psutil",
        "requests",
        "pycrypto"
    ],
    entry_points = """
    [console_scripts]
    fmws = mingdfs.fmws.command:main
    frws = mingdfs.frws.command:main
    """
)
