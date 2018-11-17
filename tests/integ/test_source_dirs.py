# Copyright 2018 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.
from __future__ import absolute_import

import os

from sagemaker.pytorch.estimator import PyTorch
from tests.integ import DATA_DIR, PYTHON_VERSION, TRAINING_DEFAULT_TIMEOUT_MINUTES
from tests.integ.timeout import timeout


def test_source_dirs(sagemaker_session, tmpdir):
    source_dir = os.path.join(DATA_DIR, 'pytorch_source_dirs')
    lib = os.path.join(str(tmpdir), 'alexa.py')

    with open(lib, 'w') as f:
        f.write('def question(to_anything): return 42')

    instance_type = 'local'
    with timeout(minutes=TRAINING_DEFAULT_TIMEOUT_MINUTES):
        estimator = PyTorch(entry_point='train.py', role='SageMakerRole', source_dir=[source_dir, lib],
                            py_version=PYTHON_VERSION, train_instance_count=1, train_instance_type=instance_type)

        estimator.fit()

        predictor = estimator.deploy(initial_instance_count=1, instance_type=instance_type)

        predict_response = predictor.predict([24])

        assert predict_response == [24]
