import json
import sqlite3
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from classes import Base
from classes.Issue import Issue

class DatabaseHandler:

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def __init__(self, config = None, root = None, job_id = None):

        if config == None or root == None or job_id == None:
            return

        self.config   = config
        self.root     = root
        self.job_id   = job_id

        self.engine   = create_engine('sqlite:///' + \
                                      self.root + '/' + \
                                      self.config['general']['database'], 
                                      echo=False)
        Session = sessionmaker(bind=self.engine)
        db = Session()
        Base.Base.metadata.create_all(self.engine)
        db.commit()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def saveCrashDetails(self, data):
        """
        TODO: IMPLEMENT

        if not self.dbinit: return False
        stmt = "INSERT INTO issues VALUES (?, ?)"
        try:
            self.cursor.execute(stmt, (self.job_id, data))
            self.database.commit()
        except Exception, ex:
            raise Exception(ex)
        """

        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def loadCrashDetails(self):
        if not self.dbinit: return False
        issue_list = []
        """
        TODO: IMPLEMENT

        stmt = "SELECT * FROM issues"
        try:
            for issue in self.cursor.execute(stmt):
                issue_list.append(issue)
        except Exception, ex:
            raise Exception(ex)
        """
        return issue_list

