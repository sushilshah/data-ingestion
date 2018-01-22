#!/usr/bin/python
import sys
import logging
import rds_config
import pymysql
import peewee as pw

rds_host  = rds_config.db_endpoint
name = rds_config.db_username
password = rds_config.db_password
db_name = rds_config.db_name
port = 3306

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:

    myDB = pw.MySQLDatabase(db_name, host=rds_host, port=3306, user=name, passwd=password)


    # conn = pymysql.connect(rds_host, user=name,
                           # passwd=password, db=db_name, connect_timeout=5)
except:
    logger.error("ERROR: Unexpected error: Could not connect to MySql instance.")
    sys.exit()

logger.info("SUCCESS: Connection to RDS mysql instance succeeded")


def lambda_handler(event, context):
    """
    This function inserts content into mysql RDS instance
    """
    class MySQLModel(pw.Model):
    """A base model that will use our MySQL database"""
    class Meta:
        database = myDB

    class User(MySQLModel):
        username = pw.CharField()
        # etc, etc


    # when you're ready to start querying, remember to connect
    try:
        myDB.connect()
        logger.info("Connected to db")
    except Exception as e:
        logger.error("Unable to connect to the DB")
    
    return "Added %d items to RDS MySQL table" %(item_count)
