# Installing packages
from flask import Flask, render_template, request
from bokeh.plotting import figure, show
from bokeh.embed import components
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
    xData = finalDf[categoricalVariable].tolist()
    yData = finalDf[numericalVariable].tolist()
    p = figure(x_range=xData, plot_height=300)
    p.vbar(x=xData, width=0.5, bottom=0,
       top=yData, color="firebrick")
    curdoc().add_root(row(p, name='plotrow'))
    return p
# Initializating the app
app = Flask(__name__)

# Initial webpage
@app.route('/', methods=['GET', 'POST'])
def homepage():
    selected_class = request.form.get('dropdown-select')
    if selected_class == 0 or selected_class == None:
        graphic = vBarGraphic(df, 'App', 'Category','ART_AND_DESIGN','Rating',6)    
    else:
        graphic = vBarGraphic(df, 'App', 'Category','ART_AND_DESIGN','Rating',6)
    script_chart, div_chart = components(graphic)
    return render_template('index.html',listCategory = listCategory,categoriesAmount = range(0,len(listCategory)), 
    div_chart=div_chart, script_chart=script_chart, selected_class=selected_class )
    #return render_template('secondIndex.html',div_chart=div_chart, script_chart=script_chart)

if __name__ == "__main__":
    app.run()