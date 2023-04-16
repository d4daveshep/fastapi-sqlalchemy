import pytest
from sqlalchemy import create_engine, select, update, delete
from sqlalchemy.orm import Session

from sql_app import models, crud
from sql_app.models import Node
from sql_app.schemas import NodeCreate


@pytest.fixture()
def db_session():
    engine = create_engine("sqlite://", echo=True)

    models.Base.metadata.create_all(engine)

    with Session(engine) as session:
        yield session

        pass


@pytest.fixture()
def session_with_3_nodes(db_session):
    andrew = Node(name="Andrew Lindesay")
    david = Node(name="David Rawson")
    robin = Node(name="Robin Southgate")
    db_session.add_all([andrew, david, robin])
    db_session.commit()

    yield db_session


def test_create_node(db_session):
    name = "Chris Callahan"
    node = crud.create_node(db_session, NodeCreate(name=name))
    assert node.name == name
    assert node.id


def test_get_node_by_id(session_with_3_nodes):
    node = crud.get_node(session_with_3_nodes, 2)
    assert node.name == "David Rawson"

    node = crud.get_node(session_with_3_nodes, 99)
    assert not node


def test_get_node_by_name(session_with_3_nodes):
    node = crud.get_node_by_name(session_with_3_nodes, "David Rawson")
    assert node.name == "David Rawson"


def test_get_nodes(session_with_3_nodes):
    nodes = crud.get_nodes(session_with_3_nodes)
    assert len(nodes) == 3


def test_get_node_like_name(session_with_3_nodes):
    nodes = crud.get_nodes_like_name(session_with_3_nodes,like="robin")
    assert len(nodes) == 1
    robin = nodes[0]
    assert robin.name == "Robin Southgate"



def test_update_node(session_with_3_nodes):
    update_stmt = update(Node).where(Node.name.ilike("%andrew%")).values(name="Andy Linde")
    result = session_with_3_nodes.execute(update_stmt)
    assert result.rowcount == 1

    select_stmt = select(Node).where(Node.name.contains("Andy"))
    andy = session_with_3_nodes.scalars(select_stmt).one()
    assert andy.name == "Andy Linde"


def test_delete_node(session_with_3_nodes):
    delete_stmt = delete(Node).where(Node.name.ilike("%david%"))
    result = session_with_3_nodes.execute(delete_stmt)
    assert result.rowcount == 1

    select_stmt = select(Node)
    assert len(session_with_3_nodes.scalars(select_stmt).all()) == 2
