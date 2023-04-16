from pydantic import BaseModel


class ItemBase(BaseModel):
    title: str
    description: str | None = None


class ItemCreate(ItemBase):
    pass


class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool
    items: list[Item] = []

    class Config:
        orm_mode = True


class NodeBase(BaseModel):
    name: str


class NodeCreate(NodeBase):
    pass


class Node(NodeBase):
    id: int

    class Config:
        orm_mode = True


class ConnectionBase(BaseModel):
    name: str


class ConnectionCreate(ConnectionBase):  # this is the info needed to create a connection
    # we need either a node name to create or an existing node id
    subject: NodeCreate | int
    target: NodeCreate | int


class Connection(ConnectionBase):  # this is a fully-populated valid connection from the database
    id: int
    subject: Node
    target: Node

    class Config:
        orm_mode = True
