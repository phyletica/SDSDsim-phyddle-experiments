#!/usr/bin/env python

import sys
import os
import math
import numpy as np
import scipy.stats as st

import sdsdsim.model


class FixedRV(object):
    def __init__(self, x):
        self.x = x

    def rvs(self, *args, **kwargs):
        return self.x


class Priors(object):
    def __init__(
        self,
        state_rate = FixedRV(0.00001),
        log_birth_rate = st.uniform(-2.0, 2.0),
        log_death_rate_prop = st.uniform(-2.0, 2.0),
        burst_rate_prop = st.uniform(0.2, 0.8),
        burst_prob = st.uniform(0.4, 0.6),
        model = st.uniform(0, 1),
    ):
        self.state_rate = state_rate
        self.log_birth_rate = log_birth_rate
        self.log_death_rate_prop = log_death_rate_prop
        self.burst_rate_prop = burst_rate_prop
        self.burst_prob = burst_prob
        self.model = model 


def draw_bdb_model(priors, rng):
    # log_state_rate = priors.log_state_rate.rvs(size = None, random_state = rng)
    state_rate = priors.state_rate.rvs(size = None, random_state = rng)

    log_birth_rate_0 = priors.log_birth_rate.rvs(size = None, random_state = rng)
    birth_rate_0 = 10**log_birth_rate_0

    log_birth_rate_1 = log_birth_rate_0
    birth_rate_1 = birth_rate_0

    log_death_rate_mult = priors.log_death_rate_prop.rvs(size = None, random_state = rng)
    death_rate_mult = 10**log_death_rate_mult
    death_rate = min([birth_rate_0, birth_rate_1]) * death_rate_mult

    burst_rate_mult = priors.burst_rate_prop.rvs(size = None, random_state = rng)
    burst_rate = min([birth_rate_0, birth_rate_1]) * burst_rate_mult
    
    burst_prob = priors.burst_prob.rvs(size = None, random_state = rng)

    model = sdsdsim.model.SDSDModel(
        q = [
            [ -state_rate,  state_rate ],
            [  state_rate, -state_rate ],
        ],
        birth_rates = [birth_rate_0, birth_rate_1],
        death_rates = [death_rate, death_rate],
        burst_rate = burst_rate,
        burst_probs = [burst_prob, burst_prob],
        burst_furcation_poisson_means = [1.0, 1.0],
        burst_furcation_poisson_shifts = [2, 2],
        only_bifurcate = True,
    )
    return model

def parse_cli_args():
    out_path     = sys.argv[1]
    prefix       = sys.argv[2]
    sim_idx      = int(sys.argv[3])
    batch_size   = int(sys.argv[4])
    return out_path, prefix, sim_idx, batch_size

def stream_tip_states(out_stream, root, all_zeros = False):
    out_stream.write("taxa,data\n")
    for leaf in root.leaf_iter():
        if all_zeros:
            out_stream.write(f"{leaf.label},0\n")
        else:
            out_stream.write(f"{leaf.label},{leaf.leafward_state}\n")

def write_tip_states(path, root, all_zeros = False):
    with open(path, 'w') as out_stream:
        stream_tip_states(out_stream, root, all_zeros)

def stream_variables(out_stream, var_dict):
    names = list(sorted(var_dict.keys()))
    header = ",".join(names)
    vals = ",".join(str(var_dict[n]) for n in names)
    out_stream.write(f"{header}\n{vals}\n")

def write_variables(path, var_dict):
    with open(path, 'w') as out_stream:
        stream_variables(out_stream, var_dict)

def get_model_parameters(sdsd_model):
    return {
        'state_rate_01'         : sdsd_model.ctmc.q[0][1],
        'state_rate_10'         : sdsd_model.ctmc.q[1][0],
        'birth_rate_0'          : sdsd_model.birth_rates[0],
        'birth_rate_1'          : sdsd_model.birth_rates[1],
        'death_rate_0'          : sdsd_model.death_rates[0],
        'death_rate_1'          : sdsd_model.death_rates[1],
        'burst_rate'            : sdsd_model.burst_rate,
        'burst_prob_0'          : sdsd_model.burst_probs[0],
        'burst_prob_1'          : sdsd_model.burst_probs[1],
        'expected_burst_rate_0' : sdsd_model.burst_rate * sdsd_model.burst_probs[0],
        'expected_burst_rate_1' : sdsd_model.burst_rate * sdsd_model.burst_probs[1],
    }

def get_log10_model_parameters(sdsd_model):
    p = {}
    for k, v in get_model_parameters(sdsd_model).items():
        p[f'log10_{k}'] = math.log10(v)
    return p

def main():
    out_path, prefix, start_idx, batch_size = parse_cli_args()
    if not os.path.exists(out_path):
        os.mkdir(out_path)

    path_prefix = os.path.join(out_path, prefix)

    rng = np.random.default_rng(start_idx)

    root_state = 0
    priors = Priors()

    include_root_annotations = False
    keep_extinct_trees = False
    max_extant_leaves = 500
    tree_width = 500
    max_total_leaves = None
    max_extinct_leaves = None
    max_time = None
    max_leaves_strict = True
    # Phyddle does this according to the tree_encode config setting
    prune_extinct_leaves = False

    # Output everything and control use of variables with Phyddle config
    label_names = [
        'log10_state_rate_01',
        'log10_state_rate_10',
        'log10_birth_rate_0',
        'log10_birth_rate_1',
        'log10_death_rate_0',
        'log10_death_rate_1',
        'log10_burst_rate',
        'log10_burst_prob_0',
        'log10_burst_prob_1',
        'log10_expected_burst_rate_0',
        'log10_expected_burst_rate_1',
    ]

    sim_idx = start_idx

    while sim_idx < (start_idx + batch_size):
        sim_path_prefix = f'{path_prefix}.{sim_idx}'
        tree_path = f'{sim_path_prefix}.tre'
        data_path = f'{sim_path_prefix}.dat.csv'
        labels_path = f'{sim_path_prefix}.labels.csv'

        model = draw_bdb_model(priors, rng)

        seed = rng.random()

        survived, root, burst_times = sdsdsim.model.sim_SDSD_tree(
            rng_seed = seed,
            sdsd_model = model,
            root_state = root_state,
            max_extant_leaves = max_extant_leaves,
            max_extinct_leaves = max_extinct_leaves,
            max_total_leaves = max_total_leaves,
            max_time = max_time,
        )

        if (not survived) and (not keep_extinct_trees):
            continue
        if max_leaves_strict:
            if (max_total_leaves and (root.number_of_leaves > max_total_leaves)):
                sys.stderr.write(
                    f"max_total_leaves is {max_total_leaves} and final shared event resulted "
                    f"in {root.number_of_leaves} leaves...\n"
                    f"\tDiscarding this simulation!\n"
                )
                continue
            if (max_extant_leaves and (root.number_of_extant_leaves > max_extant_leaves)):
                sys.stderr.write(
                    f"max_extant_leaves is {max_extant_leaves} and final shared event resulted "
                    f"in {root.number_of_extant_leaves} leaves...\n"
                    f"\tDiscarding this simulation!\n"
                )
                continue
            if (max_extinct_leaves and (root.number_of_extinct_leaves > max_extinct_leaves)):
                # This should never happen, but putting logic in place in case
                # we ever decide to allow shared extinction events
                sys.stderr.write(
                    f"max_extinct_leaves is {max_extinct_leaves} and final shared event resulted "
                    f"in {root.number_of_extinct_leaves} leaves...\n"
                    f"\tDiscarding this simulation!\n"
                )
                continue

        assert root.number_of_extant_leaves == tree_width

        if prune_extinct_leaves:
            tree = tree.prune_extinct_leaves()

        log10_variables = get_log10_model_parameters(model)
        reduced_log10_variables = log10_variables
        if label_names:
            reduced_log10_variables = {k : log10_variables[k] for k in label_names}
        write_variables(labels_path, reduced_log10_variables)
        write_tip_states(data_path, root, all_zeros = True)
        with open(tree_path, 'w') as out_stream:
            root.write_newick_simple(
                out_stream,
                include_root_annotations = include_root_annotations,
            )
            out_stream.write(";\n")
        sim_idx += 1

if __name__ == '__main__':
    main()
