import os

from google.cloud import datastore

def main():
    PORT = 10901
    os.environ["DATASTORE_EMULATOR_HOST"] = "127.0.0.1:%s" % PORT
    os.environ["DATASTORE_PROJECT_ID"] = "demo-project"

    def get_new_client():
        return datastore.Client(
            project=os.environ.get("GCLOUDC_PROJECT_ID", "demo-project"),
            namespace=None,
            _http=None,
        )

    client = get_new_client()
    kind = "a_kind"
    key = client.key(kind, -1)

    client.reserve_ids_sequential(key, 1)


if __name__ == "__main__":
    main()