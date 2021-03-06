#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
"""
Helpers to perform system tests for the Google Cloud Build service.
"""
import argparse

from airflow.gcp.example_dags.example_bigquery import DATA_EXPORT_BUCKET_NAME
from tests.contrib.utils.gcp_authenticator import GcpAuthenticator, GCP_CLOUD_BUILD_KEY
from tests.contrib.utils.logging_command_executor import LoggingCommandExecutor


class GCPBigQueryTestHelper(LoggingCommandExecutor):
    """
    Helper class to perform system tests for the Google BigQuery service.
    """

    def create_repository_and_bucket(self):
        """Create a bucket."""
        self.execute_cmd(["gsutil", "mb", "gs://{}".format(DATA_EXPORT_BUCKET_NAME)])

    def delete_bucket(self):
        """Delete bucket in Google Cloud Storage service"""

        self.execute_cmd(["gsutil", "rb", "gs://{}".format(DATA_EXPORT_BUCKET_NAME)])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Create and delete bucket for system tests.")
    parser.add_argument(
        "--action",
        dest="action",
        required=True,
        choices=("create-bucket", "delete-bucket", "before-tests", "after-tests"),
    )
    action = parser.parse_args().action

    helper = GCPBigQueryTestHelper()
    gcp_authenticator = GcpAuthenticator(GCP_CLOUD_BUILD_KEY)
    helper.log.info("Starting action: %s", action)

    gcp_authenticator.gcp_store_authentication()
    try:
        gcp_authenticator.gcp_authenticate()
        if action == "before-tests":
            pass
        elif action == "after-tests":
            pass
        elif action == "create-bucket":
            helper.create_repository_and_bucket()
        elif action == "delete-bucket":
            helper.delete_bucket()
        else:
            raise Exception("Unknown action: {}".format(action))
    finally:
        gcp_authenticator.gcp_restore_authentication()

    helper.log.info("Finishing action: %s", action)
