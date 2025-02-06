import sys

from lib import Utils
from lib import ConfigLoader
from lib.logger import Log4j

if __name__ == '__main__':

    if len(sys.argv) < 3:
        print("Usage: sbdl {local, qa, prod} {load_date} : Arguments are missing")
        sys.exit(-1)

    job_run_env = sys.argv[1].upper()
    load_date = sys.argv[2]

    spark = Utils.get_spark_session(job_run_env)
    logger = Log4j(spark)

    confs = ConfigLoader.get_config(job_run_env)
    spark_confs = ConfigLoader.get_spark_conf(job_run_env)

    accounts = Utils.read_csv(spark, "test_data/accounts/account_samples.csv")
    party = Utils.read_csv(spark, "test_data/accounts/party_samples.csv")
    party_address = Utils.read_csv(spark, "test_data/accounts/address_samples.csv")



    logger.info("Finished creating Spark Session")
