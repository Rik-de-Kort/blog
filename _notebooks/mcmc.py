import numpy as np
import pandas as pd
from scipy.stats import uniform, norm
from tqdm import tqdm

import altair as alt
import os
from toolz.curried import pipe

def json_dir(data, data_dir='altairdata'):
    os.makedirs(data_dir, exist_ok=True)
    return pipe(data, alt.to_json(filename=data_dir + '/{prefix}-{hash}.{extension}') )


# Generic functions
def simulate(initial, transition, n_iter=100, n_warmup=0):
    """
    Runs a markov chain simulation for n_iter iterations
    
    :param initial: initial point, sequence
    :param transition: function which takes points to points
    :param n_iter: number of iterations, int
    :param n_warmup: number of iterations to use as warmup
    :return: DataFrame of the Markov chain generated,
                each point having its coordinates expanded,
                and labeled with the iteration number i.
    """
    # Warmup
    current = initial
    for _ in tqdm(range(n_warmup)):
        current = transition(current)
    
    result = [current]
    for _ in tqdm(range(n_iter-1)):
        current = transition(current)
        result.append(current)
        
    n_dim = len(initial)
    result = pd.DataFrame(result,
                        columns=[f"x{i}" for i in range(n_dim)],
                         index=range(n_iter))
    result.index.name = "i"
    return result

def simulate_multiple(initial_points, transition, n_iter=100, n_warmup=0):
    """
    Runs multiple markov chains using simulate(p, transition, n_iter, n_warmup),
    one for every point p in initial_points.
    """
    return pd.concat([simulate(initial, transition, n_iter, n_warmup) for initial in initial_points],
                     keys=range(len(initial_points)),
                     names=["simulation", "i"],
                     axis=0).reset_index()


def visualize_simulation(df):
    """
    Visualizes a 2d-simulation interactively.
    
    :param df: DataFrame with columns i, x, and y with i the observation index
    :return: an Altair chart to play out the simulation with each realization its own facet
    """
    n_iter = df.i.nunique()
    slider = alt.binding_range(min=1, max=n_iter, step=1)
    select_time = alt.selection_single(name="iteration", fields=['i'],
                                       bind=slider, init={'i': 1})
    
    xmin, xmax = df.x0.min(), df.x0.max()
    ymin, ymax = df.x1.min(), df.x1.max()
    
    return alt.Chart(df).mark_point().encode(
        x=alt.X("x0", scale=alt.Scale(domain=(xmin, xmax))),
        y=alt.Y("x1", scale=alt.Scale(domain=(ymin, ymax))),
        opacity=alt.condition(alt.datum.i < select_time.i, alt.value(1), alt.value(0)),
        order="i"
    ).add_selection(
         select_time
    )



def transition_MH(current, f, scale=0.1):
    """
    Transition function for the Metropolis-Hastings algorithm
    
    :param current: current point
    :param f: probability proportion, taking a point and producing a float
    :param scale: scale for the proposal distribution
    :return: next point in the MH-chain
    """
    
    proposal = norm.rvs(loc=current, scale=scale)
    u = uniform.rvs()
    return proposal if u <= f(proposal)/f(current) else current


# Functions for traced simulation in the MH case
def transition_MH_trace(current, f, scale=0.1):
    """
    Add tracing info to transition_MH
    """
    proposal = norm.rvs(loc=current, scale=scale)
    u = uniform.rvs()
    result = proposal if u <= f(proposal)/f(current) else current
    return result, (current, f(current), proposal, f(proposal), u)


def simulate_trace(initial, transition, n_iter=100):
    """
    Modify simulate() to deal with tracing info from transition_MH
    """
    result = [initial]
    trace = [(initial, 0, initial, 0, 0)]
    for _ in range(n_iter-1):
        point, info = transition(result[-1])
        result.append(point)
        trace.append(info)
        
    n_dim = len(initial)
    result = pd.DataFrame(result,
                          columns=[f"x{i}" for i in range(n_dim)],
                          index=range(n_iter))
    result.index.name = "i"
    
    info = pd.DataFrame(trace,
                        columns=["current", "f_current", "proposal", "f_proposal", "u"],
                        index=range(n_iter))
    info.index.name = "i"
    
    return result, info

# Functions for comparing against the true 2d-distribution
def generate_sample(p_prop, x_bins, y_bins):
    """
    Sample from the "true" distribution using a grid of x_bins x y_bins
    """
    sample_grid = [(x, y) for x in x_bins for y in y_bins]
    result = pd.DataFrame([(q[0], q[1], p_prop(q)) for q in tqdm(sample_grid)], columns=("x0", "x1", "p"))
    result.p = result.p / result.p.sum()
    return result

def make_2d_histogram(df, x_bins, y_bins):
    """
    Create a 2d histogram from a simulation dataframe
    
    :param df: DataFrame with columns x0, x1, encoding points
    :param x_bins: iterable of bin edges for the x-axis
    :param y_bins: iterable of bin edges for the y-axis
    :return: an Altair chart with a histogram of the points
    """
    n_x, n_y = len(x_bins)-1, len(y_bins)-1
    H, _, _ = np.histogram2d(df.x0, df.x1, bins=[x_bins, y_bins])
    binned = pd.DataFrame([(x_bins[i], y_bins[j], H[i, j]) for i in range(n_x) for j in range(n_y)],
                  columns=("x0", "x1", "p"))
    binned.p = binned.p / binned.p.sum()
    return alt.Chart(binned).mark_point().encode(x="x0", y="x1", color="p")


# Functions for monitoring convergence
def split_single_chain(chain):
    n_iter = chain.i.max()+1
    first_half, second_half = chain[chain.i < n_iter / 2], chain[chain.i >= n_iter / 2]
    
    # Update chain number
    second_half.simulation = second_half.simulation + 0.5
    second_half.i = second_half.i - int(n_iter / 2)
    
    return pd.concat([first_half, second_half])

def split_chains(df):
    return df.groupby("simulation").apply(split_single_chain).reset_index(drop=True)


def Rhat(df, parameter):
    df = split_chains(df)
    
    n_iter = df.i.max()
    n_chains = df.simulation.nunique()
    
    chains = df.groupby("simulation")[parameter]
    
    W = chains.apply(lambda c: ((c - c.mean())**2).sum() / (n_iter - 1)).mean()
    
    chain_means = chains.mean()
    B = chain_means.apply(lambda c_mean: (c_mean - chain_means.mean())**2).sum() / (n_chains - 1)
    
    return np.sqrt((n_iter - 1)/n_iter + B / W)

def convergence(df, params):
    n_iter = df.i.max()
    a_Rhat = [[i] + [Rhat(df[df.i <= i], p) for p in params] for i in tqdm(range(n_iter-100, n_iter+1))]
    return pd.DataFrame(a_Rhat, columns=["i"] + [f"Rhat_{p}" for p in params])