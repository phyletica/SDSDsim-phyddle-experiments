#! /usr/bin/env python

import sys
import os
import argparse
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import gridspec
import seaborn as sns
import pandas as pd


def data_frame_iter(csv_paths, **kwargs):
    """
    A generator function that, given an iterable of path to tabular data files,
    yields tuples of (path, pandas dataframe). All keyword args are given to
    `pandas.read_csv` when parsing the data file.
    """
    for p in csv_paths:
        yield p, pd.read_csv(p, **kwargs)

def concat_data_frames(csv_paths, **kwargs):
    """
    Given an iterable of paths to tabular data files, returns a single pandas
    dataframe of all the data concatenated together.  All keyword args are
    given to `pandas.read_csv` when parsing the data.
    """
    df_iter = (df for path, df in data_frame_iter(csv_paths, **kwargs))
    return pd.concat(df_iter, ignore_index = True)

def plot_int_histo(
    int_values,
    stat = 'proportion',
    xlabel = None,
    ylabel = None,
    title = None,
):
    fig = matplotlib.figure.Figure()
    gs = fig.add_gridspec(1, 1,
            wspace = 0.0,
            hspace = 0.0)
    ax = fig.add_subplot(gs[0, 0])
    plot_int_histo_on_ax(ax, int_values, stat, xlabel, ylabel, title)
    return fig, gs, ax

def plot_int_histo_on_ax(
    ax,
    int_values,
    stat = 'proportion',
    xlabel = None,
    ylabel = None,
    title = None,
    color = '#714A7E',
):
    sns.histplot(data = int_values, discrete = True, stat = stat, ax = ax, color = color)
    if xlabel:
        ax.set_xlabel(xlabel)
    if ylabel:
        ax.set_ylabel(ylabel)
    if title:
        ax.set_title(title)
    xticks = list(range(min(int_values), max(int_values) + 1))
    ax.set_xticks(xticks)
    ax.set_xticklabels(xticks)
    return

def arg_is_dir(path):
    """
    Returns the passed string if it is a valid path to a directory.
    Otherwise raises an `ArgumentTypeError`.

    Examples
    --------
    >>> d = os.path.abspath(os.path.dirname(__file__))
    >>> returned = arg_is_dir(d)
    >>> returned == d
    True
    """
    if os.path.isdir(path):
        return path
    raise argparse.ArgumentTypeError('{0!r} is not a directory'.format(path))

def arg_is_file(path):
    """
    Returns the passed string if it is a valid path to a file.
    Otherwise raises an `ArgumentTypeError`.

    Examples
    --------
    >>> p = os.path.abspath(__file__)
    >>> returned = arg_is_file(p)
    >>> returned == p
    True
    """
    if os.path.isfile(path):
        return path
    raise argparse.ArgumentTypeError('{0!r} is not a file'.format(path))

def main():
    sns.set_theme(context = "talk", style = "ticks", palette = "colorblind")

    parser = argparse.ArgumentParser()
    parser.add_argument(
        'count_path',
        type = arg_is_file,
        help = 'Path to two-column file with burst counts.',
    )
    parser.add_argument(
        '-o', '--outdir',
        type = arg_is_dir,
        default = os.getcwd(),
        help = 'Path to output directory.',
    )
    parser.add_argument(
        '-t', '--title',
        type = str,
        default = None,
        help = 'Plot title.',
    )

    args = parser.parse_args()

    df = concat_data_frames([args.count_path], sep = '\t')

    fig, gs, ax = plot_int_histo(
        int_values = df['burst_count'],
        stat = "proportion",
        xlabel = "Number of burst events",
        ylabel = "Proportion of trees",
        title = args.title,
    )
    fig.savefig(
        os.path.join(args.outdir, "burst-counts.pdf"),
            bbox_inches = "tight")
    plt.close(fig)

    fig, gs, ax = plot_int_histo(
        int_values = df['bursts_with_extant_nodes_count'],
        stat = "proportion",
        xlabel = "Number of burst events",
        ylabel = "Proportion of trees",
        title = args.title,
    )
    fig.savefig(
        os.path.join(args.outdir, "burst-with-extant-nodes-counts.pdf"),
            bbox_inches = "tight")
    plt.close(fig)

if __name__ == '__main__':
    main()
