#!/bin/bash

cd pyvcs
black -l 100 cli.py index.py objects.py porcelain.py refs.py repo.py tree.py __init__.py __main__.py
#mypy cli.py index.py objects.py porcelain.py refs.py repo.py tree.py __init__.py __main__.py
#isort cli.py index.py objects.py porcelain.py refs.py repo.py tree.py __init__.py __main__.py
cd ..

cd tests
black -l 100 __init__.py test_index.py test_objects.py test_porcelain.py test_refs.py test_repo.py test_tree.py
#mypy __init__.py test_index.py test_objects.py test_porcelain.py test_refs.py test_repo.py test_tree.py
#isort __init__.py test_index.py test_objects.py test_porcelain.py test_refs.py test_repo.py test_tree.py
cd ..

