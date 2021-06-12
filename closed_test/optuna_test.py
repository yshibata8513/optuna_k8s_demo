
import optuna
import numpy as np
import subprocess


def objective(trial):
    v = trial.suggest_uniform('v', 5., 15.)
    delta = trial.suggest_uniform('delta', 0.001, 0.05)

    cmd = "./a.out " + "localhost " + str(v) + " " + str(delta)
    d = subprocess.check_output(cmd.split())
    return float(d)


def main():

    # optimize
    study = optuna.create_study(
        study_name="closed_test"
    )

    study.optimize(objective, n_trials=100, n_jobs=1)
    print(study.best_trial)

if __name__ == '__main__':
    main()