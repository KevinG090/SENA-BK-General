from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Column,
    Integer,
    String,
    create_engine,
    text,
    BigInteger,
    ForeignKey,
)


Base = declarative_base()


class ModelBase(Base):
    __abstract__ = True

    def to_dict(self, exclude_columns: list = []):
        return {
            c.name: getattr(self, c.name)
            for c in self.__table__.columns
            if not c.name in exclude_columns
        }


class Usuario(ModelBase):
    __tablename__ = "tbl_usuarios"

    pk_id_usuario = Column(Integer, primary_key=True)
    nombre_usuario = Column(String)
    nombre_usuario = Column(String)
    celular = Column(BigInteger)
    correo = Column(String)
    identificacion = Column(BigInteger)
    contraseña = Column(String)
    observaciones = Column(String)
    fk_id_tipo_usuario = Column(
        Integer, ForeignKey("tbl_tipo_usuarios.pk_id_tipo_usuario")
    )
