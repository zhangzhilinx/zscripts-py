from setuptools import setup

setup(
    name="zscripts",
    version="0.0.2",
    keywords="scripts",
    description="ZhangZhilin's personal scripts",
    long_description="A set of scripts for my personal use.",
    license="MPLv2",

    url="https://github.com/zhangzhilinx",
    author="ZhangZhilin",
    author_email="corex_public@outlook.com",

    # packages=find_packages(),
    packages=['zscripts', 'zscripts.cmds'],
    include_package_data=True,
    platforms="any",
    install_requires=[
        'argparse>=1.1',
        'numpy>=1.12.0',
        'opencv-contrib-python>=4.2.0',
        'pywin32>=226'
    ],

    # scripts=[],
    entry_points={
        'console_scripts': [
            'zsp = zscripts:main'
        ]
    }
)
