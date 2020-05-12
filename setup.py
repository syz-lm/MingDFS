from setuptools import find_packages, setup

setup(
    name='mingdfs',
    version='1.0.0',
    url='',
    license='',
    maintainer='zswj123',
    maintainer_email='l2se@sina.cn',
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
        "gevent"
    ],
    entry_points = """
    [console_scripts]
    fmws = mingdfs.fwms.apps:main
    frws = mingdfs.frws.apps:main
    """
)
