import matplotlib.pyplot as plt
from matplotlib.patheffects import withStroke
import random

def create_sign(word, font_size=100, font_color='lime', background_color='black', glow_color='lime'):

    word = word.replace("_"," ").title()
    fig, ax = plt.subplots(figsize=(8, 2))
    ax.axis('off')

    total_height = font_size * .05 # Calculate total height of stacked words Adjust spacing as needed 
    ax.set_facecolor(background_color) # Set background color

    # Render the text with a glow effect
    text = ax.text(0.1, 0.2, word, ha='center', va='center', fontsize=font_size, color=font_color,
                   path_effects=[withStroke(linewidth=2, foreground=glow_color)])
    return plt



import matplotlib.pyplot as plt
import matplotlib.patheffects as pe
from matplotlib.font_manager import FontProperties
from io import BytesIO

def create_sign_II(
    word: str,
    font_size: int = 120,
    font_color: str = "lime",
    background_color: str = "black",
    glow_color: str = "lime",
    glow_width: int = 6,
    pad_px: int = 40,
    font_path: str | None = None,
    dpi: int = 200,
    save_path: str | None = None,
):
    """
    Render a glowing text 'sign' and optionally save to file.

    Returns:
        (fig, ax) if not saved, else the save_path.
    """
    # Normalize/title-case and prepare font
    text = word.replace("_", " ").strip().title()
    fp = FontProperties(fname=font_path) if font_path else None

    # -- first: get text bbox to auto-size the figure --
    tmp_fig, tmp_ax = plt.subplots()
    tmp_ax.axis("off")
    t = tmp_ax.text(
        0, 0, text, fontsize=font_size, fontproperties=fp
    )
    tmp_fig.canvas.draw()
    bbox = t.get_window_extent(renderer=tmp_fig.canvas.get_renderer())
    plt.close(tmp_fig)

    # Compute figure size from pixel bbox + padding
    width_px = bbox.width + 2 * pad_px
    height_px = bbox.height + 2 * pad_px
    fig_w, fig_h = width_px / dpi, height_px / dpi

    # -- render final figure --
    fig, ax = plt.subplots(figsize=(fig_w, fig_h), dpi=dpi)
    ax.set_facecolor(background_color)
    ax.axis("off")

    # Center in axes using axes coords
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)

    # Nice layered glow (thick → thin → face)
    effects = [
        pe.withStroke(linewidth=glow_width, foreground=glow_color, alpha=0.25),
        pe.withStroke(linewidth=max(1, glow_width//2), foreground=glow_color, alpha=0.6),
        pe.withStroke(linewidth=1, foreground=glow_color, alpha=0.9),
    ]

    ax.text(
        0.5, 0.5, text,
        ha="center", va="center",
        fontsize=font_size, color=font_color,
        fontproperties=fp,
        path_effects=effects
    )

    fig.tight_layout(pad=0)

    if save_path:
        fig.savefig(save_path, facecolor=background_color, dpi=dpi, bbox_inches="tight", pad_inches=0)
        plt.close(fig)
        return save_path
    return fig, ax



def persist_plt(plt,filename): 
    # Save the figure as PNG if filename is provided
    if filename:
        plt.savefig(filename, bbox_inches='tight', pad_inches=0, transparent=True)



def create_stacked_sign(phrase, font_size=100, font_color='lime', background_color='black', glow_color='lime'):
    ''' Split the phrase into individual words '''
    phrase = phrase.replace("_"," ").title()
    words = phrase.split()
    total_height = len(words) * font_size * 1.9  # Adjust spacing as needed
    
    # Create a figure and axis with appropriate size
    fig, ax = plt.subplots(figsize=(8, total_height / 100))  # Divide total height by 100 for inches

    # Set background color
    ax.set_facecolor(background_color)

    # Render the words with glow effect and center them vertically
    for i, word in enumerate(words):
        text_y = (total_height - (i * font_size * 1.9)) / total_height  # Calculate y position
        text = ax.text(0.5, text_y, word, ha='center', va='center', fontsize=font_size, color=font_color,
                       path_effects=[withStroke(linewidth=2, foreground=glow_color)])

    ax.axis('off')    # Hide axes
    return plt


def create_solution_sign(df):
    named_colors = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black', 'white']
    path_to_solutions = r"C://Users//josep//"
    for index, row in df.iterrows():
        # Print out the desired columns for each row
        solution_name =  row['solution_name'] 
        solution_directory =  row['solution_directory']  
        foreground_color = random.choice(named_colors)
        stacked_filename = f"{path_to_solutions}{solution_directory}//solution_stacked_sign.png"
        sign_filename = f"{path_to_solutions}{solution_directory}//solution_sign.png" 
        plt = create_stacked_sign(solution_name, font_size=40, font_color=foreground_color , background_color='lightblue', glow_color='blue')
        persist_plt(plt,stacked_filename)
        plt.show()
        plt = create_sign(solution_name, font_size=45, font_color='gold', background_color='black', glow_color='darkblue')
        persist_plt(plt,sign_filename)
        plt.show()        