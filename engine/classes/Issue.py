from Base import Base
from sqlalchemy import Column, Integer, String, Text

# -----------------------------------------------------------------------------
#
# -----------------------------------------------------------------------------

class Issue(Base):
    __tablename__ = 'issues'
    id        = Column(Integer, primary_key=True)
    job_id    = Column(String(32), unique=True)
    time      = Column(Integer)
    signum    = Column(Integer)
    sigstr    = Column(String(64))
    info      = Column(Text)
    payload   = Column(Text)
