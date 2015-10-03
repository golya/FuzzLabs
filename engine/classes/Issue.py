from Base import Base
from sqlalchemy import Column, Integer, String, Text

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Issue(Base):
    __tablename__ = 'issues'
    id        = Column(Integer, primary_key=True)
    job_id    = Column(String(32))
    time      = Column(Integer)
    info      = Column(Text)
    payload   = Column(Text)
