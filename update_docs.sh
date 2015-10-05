#!/bin/bash
echo "Generating output from the examples"
for i in {basic,basic_35,selective,callables,kwargs}; do python -m docs.examples.$i > docs/examples/$i.out; done

echo "Rebuilding html docs"
cd docs
make html
