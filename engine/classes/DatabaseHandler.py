import json
import time
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

        if config == None or root == None:
            return

        self.config   = config
        self.root     = root

        self.engine   = create_engine('sqlite:///' + \
                                      self.root + '/' + \
                                      self.config['general']['database'], 
                                      echo=False)
        Session = sessionmaker(bind=self.engine)
        self.db = Session()
        Base.Base.metadata.create_all(self.engine)
        self.db.commit()

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def saveIssue(self, data):
        if not data: return False

        i_info = {
                 "target":       data.get("target"),
                 "name":         data.get("name"),
                 "mutant_index": data.get("mutant_index"),
                 "process":      data.get("process_status")
                 }

        n_issue = Issue(job_id=data.get("job_id"),
                        time=time.time(),
                        info=json.dumps(i_info),
                        payload=data.get("request"))

        self.db.add(n_issue)
        self.db.commit()

        return True

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def loadIssues(self):
        """
        Returns a simple list of all issues in the database.
        """

        issue_list = []
        issues = self.db.query(Issue).all()
        for issue in issues:
            i_data = {
                     "id":     issue.id,
                     "job_id": issue.job_id,
                     "time":   issue.time
                     }
            issue_list.append(i_data)
        return issue_list

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def loadIssue(self, id):
        """
        Returns full details of an issues.
        """

        issue = self.db.query(Issue).filter_by(id=id).first()
        if not issue: return {}
        i_data = {
                 "id":      issue.id,
                 "job_id":  issue.job_id,
                 "time":    issue.time,
                 "info":    json.loads(issue.info),
                 "payload": issue.payload
                 }
        return i_data

    # -------------------------------------------------------------------------
    #
    # -------------------------------------------------------------------------

    def deleteIssue(self, id):
        """
        Delete an issue from the database.
        """

        issue = self.db.query(Issue).filter_by(id=id).first()
        self.db.delete(issue)
        self.db.commit()

