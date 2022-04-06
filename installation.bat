@echo off


:start
cls

set python_ver=310

python ./get-pip.py

cd \
cd \python%python_ver%\Scripts\
pip install numpy
pip install flask
pip install dash
pip install snscrape
pip install plotly
pip install dash-bootstrap-components
pip install datetime
pip install threaded
pip install whitenoise

exit