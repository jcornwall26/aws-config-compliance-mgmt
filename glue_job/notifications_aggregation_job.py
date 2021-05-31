import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

## @params: [JOB_NAME]
args = getResolvedOptions(sys.argv, ['JOB_NAME'])

sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args['JOB_NAME'], args)

def filter_type(item, compliance_type):
    return item['compliancetype'] == compliance_type

config_notification_datasource = glueContext.create_dynamic_frame.from_catalog(database = "default", table_name = "config_notifications", transformation_ctx = "DataSource0")

filter_for_non_compliant = Filter.apply(frame = config_notification_datasource, f = lambda item:filter_type(item, 'NON_COMPLIANT'), transformation_ctx = "filter_for_non_compliant")
filter_for_compliant = Filter.apply(frame = config_notification_datasource, f = lambda item:filter_type(item, 'COMPLIANT'), transformation_ctx = "filter_for_non_compliant")

non_compliant_repartition = filter_for_non_compliant.repartition(1)
compliant_repartition = filter_for_compliant.repartition(1)

non_compliant_data_sink = glueContext.write_dynamic_frame.from_options(frame = non_compliant_repartition, connection_type = "s3", format = "csv", connection_options = {"path": "s3://mwa-ct-lll-security-topic-noncompliant-notifications-output/vA/", "partitionKeys": []}, transformation_ctx = "non_compliant_data_sink")
compliant_data_sink = glueContext.write_dynamic_frame.from_options(frame = compliant_repartition, connection_type = "s3", format = "csv", connection_options = {"path": "s3://mwa-ct-lll-security-topic-noncompliant-notifications-output/vA/raw/", "partitionKeys": []}, transformation_ctx = "DataSinkx")

job.commit()