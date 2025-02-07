import sys
import uuid

from pyspark.sql.functions import col, to_json, struct

from lib import Utils
from lib import ConfigLoader
from lib.logger import Log4j
from lib import DataLoader
from lib import Transformations

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: sbdl {local, qa, prod} {load_date} : Arguments are missing")
        sys.exit(-1)

    job_run_env = sys.argv[1].upper()
    load_date = sys.argv[2]
    job_run_id = "SBDL-" + str(uuid.uuid4())

    print("Initialising SBDL job in" + job_run_env + "Job ID:" + job_run_id)
    conf = ConfigLoader.get_config(job_run_env)
    enable_hive = True if conf["enable.hive"] == "true" else False
    hive_db = conf["hive.database"]

    print("Creating Spark session")
    spark = Utils.get_spark_session(job_run_env)

    logger = Log4j(spark)

    logger.info("Reading SBDL Account DF")
    accounts_df = DataLoader.read_accounts(spark, job_run_env, enable_hive, hive_db)
    contract_df = Transformations.get_contract(accounts_df)

    logger.info("Reading SBDL Party DF")
    parties_df = DataLoader.read_parties(spark, job_run_env, enable_hive, hive_db)
    relations_df = Transformations.get_relations(parties_df)

    logger.info("Reading SBDL Address DF")
    address_df = DataLoader.read_address(spark, job_run_env, enable_hive, hive_db)
    relation_address_df = Transformations.get_address(address_df)

    logger.info("Joining Party Relations and Address")
    party_address_df = Transformations.join_party_address(relations_df, relation_address_df)

    logger.info("Joining Account and Parties")
    data_df = Transformations.join_contract_party(contract_df, party_address_df)

    logger.info("Applying Header and Create Event")
    final_df = Transformations.apply_header(spark, data_df)

    #To send DF to kafka, must be two columns only, as a key-value pair and in JSON format
    logger.info("Preparing to send data to Kafka")
    kafka_kv_df = final_df.select(col("payload.contractIdentifier.newValue").alias("key"), to_json(struct("*")).alias("value"))


    spark_confs = ConfigLoader.get_spark_conf(job_run_env)




    logger.info("Finished creating Spark Session")
