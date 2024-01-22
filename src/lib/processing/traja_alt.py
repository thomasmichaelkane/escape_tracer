import numpy as np
from typing import Union, Tuple
from matplotlib.collections import PathCollection
from matplotlib import pyplot as plt

import traja
from traja.frame import TrajaDataFrame

def trip_grid(
    trj: TrajaDataFrame,
    bins: Union[tuple, int] = 10,
    log: bool = False,
    spatial_units: str = None,
    hist_only: bool = False,
    **kwargs,
) -> Tuple[np.ndarray, PathCollection]:
    """Generate a heatmap of time spent by point-to-cell gridding.

    Args:
      bins (int, optional): Number of bins (Default value = 10)
      log (bool): log scale histogram (Default value = False)
      spatial_units (str): units for plotting
      normalize (bool): normalize histogram into density plot
      hist_only (bool): return histogram without plotting

    Returns:
        hist (:class:`numpy.ndarray`): 2D histogram as array
        image (:class:`matplotlib.collections.PathCollection`: image of histogram

    """
    after_plot_args, kwargs = traja.plotting._get_after_plot_args(**kwargs)

    bins = traja.trajectory._bins_to_tuple(trj, bins)
    # TODO: Add kde-based method for line-to-cell gridding
    df = trj[["x", "y"]].dropna()

    # Set aspect if `xlim` and `ylim` set.
    if "xlim" in kwargs and "ylim" in kwargs:
        xlim, ylim = kwargs.pop("xlim"), kwargs.pop("ylim")
    else:
        xlim, ylim = traja.trajectory._get_xylim(df)
    xmin, xmax = xlim
    ymin, ymax = ylim

    x, y = zip(*df.values)

    hist, x_edges, y_edges = np.histogram2d(
        x, y, bins, range=((xmin, xmax), (ymin, ymax))
    )

    # rotate to keep y as first dimension
    hist = np.rot90(hist)

    if log:
        hist = np.log(hist + np.e)
    if hist_only:  # TODO: Evaluate potential use cases or remove
        return (hist, None)
    fig, ax = plt.subplots()

    image = ax.imshow(
        hist, interpolation="bilinear", aspect="equal", extent=[xmin, xmax, ymin, ymax]
    )
    # TODO: Adjust colorbar ytick_labels to correspond with time
    label = "Frames" if not log else "$ln(frames)$"
    plt.colorbar(image, ax=ax, label=label)

    traja.plotting._label_axes(trj, ax)

    plt.title("Time spent{}".format(" (Logarithmic)" if log else ""))

    traja.plotting._process_after_plot_args(**after_plot_args)
    # TODO: Add method for most common locations in grid
    # peak_index = unravel_index(hist.argmax(), hist.shape)
    return hist, image