# README

## basic

These files created by ZHANG PENG, used to test PM-CD algorithm. For example in `./10-0.1 branin` folder, there has:

1. `cdcop_random_bird 10-0.1.yaml` file: imitate from `cdcop_bird_func.yaml` file in dbay algorithm, modified the agents and constraints to adopt the PM-CD algo.
2. 12 files named like `branin_constraint copy XXX.py`: in PM-CD algo, each constraint between two agents has a unique function description. So there are 12 constraints in the `10-0.1 branin` example, i imitate 12 copys from `branin_constraint.py` file in dbay algorithm.

`./10-0.6 branin` folder is similar to `./10-0.1 branin` folder, but diffs in the kind of graph chosed. 

## another question

I have no idea why i run pydcop so slow. My algo needs a collection of more than 50 agents and about 1500 constraints. i store the template files in `./100-0.6` folder. When i run it, my machine run time out and crush after 5 hours, but there is no result. I guess it went wrong, i'm confused if there is somewhere i write a wrong config?

