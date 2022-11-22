from dash import Dash, dcc, Output, Input, html, State
import dash_bootstrap_components as dbc
import plotly.express as px
import base64
import ids, functions

# Components
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])


sequences = None

# app title
app.title = 'BioSpyder App'
# Layout
#app.layout = create_layout(app)

all_nations= ['A', 'B', 'C']
app.layout = html.Div([
    #Div for uploading file
    dcc.Upload(
        id=ids.UPLOAD_FASTA_COMPONENT,
        children= html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        # Do not allow multiple files for now
        multiple=False
    ),

    #Div for upload result, adds dropdown menu
    html.Div(id=ids.OUTPUT_DATA),

    #Div for dropdown menu result
    html.Div(id=ids.DROPDOWN_OUTPUT),

    #Div for highest GC content
    html.Div(id=ids.GC_DIV),

    #Div for bar chart
    html.Div(id=ids.BAR_CHART_DIV)

])




@app.callback(
        Output(ids.OUTPUT_DATA, 'children'),
        Input(ids.UPLOAD_FASTA_COMPONENT, 'contents'),
        State(ids.UPLOAD_FASTA_COMPONENT, 'filename'),
        State(ids.UPLOAD_FASTA_COMPONENT, 'last_modified')
    )
def update_output(list_of_contents, list_of_names, list_of_dates):
    # print('list_of_contents ', type(list_of_contents), list_of_contents)
    # print('list_of_names ', type(list_of_names), list_of_names)
    # print('list_of_dates ', type(list_of_dates), list_of_dates)

    if list_of_contents:
        content_type, content_string = list_of_contents.split(',')
        text = base64.b64decode(content_string)
        
        print('text ,' , text)
        d = functions.read_fasta(text.decode('utf-8'))
        print(d)
        # return dictionary.keys()[0]
        # return html.Div(str(d))
        #return html.Div('This is the upload file')
        global sequences
        sequences = d

        return dcc.Dropdown(options=[{'label':m, 'value':m} for m in d], id=ids.DROPDOWN_COMPONENT)

@app.callback(
    Output(ids.DROPDOWN_OUTPUT, 'children'),
    Output(ids.GC_DIV, 'children'),
    Output(ids.BAR_CHART_DIV, 'children'),
    Input(ids.DROPDOWN_COMPONENT, 'value')
)
def update_dropdown(value):
    if value:
        print('!!!!!!!!!!!!', sequences)
        #First for lenght, second for sequence, third bar graph
        length_text =f'You have selected {value}, of lenght {len(sequences[value])}'
        #Sequence
        gc_content, n = functions.gc_subsequence(sequences[value])
        gc_content_text = f'The sequence with the highest content of CG is: {gc_content}, with a total content of {n}0%'
        #Bar Graph
        df = functions.get_nucleotides(sequences[value])
        fig = px.bar(df, x='Base', y='Count')
        bar_graph = html.Div(dcc.Graph(figure=fig, id=ids.BAR_CHART))
        return length_text, gc_content_text, bar_graph



#Run app
if __name__ == '__main__':
    app.run_server(port=8000, debug=True)
