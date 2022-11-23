from dash import Dash, dcc, Output, Input, html, State
import dash_bootstrap_components as dbc
import plotly.express as px
import base64
from assets import ids, functions
import dash_bio as dashbio

# Components
app = Dash(__name__, external_stylesheets=[dbc.themes.LUX], suppress_callback_exceptions=True)


sequences = None

# app title
app.title = 'BioSpyder App'

description = 'This is a gene analysis tool for preliminary sequence analysis. \nUpload a .fasta or .csv file and get descriptive metrics about the genes'

div_style = {
    'background': 'white',
    'padding': '2rem',
    'border': '5px solid gray',
    'borderRadius': '1rem',
    'fontSize': '1.5rem',
    'margin': '0.7rem',
    'maxWidth': '70%',
    'marginLeft': 'auto',
    'marginRight':'auto'
}

# Layout
all_nations= ['A', 'B', 'C']
app.layout = html.Div([
    #Header
    html.H1('BioSpyder Sequence Analysis Tool',
        style={
            'textAlign': 'center',
            'paddingTop': '30px',
            'fontSize': '2.5rem'
        }),
    #Div for uploading file
    dcc.Upload(
        id=ids.UPLOAD_FASTA_COMPONENT,
        children= html.Div([
            'Drag and Drop or ',
            html.A('Select Files', style={
                'textDecoration': 'underline',
                'color': 'blue'
            })
        ]),
        style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px',
            'maxWidth': '80%',
            'marginLeft': 'auto',
            'marginRight': 'auto'
        },
        # Do not allow multiple files for now
        multiple=False
    ),

    html.Div(children=[
        html.Div(description, id=ids.N_SEQUENCES,
        style=div_style),

        html.Div(id=ids.OUTPUT_DATA, 
            style={
                'maxWidth': '75%',
                'marginLeft': 'auto',
                'marginRight': 'auto',
                'padding': '1rem'
                }),

        #Div for dropdown menu result
        html.Div(id=ids.DROPDOWN_OUTPUT, style={
            'padding': '1rem',
            'fontSize': '2rem'
        }),
        
        #Div for bar chart
        html.Div(id=ids.BAR_CHART_DIV),
        
        #Div for highest GC content
        html.Div(id=ids.GC_DIV)
    ],
    style={
        'textAlign': 'center',
        'margin': '10px',
        'maxWidth': '80%',
        'marginLeft': 'auto',
        'marginRight': 'auto'
    })
    #Div for upload result, adds dropdown menu


])


#Callback for upload
@app.callback(
        Output(ids.OUTPUT_DATA, 'children'),
        Output(ids.N_SEQUENCES, 'children'),
        Input(ids.UPLOAD_FASTA_COMPONENT, 'contents'),
        Input(ids.UPLOAD_FASTA_COMPONENT, 'filename'),
        prevent_initial_call=True
    )
def update_output(list_of_contents, filename):
    if str(list_of_contents) != 'None':
        print(filename)
        content_type, content_string = list_of_contents.split(',')
        text = base64.b64decode(content_string)
        #Read file based on extension
        if filename.split('.')[1] == 'fasta':
            d = functions.read_fasta(text.decode('utf-8'))
        elif filename.split('.')[1]=='csv':
            d = functions.read_csv(text.decode('utf-8'))
        #If the extension was wrong and the file was not read
        else:
            return None, 'Please only upload .fasta or .csv files'

        global sequences
        sequences = d
        print(d.keys())
        return dcc.Dropdown(
            options=[{'label':m, 'value':m} for m in d], 
            id=ids.DROPDOWN_COMPONENT,
            # value=list(d.keys())[0],!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
            ), f'{len(d)} sequences loaded'


#Callback for dropdown
@app.callback(
    Output(ids.DROPDOWN_OUTPUT, 'children'),
    Output(ids.GC_DIV, 'children'),
    Output(ids.BAR_CHART_DIV, 'children'),
    Input(ids.DROPDOWN_COMPONENT, 'value'),
    prevent_initial_call=True
)
def update_dropdown(value):
    print(type(str(value)), str(value))
    if str(value) != 'None':
        #First for lenght, second for sequence, third bar graph
        length_text =f'You have selected {value}, of length {len(sequences[value])}bp'
        #Sequence
        gc_content, n, pos = functions.gc_subsequence(sequences[value])
        gc_content_text = f'The 10bp sequence with the highest content of CG is: {gc_content}, with a total content of {n}0%'
        #Sequence visualiser for GC content
        graph = dashbio.SequenceViewer(
            id=ids.SEQUENCE_VIEWER,
            sequence=sequences[value],
            selection=[pos, pos+10, 'green'],
            badge=False,
            search=False
        )  

        #Bar Graph
        df = functions.get_nucleotides(sequences[value])
        fig = px.bar(df, x='Base', y='Percent', text='Count')
        bar_graph = html.Div(dcc.Graph(figure=fig, id=ids.BAR_CHART))
        return length_text, [gc_content_text, graph], bar_graph
    else:
        return None, None, None

#Callback for change style
@app.callback(
    Output(ids.DROPDOWN_OUTPUT, 'style'),
    Output(ids.GC_DIV, 'style'),
    Input(ids.DROPDOWN_COMPONENT, 'value')
)
def update_style(value):
    if str(value) != 'None':
        return div_style, div_style
    else:
        return None, None

#Run app
if __name__ == '__main__':
    app.run_server(port=8000, debug=True)
