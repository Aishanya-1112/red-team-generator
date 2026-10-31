# Red-team generator local demo

This project calls a prompt-generation HTTP service and converts its response
to an Excel report. The included `backend_stub.py` provides a local service
for testing the pipeline before the real backend is available.

## Run the stub

From this directory, create a virtual environment and install dependencies:

```powershell
py -3 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m uvicorn backend_stub:app --port 8000
```

The API documentation is available at <http://localhost:8000/docs>.

## Run the client locally

In another terminal:

```powershell
python scripts\call_service.py --input-one "demo application" --input-two "prompt injection"
python scripts\to_excel.py output\prompts.json output\prompts.xlsx
```

Both scripts return a non-zero exit code and print an error when the service
or input data is invalid.

## Run with Jenkins

Create a Jenkins Pipeline job pointing at this Git repository and select
**Pipeline script from SCM**. The `Jenkinsfile` exposes `INPUT_ONE`,
`INPUT_TWO`, and `SERVICE_URL` parameters and archives the generated JSON and
Excel files. For Jenkins running in Docker, the default service URL uses
`host.docker.internal`; for a native Windows Jenkins installation, use
`http://localhost:8000/generate`.
