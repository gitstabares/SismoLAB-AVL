"""Utilities for mapping numerical intensity values to Matplotlib colors."""

import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


class IntensityColorMapper:
    """Map numerical intensity values to hexadecimal colors.

    The mapper normalizes values between configurable minimum and maximum
    bounds, then looks up the corresponding color in a Matplotlib colormap.

    Attributes:
        _vmin (float): Lower bound used by the normalization.
        _vmax (float): Upper bound used by the normalization.
        _colormap: The Matplotlib colormap used to generate colors.
        _normalizer (matplotlib.colors.Normalize): The normalization object
            used to scale values into the range ``[0, 1]``.
    """

    def __init__(self, vmin, vmax, colormap_name: str = "jet"):
        """Initialize the color mapper.

        Args:
            vmin (float): Minimum value for normalization.
            vmax (float): Maximum value for normalization.
            colormap_name (str): Name of the Matplotlib colormap to use.
        """
        self._vmin = vmin
        self._vmax = vmax
        self.set_colormap(colormap_name)
        self._update_normalizer()

    def set_colormap(self, colormap_name: str):
        """Set the Matplotlib colormap used for color interpolation.

        Args:
            colormap_name (str): Name of the Matplotlib colormap, or a
                Matplotlib colormap object accepted by ``plt.get_cmap``.
        """
        self._colormap = plt.get_cmap(colormap_name)

    def set_vmin(self, vmin: float):
        """Set the minimum normalization bound.

        Args:
            vmin (float): New minimum value.
        """
        self._vmin = float(vmin)
        self._update_normalizer()

    def set_vmax(self, vmax: float):
        """Set the maximum normalization bound.

        Args:
            vmax (float): New maximum value.
        """
        self._vmax = float(vmax)
        self._update_normalizer()

    def _update_normalizer(self):
        """Refresh the normalization range used by the mapper.

        Returns:
            None: Updates the internal normalization object in place.
        """
        self._normalizer = mcolors.Normalize(vmin=self._vmin, vmax=self._vmax)

    def interpolate(self, value: float) -> str:
        """Map a value to its hexadecimal color representation.

        Args:
            value (float): Numerical value to map.

        Returns:
            str: Hexadecimal color code for the interpolated value.
        """
        # Normalize the input value between 0.0 and 1.0.
        normalized_value = self._normalizer(value)

        # Map the normalized value to an RGBA color tuple.
        rgba_color = self._colormap(normalized_value)

        # Convert RGBA to hexadecimal format.
        return mcolors.to_hex(rgba_color)