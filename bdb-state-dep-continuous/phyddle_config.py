#====================================================================#
# Default phyddle config file                                        #
#====================================================================#

args = {

    #-------------------------------#
    # Project organization          #
    #-------------------------------#
    'step'    : 'SFTEP',                   # Step(s) to run
    'verbose' : 'T',                       # print verbose phyddle output?
    'prefix'  : 'out',                     # Prefix for output for all setps
    'dir'     : './',
    'output_precision'   : 12,             # Number of digits (precision) for numbers in output files

    #-------------------------------#
    # Multiprocessing               #
    #-------------------------------#
    'use_parallel'   : 'T',                 # use multiprocessing to speed up jobs?
    'use_cuda'       : 'T',
    'num_proc'       : 30,                  # how many CPUs to use (-2 means all but 2)

    #-------------------------------#
    # Simulate Step settings        #
    #-------------------------------#
    'sim_command'       : f'python sim_bdb.py', # exact command string, argument is output file prefix
    'sim_logging'       : 'verbose',        # verbose, compressed, or clean
    'start_idx'         : 0,                # first simulation replicate index
    'end_idx'           : 100000,            # last simulation replicate index
    'sim_batch_size'    : 100,

    #-------------------------------#
    # Format Step settings          #
    #-------------------------------#
    'encode_all_sim'    : 'T',
    'num_char'          : 1,                # number of evolutionary characters
    'num_states'        : 2,                # number of states per character
    'min_num_taxa'      : 10,               # min number of taxa for valid sim
    'max_num_taxa'      : 1000,             # max number of taxa for valid sim
    'tree_width'        : 500,              # tree width category used to train network
    'tree_encode'       : 'extant',         # use model with serial or extant tree
    'brlen_encode'      : 'height_brlen',   # how to encode phylo brlen? height_only or height_brlen
    'char_encode'       : 'integer',        # how to encode discrete states? one_hot or integer
    'param_est'         : {                 # model parameters to predict (labels)
      'log10_birth_rate_0'              : 'num',
      'log10_death_rate_0'              : 'num',
      'log10_expected_burst_rate_0'     : 'num',
      'log10_expected_burst_rate_diff'  : 'num',
      'log10_state_rate_01'             : 'num',
      'root_state'                      : 'cat',
    },                                      # Model parameters and variables to estimate
    'param_data'         : {},              # Model parameters and variables treated as data
    'tensor_format'     : 'hdf5',           # save as compressed HDF5 or raw csv
    'char_format'       : 'csv',
    'save_phyenc_csv'   : 'F',              # save intermediate phylo-state vectors to file

    #-------------------------------#
    # Train Step settings           #
    #-------------------------------#
    'num_epochs'        : 200,              # number of training intervals (epochs)
    'num_early_stop'    : 3,
    'prop_test'         : 0.05,             # proportion of sims in test dataset
    'prop_val'          : 0.05,             # proportion of sims in validation dataset
    'prop_cal'          : 0.20,             # proportion of sims in CPI calibration dataset
    'cpi_coverage'      : 0.95,             # coverage level for CPIs
    'cpi_asymmetric'    : 'T',              # upper/lower ('T') or symmetric ('F') CPI adjustments
    'trn_batch_size'    : 1024,             # number of samples in each training batch
    'loss_numerical'    : 'mse',            # loss function for learning (real-valued) targets
    'optimizer'         : 'adam',           # optimizer for network weight/bias parameters

    #-------------------------------#
    # Estimate Step settings        #
    #-------------------------------#

    #-------------------------------#
    # Plot Step settings            #
    #-------------------------------#
    'plot_train_color'      : 'blue',       # plot color for training data
    'plot_test_color'       : '#714A7E',     # plot color for test data
    # 'plot_test_color'       : '#440154',     # plot color for test data
    'plot_val_color'        : 'red',        # plot color for validation data
    'plot_aux_color'        : 'green',      # plot color for input auxiliary data
    'plot_label_color'      : 'orange',     # plot color for labels (params)
    'plot_emp_color'        : 'black',      # plot color for estimated data/values
    'plot_pca_noise'        : 0.01,         # Add noise to PCA plot to dampen contrast from point values
    'plot_num_scatter'      : 100,          # Number of examples in scatter plot
 }
