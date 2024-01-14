import json
from pytest_snapshot.plugin import Snapshot
from .snapshots_settings import SNAPSHOTS_DIR, ALLOW_SNAPSHOT_DELETION, SNAPSHOT_UPDATE
from rest_framework.status import HTTP_200_OK

def create_snapshot():
    return Snapshot(
        allow_snapshot_deletion=ALLOW_SNAPSHOT_DELETION,
        snapshot_update=SNAPSHOT_UPDATE,
        snapshot_dir=SNAPSHOTS_DIR,
    )
def assert_match_with_snapshot(snapshot, data, snapshot_name):
    data_str = json.dumps(data, indent=2)
    snapshot.assert_match(data_str, snapshot_name)

def snapshot_check(api_client, endpoint, snapshot_name):
    response = api_client.get(endpoint)
    assert response.status_code == HTTP_200_OK
    snapshot = create_snapshot()
    assert_match_with_snapshot(snapshot, response.data, snapshot_name)