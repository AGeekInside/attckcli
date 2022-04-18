from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Table
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

matrix_to_tactic_table = Table(
    "matrix_to_tactic",
    Base.metadata,
    Column("matrix_id", ForeignKey("matrix.id"), primary_key=True),
    Column("tactic_id", ForeignKey("tactic.id"), primary_key=True),
)

tactic_to_pattern_table = Table(
    "matrix_to_tactic",
    Base.metadata,
    Column("tactic_id", ForeignKey("tactic.id"), primary_key=True),
    Column("attack_pattern_id", ForeignKey("attack_pattern.id"), primary_key=True),
)


class Matrix(Base):
    __tablename__ = "matrix"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    version = Column(String(20))
    attck_id = Column(String(75))
    tactics = relationship(
        "Tactic", secondary=matrix_to_tactic_table, back_populates="matrices"
    )


class Tactic(Base):
    __tablename__ = "tactic"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    version = Column(String(20))
    attck_id = Column(String(75))
    matrices = relationship(
        "Matrix", secondary=matrix_to_tactic_table, back_populates="tactics"
    )
    attack_patterns = relationship(
        "AttackPattern",
        secondary=tactic_to_pattern_table,
        back_populates="attack_patterns",
    )


class AttackPattern(Base):
    __tablename__ = "attack_pattern"

    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    version = Column(String(20))
    attck_id = Column(String(75))
    is_subtechnique = Column(Boolean())
    attack_patterns = relationship(
        "AttackPattern",
        secondary=tactic_to_pattern_table,
        back_populates="attack_patterns",
    )


def load_database(matrices):
    print(f"Loading ATT&CK data into the database.")

    for matrix in matrices:
        name = matrix["name"]

        id_lookup = {}
        tactics = {}
        attack_patterns = {}

        objects = matrix["objects"]
        for object in objects:
            attck_id = object["id"]
            obj_type = object["type"]
            id_lookup[attck_id] = object
            if obj_type == "x-mitre-tactic":
                tactics[attck_id] = object
            elif obj_type == "attack-pattern":
                attack_patterns[attck_id] = object

        matrix["id_lookup"] = id_lookup
        matrix["tactics"] = tactics
        matrix["attack_patterns"] = attack_patterns

        print(f"Found {len(matrix['id_lookup']):,} ids in {name} matrix.")
        print(f"Found {len(matrix['tactics']):,} tactics in {name} matrix.")
        print(
            f"Found {len(matrix['attack_patterns']):,} attack patterns in {name} matrix."
        )
