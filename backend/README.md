## How to run backend

Get database access in .env

1. Install dependencies

```
pip install -r requirements.txt
```

2. Run 

```
uvicorn main:app --host 0.0.0.0 --port 8082
```