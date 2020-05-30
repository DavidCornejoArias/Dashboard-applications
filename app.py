# Installing packages
from flask import Flask, render_template, request
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter
from bokeh.layouts import row 
import pandas
from bokeh.io import curdoc

# Reading the dataframe
df = pandas.read_csv(r'..\data\googleplaystore.csv')
# Getting list of categories
listCategory = list(df.Category.unique())
# Trying another way

# Function for making the graphic:
def vBarGraphic(df, categoricalVariable, filterCategorical, filterCategoricalValue, numericalVariable, numberToShow):
    df.dropna(subset = [numericalVariable], inplace=True)
    finalDf = df[df[filterCategorical]==filterCategoricalValue].sort_values(by=numericalVariable,ascending=False).head(numberToShow)
    source = ColumnDataSource(finalDf)    
    hover = HoverTool()
    hover_tool = HoverTool(tooltips=[('Name', '@App'), ('Rating', '@Rating')])
    hover.tooltips = """
        <div>
            <h3>@App</h3>
            <div><strong>Value: </strong> @Rating </div>
        </div>
    """
    p = figure(x_range=source.data['App'].tolist() , plot_height=300)
    p.vbar(x=categoricalVariable, width=0.5, bottom=0, 
    top=numericalVariable, color="firebrick", source = source)
    p.add_tools(hover)
    return p
# Function making the second graphic
def vBarGraphic2(df, categoricalVariable, filterCategorical, filterCategoricalValue):
    dfCategory = df[df[filterCategorical]==filterCategoricalValue]
    typByCategoryDF = dfCategory.groupby(categoricalVariable)[categoricalVariable].value_counts().to_frame()
    typByCategoryDF['values'] = typByCategoryDF.index
    typByCategoryDF['values']  = [i[0] for i in typByCategoryDF['values'].tolist()]
    source = ColumnDataSource(typByCategoryDF)
    hover = HoverTool()
    hover.tooltips = """
        <div>
            <h3>@values</h3>
            <div><strong>Value: </strong> @Type </div>
        </div>
    """
    hover_tool = HoverTool(tooltips=[('Category', '@values'), ('Count', '@Type')])
    p = figure(x_range=source.data['values'].tolist() , plot_height=300)
    p.vbar(x='values', width=0.5, bottom=0,
        top='Type', source = source)
    p.add_tools(hover)
    return p
# Initializating the app
app = Flask(__name__)

# Initial webpage
@app.route('/', methods=['GET', 'POST'])
def homepage():
    selected_class = request.form.get('dropdown-select')
    if selected_class == 0 or selected_class == None:
        graphic = vBarGraphic(df, 'App', 'Category',listCategory[0],'Rating',3)   
        graphic2 = vBarGraphic2(df, 'Type', 'Category', listCategory[0]) 
    else:
        graphic = vBarGraphic(df, 'App', 'Category',listCategory[int(selected_class)],'Rating',3)
        graphic2 = vBarGraphic2(df, 'Type', 'Category', listCategory[int(selected_class)]) 
    script_chart, div_chart = components(graphic)
    script_chart2, div_chart2 = components(graphic2)
    return render_template('index.html',listCategory = listCategory,categoriesAmount = range(0,len(listCategory)), 
    div_chart=div_chart, script_chart=script_chart, selected_class=selected_class,
    div_chart2 = div_chart2, script_chart2 = script_chart2)
    #return render_template('secondIndex.html',div_chart=div_chart, script_chart=script_chart)

if __name__ == "__main__":
    app.run()
