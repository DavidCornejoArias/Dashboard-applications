# Installing packages
from flask import Flask, render_template, request
from bokeh.plotting import figure, show
from bokeh.embed import components
from bokeh.models import ColumnDataSource, HoverTool, PrintfTickFormatter, CustomJS, Slider
from bokeh.layouts import row, column
import pandas
from bokeh.io import curdoc

# Reading the dataframe
df = pandas.read_csv(r'..\data\googleplaystore.csv')
# Getting list of categories
listCategory = list(df.Category.unique())
# Trying another way
# Creating dispersion Plot
def dispersionPlot(df,xVariable,yVariable,slideVariable,filterCategorical,filterCategoricalValue):
    df = df[df[filterCategorical]==filterCategoricalValue]
    source = ColumnDataSource(df)
    hover = HoverTool()
    hover.tooltips = """
        <div>
            <h3>Reviews number: @Reviews</h3>
            <div><strong>Installation number: </strong> @Installs </div>
        </div>
    """
    hover_tool = HoverTool(tooltips=[('Reviews', '@Reviews'), ('Installs', '@Installs')])
    p = figure(x_range=(df[xVariable].min(),df[xVariable].max()),y_range=(df[yVariable].min(),df[yVariable].max())
    , title="Review by installation",
    x_axis_label='Reviews', y_axis_label='Installs',
    plot_width=400, plot_height=400
        )
    p.circle(xVariable, yVariable,source = source, legend_label=yVariable, fill_color="red", line_color="red", size=6)
    # adding slider:
    rating_slider = Slider(start=df[slideVariable].min(), end=df[slideVariable].max(), value=1, step=.1, title=slideVariable)
    # Adding JS code
    callback = CustomJS(args=dict(source=source, rating=rating_slider),
                        code="""
        const data = source.data;
        source.change.emit();
    """)
    rating_slider.js_on_change('value', callback)
    p.add_tools(hover)
    layout = row(
        p,
        column(rating_slider),
    )
    # show the results
    return layout

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
    p = figure(x_range=source.data['App'].tolist() , plot_height=300,title="Best 3 review apps",
    x_axis_label='Apps', y_axis_label='Reviews')
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
    p = figure(x_range=source.data['values'].tolist() , plot_height=300,title="Type of app",
    x_axis_label='Apps', y_axis_label='Number of apps')
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
        graphic3 = dispersionPlot(df,'Reviews','Installs','Rating','Category',listCategory[0])
    else:
        graphic = vBarGraphic(df, 'App', 'Category',listCategory[int(selected_class)],'Rating',3)
        graphic2 = vBarGraphic2(df, 'Type', 'Category', listCategory[int(selected_class)])
        graphic3 = dispersionPlot(df,'Reviews','Installs','Rating','Category',listCategory[int(selected_class)])
    script_chart, div_chart = components(graphic)
    script_chart2, div_chart2 = components(graphic2)
    script_chart3, div_chart3 = components(graphic3)
    return render_template('index.html',listCategory = listCategory,categoriesAmount = range(0,len(listCategory)), 
    div_chart=div_chart, script_chart=script_chart, selected_class=selected_class,
    div_chart2 = div_chart2, script_chart2 = script_chart2,
    div_chart3 = div_chart3, script_chart3 = script_chart3)
    #return render_template('secondIndex.html',div_chart=div_chart, script_chart=script_chart)

if __name__ == "__main__":
    app.run()
