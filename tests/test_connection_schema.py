import pytest
from pydantic import ValidationError

from web_apps.schemas import ConnectionCreate, NodeCreate


def test_connection_create_subject_target_nodes():
    cc = ConnectionCreate(subject=NodeCreate(name="Andrew"),
                          name="has title",
                          target=NodeCreate(name="Chief Engineer"))
    assert cc
    cc_dict = cc.dict()
    assert cc_dict["name"] == "has title"
    assert cc_dict["subject"]["name"] == "Andrew"
    assert cc_dict["target"]["name"] == "Chief Engineer"


def test_connection_create_subject_target_ids():
    cc = ConnectionCreate(subject=1,
                          name="has title",
                          target=2)
    assert cc
    cc_dict = cc.dict()
    assert cc_dict["name"] == "has title"
    assert cc_dict["subject"] == 1
    assert cc_dict["target"] == 2


def test_connection_create_no_subject():
    with pytest.raises(ValidationError) as error:
        cc = ConnectionCreate(name="has title", target=2)
        assert cc
    pass
