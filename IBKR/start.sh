cd gateway && sh bin/run.sh root/conf.yaml &
cd webapp && python3 -m venv venv && . venv/bin/activate && venv/bin/pip install -r requirements.txt
uvicorn main:app --host 0.0.0.0 --port 8000