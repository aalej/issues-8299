# Repro for issue 8299

## Versions

firebase-tools: v13.33.0<br>
python: Python 3.12.4<br>

```
Google Cloud SDK 514.0.0
beta 2025.03.07
bq 2.1.14
cloud-datastore-emulator 2.3.1
cloud-firestore-emulator 1.19.9
core 2025.03.07
gcloud-crc32c 1.0.0
gsutil 5.33
```

## Steps to reproduce

1. Run `python3.12 -m venv venv`
1. Run `. venv/bin/activate` to activate the venv
1. Run `python3.12 -m pip install -r requirements.txt` to install dependencies
1. On a separate terminal, satrt the emulator by running `gcloud emulators firestore start --host-port=127.0.0.1:10901 --database-mode=datastore-mode`
1. Run `python3.12 main.py`

```
$ python3.12 main.py
Traceback (most recent call last):
  File "/Users/USER/Desktop/firebase-tools/issues/8299/main.py", line 25, in <module>
    main()
  File "/Users/USER/Desktop/firebase-tools/issues/8299/main.py", line 21, in main
    client.reserve_ids_sequential(key, 1)
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/cloud/datastore/client.py", line 1020, in reserve_ids_sequential
    self._datastore_api.reserve_ids(
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/cloud/datastore_v1/services/datastore/client.py", line 1594, in reserve_ids
    response = rpc(
               ^^^^
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/gapic_v1/method.py", line 131, in __call__
    return wrapped_func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/retry/retry_unary.py", line 293, in retry_wrapped_func
    return retry_target(
           ^^^^^^^^^^^^^
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/retry/retry_unary.py", line 153, in retry_target
    _retry_error_helper(
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/retry/retry_base.py", line 212, in _retry_error_helper
    raise final_exc from source_exc
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/retry/retry_unary.py", line 144, in retry_target
    result = target()
             ^^^^^^^^
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/timeout.py", line 130, in func_with_timeout
    return func(*args, **kwargs)
           ^^^^^^^^^^^^^^^^^^^^^
  File "/Users/USER/Desktop/firebase-tools/issues/8299/venv/lib/python3.12/site-packages/google/api_core/grpc_helpers.py", line 78, in error_remapped_callable
    raise exceptions.from_grpc_error(exc) from exc
google.api_core.exceptions.Unknown: None
```

## Connecting to actual project

When connecting to an actual project, no errors are raised

1. Run `export GOOGLE_APPLICATION_CREDENTIALS=./service-account.json`
2. Update the Python code to something like below:

```python
import os

from google.cloud import datastore

def main():
    PORT = 10901
    # os.environ["DATASTORE_EMULATOR_HOST"] = "127.0.0.1:%s" % PORT
    os.environ["DATASTORE_PROJECT_ID"] = "PROJECT_ID"

    def get_new_client():
        return datastore.Client(
            project=os.environ.get("GCLOUDC_PROJECT_ID", "PROJECT_ID"),
            namespace=None,
            _http=None,
        )

    client = get_new_client()
    kind = "a_kind"
    key = client.key(kind, -1)

    client.reserve_ids_sequential(key, 1)


if __name__ == "__main__":
    main()
```

3. No errors raised.
