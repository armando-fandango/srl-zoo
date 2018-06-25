from __future__ import print_function, division, absolute_import

import subprocess

TEST_DATA_FOLDER = "data/kuka_gym_test"
LOG_FOLDER = "logs/kuka_gym_test"

TEST_DATA_FOLDER_DUAL = "data/kuka_gym_dual_test"
NUM_EPOCHS = 1
STATE_DIM = 2
TRAINING_SET_SIZE = 2000
KNN_SAMPLES = 1000
SEED = 0


def assertEq(left, right):
    assert left == right, "{} != {}".format(left, right)


def assertNeq(left, right):
    assert left != right, "{} == {}".format(left, right)


def testPipeLine():
    # Pipeline on test config
    args = ['--data-folder', TEST_DATA_FOLDER,
            '--base-config', 'configs/test_pipeline.json']
    args = list(map(str, args))

    ok = subprocess.call(['python', 'pipeline.py'] + args)
    assertEq(ok, 0)

    args = ['--data-folder', TEST_DATA_FOLDER_DUAL,
            '--base-config', 'configs/test_pipeline_dual.json']
    args = list(map(str, args))

    ok = subprocess.call(['python', 'pipeline.py'] + args)
    assertEq(ok, 0)

    # Pipeline on baselines
    args = ['--data-folder', TEST_DATA_FOLDER,
            '--baselines',
            '--base-config', 'configs/test_pipeline.json']
    args = list(map(str, args))

    ok = subprocess.call(['python', 'pipeline.py'] + args)
    assertEq(ok, 0)

    # Test report
    args = ['-d', LOG_FOLDER]
    args = list(map(str, args))
    ok = subprocess.call(['python', 'evaluation/create_report.py'] + args)
    assertEq(ok, 0)


def testExtraSRLTrain():
    for model_type in ['resnet', 'mlp']:
        args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER,
                '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
                '--seed', SEED, '--val-size', 0.1,
                '--state-dim', STATE_DIM, '--model-type', model_type, '-bs', 128,
                '--losses', "forward", "inverse", "reward", "priors", "episode-prior", "reward-prior",
                '--l1-reg', 0.0001]
        args = list(map(str, args))

        ok = subprocess.call(['python', 'train.py'] + args)
        assertEq(ok, 0)

        # Tests for Dual camera
        for model_type in ['custom_cnn', 'mlp']:
            args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER_DUAL,
                    '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
                    '--seed', SEED, '--val-size', 0.1,
                    '--state-dim', STATE_DIM, '--model-type', model_type, '-bs', 32,
                    '--losses', "forward", "inverse", "reward", "priors", "episode-prior", "reward-prior", "triplet",
                    '--l1-reg', 0.0001,
                    '--multi-view']
            args = list(map(str, args))


def testExtraBaselineTrain():
    for baseline in ['vae', 'autoencoder']:
        # single camera
        args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER,
                '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
                '--seed', SEED, '--val-size', 0.1,
                '--state-dim', STATE_DIM, '--model-type', 'mlp', '-bs', 128,
                '--losses', baseline]
        args = list(map(str, args))

        ok = subprocess.call(['python', 'train.py'] + args)
        assertEq(ok, 0)

        # dual camera
        args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER_DUAL,
                '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
                '--seed', SEED, '--val-size', 0.1,
                '--state-dim', STATE_DIM, '--model-type', 'mlp', '-bs', 64,
                '--losses', baseline,
                '--multi-view']
        args = list(map(str, args))

        ok = subprocess.call(['python', 'train.py'] + args)
        assertEq(ok, 0)

    # Linear AE
    # single camera
    args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER,
            '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
            '--seed', SEED, '--val-size', 0.1,
            '--state-dim', STATE_DIM, '--model-type', 'linear', '-bs', 128,
            '--losses', 'autoencoder']
    args = list(map(str, args))
    # dual camera
    args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER_DUAL,
            '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
            '--seed', SEED, '--val-size', 0.1,
            '--state-dim', STATE_DIM, '--model-type', 'linear', '-bs', 64,
            '--losses', 'autoencoder',
            '--multi-view']
    args = list(map(str, args))

    ok = subprocess.call(['python', 'train.py'] + args)
    assertEq(ok, 0)


def testExtraSupervisedTrain():
    args = ['--no-plots', '--data-folder', TEST_DATA_FOLDER,
            '--epochs', NUM_EPOCHS, '--training-set-size', TRAINING_SET_SIZE,
            '--seed', SEED, '--model-type', 'mlp']
    args = list(map(str, args))

    ok = subprocess.call(['python', '-m', 'baselines.supervised'] + args)
    assertEq(ok, 0)