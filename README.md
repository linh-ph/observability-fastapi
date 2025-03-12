# FastAPI with observability integration
## Prerequisite

Source tìm hiểu về opentelemetry ghi log tới clickhouse. Source đang gặp khó khi cấu hình collector ánh xạ các field vào table custom (log) clickhouse (Thay vì sử dụng schema table default của otel (otel_log))

## Run instructions for sending data to SigNoz

- Create a virtual environment and activate it

```
python3 -m venv .venv
source .venv/bin/activate
```

- Change directory

```
cd app
```

- Install dependencies

```
pip install -r requirements.txt
```

- Install instrumentation packages

```
opentelemetry-bootstrap --action=install
```

- Run the app
Open container fastapi, clickhouse, collector