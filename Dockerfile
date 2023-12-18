
# base image
FROM python:3.8

# copy requirements file and install dependencies in the container
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy the (re)sources to the /fakebook directory in the container
# COPY . fakebook
COPY ./src /fakebook/src
COPY ./static_cdn/static_root /fakebook/static_cdn/static_root
COPY ./config /fakebook/config
COPY ./data.template /fakebook/data.template

# Collect static files
RUN python /fakebook/src/manage.py collectstatic --noinput

# set working directory for application inside the container
WORKDIR /fakebook

# run the manage.py script on container run
ENTRYPOINT [ "python", "src/manage.py" ]

# start server, bind to all interfaces, port 8000, this port may be exposed to something else using docker / compose
CMD [ "runserver", "0.0.0.0:8000" ]