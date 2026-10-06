import matplotlib.colors as mcolors
import matplotlib.pyplot as plt


class IntensityColorMapper:
    """Manages color mapping and normalization for seismic or numerical intensity.
    
    This class allows configuring a colormap and normalization bounds (vmin, vmax)
    without using property decorators, providing explicit getter and setter methods.
    """
    
    def __init__(self, vmin, vmax, colormap_name: str = "jet"):
        """Initializes the color mapper with a colormap and normalization range.
        
        Args:
            colormap_name (str): The name of the matplotlib colormap.
            vmin (float): Minimum value for normalization.
            vmax (float): Maximum value for normalization.
        """
        self._vmin = vmin
        self._vmax = vmax
        self.set_colormap(colormap_name)
        self._update_normalizer()

    def set_colormap(self, colormap_name: str):
        """Sets a new colormap by its string name or colormap object.
        
        Args:
            colormap_name (str or Colormap): The colormap name or instance.
        """
        self._colormap = plt.get_cmap(colormap_name)

    def set_vmin(self, vmin: float):
        """Sets the minimum value of the normalizer and updates it.
        
        Args:
            vmin (float): The new minimum value.
        """
        self._vmin = float(vmin)
        self._update_normalizer()

    def set_vmax(self, vmax: float):
        """Sets the maximum value of the normalizer and updates it.
        
        Args:
            vmax (float): The new maximum value.
        """
        self._vmax = float(vmax)
        self._update_normalizer()

    def _update_normalizer(self):
        """Internal helper method to refresh the normalization range."""
        self._normalizer = mcolors.Normalize(vmin=self._vmin, vmax=self._vmax)

    def interpolate(self, value: float) -> str:
        """Interpolates a given intensity value into an hexadecimal color code.
        
        Args:
            value (float): The numerical value to map.
            
        Returns:
            str: The resulting hexadecimal color string.
        """
        # Normalize the input value between 0.0 and 1.0
        normalized_value = self._normalizer(value)
        
        # Map the normalized value to an RGBA color tuple
        rgba_color = self._colormap(normalized_value)
        
        # Convert RGBA to hexadecimal format
        return mcolors.to_hex(rgba_color)