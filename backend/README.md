# Backend API for a restaurant

This API was developed using Python 3.6+ and the framework FastAPI.

## Files structre

```
├── LICENSE
├── main.py
├── README.md
├── requirements.txt
├── database
│   ├── __init__.py
│   ├── __init__.py
│   └── models.py
├── routers
│   ├── __init__.py
│   ├── orders.py
│   └── products.py
├── tests
│   ├── __init__.py
│   └── test_main.py
└── schemas
    ├── __init__.py
    ├── employe.py
    ├── orders.py
    ├── product.py
    └── table.py
```

## Instructions

This is a simple project in Python, but you need a few dependencies to run it. If you want to run the project follow the instructions below:

### 1. Project setup and install requirements

```
python3 -m venv <environtment_name>
source <environtment_name>/bin/activate
pip install -r requirements.txt
```
> Note: you need to have ``pip`` installed on your computer in order to install the requirements of the project, if you don't have it please go to this [link](https://pip.pypa.io/en/stable/cli/pip_install/) to install it.

### 2. Run the code

```
uvicorn main:app --host <host> --port <port> --reload
```

>Note: you can use any host and port, but remember specifically use these in calls to the API.
