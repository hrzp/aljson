Convert a SqlAlchemy query object to a dict(json)

Install
=======

::

    pip install aljson


Usage
=====

.. code:: python

    from aljson import BaseMixin

    # The Sqlalchemy model
    class Parent(Base, BaseMixin):
    __tablename__ = 'parent'
    id = sa.Column(sa.Integer, primary_key=True, unique=True)
    name = sa.Column(sa.String(64))

    # query Parent model

    print(result.to_json())


Full example
============

.. code:: python

    from sqlalchemy.orm import sessionmaker, relationship, backref
    from sqlalchemy.ext.declarative import declarative_base
    from aljson import BaseMixin
    import sqlalchemy as sa

    Base = declarative_base()


    class Parent(Base, BaseMixin):
        __tablename__ = 'parent'
        id = sa.Column(sa.Integer, primary_key=True, unique=True)
        name = sa.Column(sa.String(64))


    class Child(Base, BaseMixin):
        __tablename__ = 'child'
        id = sa.Column(sa.Integer,  primary_key=True, unique=True)
        name = sa.Column(sa.String(64))
        parent_id = sa.Column(sa.Integer, sa.ForeignKey('parent.id'))
        parent = relationship("Parent")


    # Create an engine that stores data in the local directory's
    # sqlalchemy_example.db file.
    engine = sa.create_engine('sqlite:///my_database.sqlite')

    # Create all tables in the engine. This is equivalent to "Create Table"
    # statements in raw SQL.
    Base.metadata.create_all(engine)

    DBSession = sessionmaker(bind=engine)
    session = DBSession()


    # Create a new parent and a child
    new_parent = Parent()
    new_parent.name = "parent_1"

    new_child = Child()
    new_child.name = "child_1"
    new_child.parent = new_parent

    session.add(new_parent)
    session.add(new_child)

    session.commit()

    # Search for a row
    query_result = session.query(Child).first()


    # And you can call .to_json
    print(query_result.to_json())

    # The result should be like this:
    # {'id': 1, 'name': 'child_1', 'parent_id': 1, 'parent': {'id': 1, 'name': 'parent_1'}}