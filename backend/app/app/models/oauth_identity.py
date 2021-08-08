from sqlalchemy import ForeignKey, Column, Integer, String, Enum, UniqueConstraint, TIMESTAMP, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base

from .enums import IdentityProviderName

class OAuthUserIdentity(Base):
    id = Column(Integer, primary_key=True, index=True)
    provider = Column(Enum(IdentityProviderName), unique=False, nullable=False)
    external_user_id = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="oauth_identities")

    created = Column(TIMESTAMP, server_default=func.now())
    updated = Column(TIMESTAMP, server_default=func.now(), onupdate=func.current_timestamp())

    __table_args__ = (
        UniqueConstraint('provider', 'external_user_id', name='_provider_external_user_id_uc'),
    )
