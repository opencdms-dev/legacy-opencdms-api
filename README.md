# opencdms-server

OpenCDMS server uses Python FastAPI to expose a web interface for `opencdms-app` and other applications.

```
# create a virtual environment

$ pip install -r requirements.txt
$ export DATABASE_URI=connection_string
$ python main.py
```

Visit http://localhost:5000/docs for interactive API docs.
