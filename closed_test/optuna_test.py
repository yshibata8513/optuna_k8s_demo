
import optuna
import numpy as np
import subprocess
import os


def objective(trial):
    v = trial.suggest_uniform('v', 5., 15.)
    delta = trial.suggest_uniform('delta', 0.001, 0.05)

    cmd = "./a.out " + "localhost " + str(v) + " " + str(delta)
    d = subprocess.check_output(cmd.split())
    return float(d)


def main():



    study = optuna.load_study(
        study_name="closed_test",
        storage="postgresql://{}:{}@{}:5432/{}".format(
            os.environ["POSTGRES_USER"],
            os.environ["POSTGRES_PASSWORD"],
            os.environ["POSTGRES_ENDPOINT"],
            os.environ["POSTGRES_DB"],
        ),
    )
    study.optimize(objective, n_trials=20)
    print(study.best_trial)

if __name__ == '__main__':
    main()