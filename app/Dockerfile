# No longer required since using PythonAnywhere
# However, keeping it for reference in case planning to use VPS, and using Docker for deployment


FROM tiangolo/uwsgi-nginx-flask:python3.6

# copy over our requirements.txt file
COPY requirements.txt /tmp/

# upgrade pip and install required python packages
RUN pip install -U pip
RUN pip install -r /tmp/requirements.txt

COPY ./app /app