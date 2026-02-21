"""
Example 66: Transparent Grid
Demonstrates using rgba theme colors to make the grid translucent,
allowing an animated background to show through.
"""
import dash
from dash import html
import dash_glide_grid as dgg

app = dash.Dash(__name__, suppress_callback_exceptions=True)

COLUMNS = [
    {'title': 'City', 'id': 'city', 'width': 180},
    {'title': 'Country', 'id': 'country', 'width': 140},
    {'title': 'Population', 'id': 'population', 'width': 130},
    {'title': 'Elevation (m)', 'id': 'elevation', 'width': 130},
    {'title': 'Founded', 'id': 'founded', 'width': 100},
]

DATA = [
    {'city': 'Tokyo', 'country': 'Japan', 'population': 13960000, 'elevation': 40, 'founded': 1457},
    {'city': 'Paris', 'country': 'France', 'population': 2161000, 'elevation': 35, 'founded': 259},
    {'city': 'New York', 'country': 'USA', 'population': 8336000, 'elevation': 10, 'founded': 1624},
    {'city': 'Sydney', 'country': 'Australia', 'population': 5312000, 'elevation': 3, 'founded': 1788},
    {'city': 'Cairo', 'country': 'Egypt', 'population': 9540000, 'elevation': 75, 'founded': 969},
    {'city': 'London', 'country': 'UK', 'population': 8982000, 'elevation': 11, 'founded': 47},
    {'city': 'Mumbai', 'country': 'India', 'population': 12478000, 'elevation': 14, 'founded': 1507},
    {'city': 'Rio de Janeiro', 'country': 'Brazil', 'population': 6748000, 'elevation': 11, 'founded': 1565},
    {'city': 'Istanbul', 'country': 'Turkey', 'population': 15460000, 'elevation': 39, 'founded': 660},
    {'city': 'Nairobi', 'country': 'Kenya', 'population': 4397000, 'elevation': 1661, 'founded': 1899},
]

BLOB_CONFIGS = [
    {'x': 200, 'y': 200, 'size': 180, 'color': '#ff6b6b', 'opacity': 0.35, 'dur': '8s',  'dx': 120, 'dy': 80},
    {'x': 500, 'y': 300, 'size': 150, 'color': '#ffd93d', 'opacity': 0.30, 'dur': '10s', 'dx': 100, 'dy': 120},
    {'x': 350, 'y': 150, 'size': 220, 'color': '#6bcb77', 'opacity': 0.25, 'dur': '7s',  'dx': 140, 'dy': 60},
    {'x': 150, 'y': 400, 'size': 160, 'color': '#4d96ff', 'opacity': 0.30, 'dur': '12s', 'dx': 90,  'dy': 110},
]

def make_blob(cfg, i):
    # Each blob gets a unique CSS animation via inline keyframes
    name = f'blob{i}'
    x, y = cfg['x'], cfg['y']
    return html.Div(style={
        'position': 'absolute',
        'left': f'{x}px', 'top': f'{y}px',
        'width': f'{cfg["size"]}px', 'height': f'{cfg["size"]}px',
        'borderRadius': '50%',
        'background': cfg['color'],
        'opacity': cfg['opacity'],
        'filter': 'blur(40px)',
        'animation': f'{name} {cfg["dur"]} ease-in-out infinite',
    })

# Build @keyframes CSS for each blob
keyframes_css = ''
for i, cfg in enumerate(BLOB_CONFIGS):
    name = f'blob{i}'
    dx, dy = cfg['dx'], cfg['dy']
    keyframes_css += f"""
    @keyframes {name} {{
        0%   {{ transform: translate(0, 0); }}
        25%  {{ transform: translate({dx}px, {-dy}px); }}
        50%  {{ transform: translate({-dx//2}px, {dy}px); }}
        75%  {{ transform: translate({-dx}px, {-dy//2}px); }}
        100% {{ transform: translate(0, 0); }}
    }}
    """

app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>''' + keyframes_css + '''</style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

app.layout = html.Div([
    html.H2('Transparent Grid', style={
        'color': 'white', 'textShadow': '1px 1px 3px black',
        'position': 'relative', 'zIndex': 1,
    }),

    html.Div(
        dgg.GlideGrid(
            id='transparent-grid',
            columns=COLUMNS,
            data=DATA,
            height=350,
            readonly=True,
            rowMarkers='number',
            smoothScrollX=True,
            smoothScrollY=True,
            theme={
                'bgCell': 'rgba(255, 255, 255, 0.35)',
                'bgHeader': 'rgba(255, 255, 255, 0.55)',
                'bgHeaderHasFocus': 'rgba(255, 255, 255, 0.65)',
                'bgHeaderHovered': 'rgba(255, 255, 255, 0.60)',
                'textDark': '#1a1a2e',
                'textHeader': '#1a1a2e',
                'borderColor': 'rgba(255, 255, 255, 0.4)',
                'horizontalBorderColor': 'rgba(255, 255, 255, 0.3)',
                'accentLight': 'rgba(100, 180, 255, 0.25)',
                'bgCellMedium': 'rgba(255, 255, 255, 0.25)',
            },
        ),
        style={'width': '720px', 'position': 'relative', 'zIndex': 1},
    ),

    # Animated blobs — pure CSS, no callbacks
    html.Div(
        [make_blob(cfg, i) for i, cfg in enumerate(BLOB_CONFIGS)],
        style={
            'position': 'fixed', 'top': 0, 'left': 0,
            'width': '100%', 'height': '100%',
            'zIndex': 0, 'overflow': 'hidden', 'pointerEvents': 'none',
        },
    ),
], style={
    'margin': 0,
    'padding': '40px',
    'fontFamily': 'Arial, sans-serif',
    'background': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    'minHeight': '100vh',
    'position': 'relative',
})

if __name__ == '__main__':
    app.run(debug=True, port=8066)
