"""
Utility functions for the Vector Databases project.

This module contains helper functions for image processing, base64 conversion,
and other common tasks used across the notebooks.
"""

import base64
import io
import matplotlib.pyplot as plt
from IPython.display import Image, display
from typing import Optional


def figure_to_base64(
    fig: plt.Figure, format: str = "png", dpi: int = 150, bbox_inches: str = "tight"
) -> str:
    """
    Convert a matplotlib figure to base64 string.

    Args:
        fig: Matplotlib figure object
        format: Image format ('png', 'jpg', 'svg', etc.)
        dpi: Resolution in dots per inch
        bbox_inches: Bounding box setting for tight layout

    Returns:
        Base64 encoded string of the image

    Example:
        >>> fig, ax = plt.subplots()
        >>> ax.plot([1, 2, 3], [1, 4, 2])
        >>> base64_str = figure_to_base64(fig)
        >>> display(Image(data=base64_str))
    """
    img_buffer = io.BytesIO()
    fig.savefig(img_buffer, format=format, bbox_inches=bbox_inches, dpi=dpi)
    img_buffer.seek(0)

    img_base64 = base64.b64encode(img_buffer.read()).decode("utf-8")
    img_buffer.close()

    return img_base64


def plot_to_base64(
    plot_func, *args, figsize: tuple = (8, 6), close_fig: bool = True, **kwargs
) -> str:
    """
    Create a plot using a function and convert it to base64.

    Args:
        plot_func: Function that creates the plot
        *args: Arguments to pass to plot_func
        figsize: Figure size as (width, height)
        close_fig: Whether to close the figure after conversion
        **kwargs: Keyword arguments to pass to plot_func

    Returns:
        Base64 encoded string of the plot

    Example:
        >>> def my_plot():
        ...     plt.plot([1, 2, 3], [1, 4, 2])
        ...     plt.title('Sample Plot')
        >>> base64_str = plot_to_base64(my_plot)
    """
    fig, ax = plt.subplots(figsize=figsize)
    plot_func(*args, **kwargs)

    base64_str = figure_to_base64(fig)

    if close_fig:
        plt.close(fig)

    return base64_str


def image_file_to_base64(image_path: str) -> str:
    """
    Convert an image file to base64 string.

    Args:
        image_path: Path to the image file

    Returns:
        Base64 encoded string of the image

    Raises:
        FileNotFoundError: If the image file doesn't exist

    Example:
        >>> base64_str = image_file_to_base64('path/to/image.png')
        >>> display(Image(data=base64_str))
    """
    try:
        with open(image_path, "rb") as img_file:
            img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
        return img_base64
    except FileNotFoundError:
        raise FileNotFoundError(f"Image file not found: {image_path}")


def display_base64_image(
    base64_str: str, width: Optional[int] = None, height: Optional[int] = None
) -> None:
    """
    Display a base64 image in Jupyter notebook.

    Args:
        base64_str: Base64 encoded image string
        width: Optional width for display
        height: Optional height for display

    Example:
        >>> base64_str = image_file_to_base64('image.png')
        >>> display_base64_image(base64_str, width=400)
    """
    img = Image(data=base64_str)
    if width is not None:
        img.width = width
    if height is not None:
        img.height = height
    display(img)


def create_markdown_image(
    base64_str: str,
    alt_text: str = "Image",
    width: Optional[int] = None,
    height: Optional[int] = None,
    use_html: bool = True,
) -> str:
    """
    Create markdown/HTML string for embedding base64 image.

    Args:
        base64_str: Base64 encoded image string
        alt_text: Alternative text for the image
        width: Optional width attribute
        height: Optional height attribute
        use_html: Whether to use HTML img tag (True) or markdown syntax (False)

    Returns:
        Markdown/HTML string for embedding the image

    Example:
        >>> base64_str = image_file_to_base64('image.png')
        >>> markdown = create_markdown_image(base64_str, "My Image", width=400)
        >>> print(markdown)
    """
    data_url = f"data:image/png;base64,{base64_str}"

    if use_html:
        style_attrs = []
        if width is not None:
            style_attrs.append(f'width="{width}"')
        if height is not None:
            style_attrs.append(f'height="{height}"')

        attrs = " ".join(style_attrs)
        return f'<img src="{data_url}" alt="{alt_text}" {attrs}>'
    else:
        return f"![{alt_text}]({data_url})"


def get_image_info(base64_str: str) -> dict:
    """
    Get information about a base64 encoded image.

    Args:
        base64_str: Base64 encoded image string

    Returns:
        Dictionary with image information

    Example:
        >>> info = get_image_info(base64_str)
        >>> print(f"Size: {info['size_bytes']} bytes")
    """
    return {
        "size_bytes": len(base64_str.encode("utf-8")),
        "size_kb": round(len(base64_str.encode("utf-8")) / 1024, 2),
        "base64_length": len(base64_str),
        "preview": base64_str[:100] + "..." if len(base64_str) > 100 else base64_str,
    }


# Example usage and demo functions
def demo_matplotlib_to_base64():
    """Demo function showing matplotlib to base64 conversion."""
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.plot([1, 2, 3, 4], [1, 4, 2, 3], "bo-", linewidth=2, markersize=8)
    ax.set_title("Sample Plot for Base64 Demo", fontsize=14)
    ax.set_xlabel("X Values")
    ax.set_ylabel("Y Values")
    ax.grid(True, alpha=0.3)

    base64_str = figure_to_base64(fig)
    plt.close(fig)

    print(f"Generated base64 image:")
    print(f"- Size: {get_image_info(base64_str)['size_kb']} KB")
    print(f"- Preview: {base64_str[:100]}...")

    display_base64_image(base64_str)
    return base64_str


if __name__ == "__main__":
    # Run demo if script is executed directly
    print("Vector Databases Utils - Base64 Image Demo")
    print("=" * 50)
    demo_matplotlib_to_base64()
