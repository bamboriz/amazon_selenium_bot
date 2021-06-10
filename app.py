import dash

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(children=[
    html.H2(children='Amazon Buy Bot'),
    
   dcc.Input(
    id = "item_q",
    value = '',
    placeholder = "Enter an item ..."),

    html.Button(
    "Buy Now",
    id = "submit",
    n_clicks = 0 ),

    html.Div(id = "result")

])

@app.callback(
  Output("result","children"),
  Input("submit","n_clicks"),
  Input("item_q","value"))

def update_result(submit,item_q):
  changed_id = [p['prop_id'] for p in dash.callback_context.triggered][0]

  if "submit" in changed_id:
    item_q = item_q.lower()
    driver = webdriver.Chrome('./chromedriver')
    driver.get("https://www.amazon.fr/")
    time.sleep(2)
    WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.ID, "a-autoid-0"))).click()
    time.sleep(1)
    search_bar = driver.find_element_by_name("field-keywords")
    for letter in item_q:
        search_bar.send_keys(letter)

    search_bar.send_keys(Keys.RETURN)
    time.sleep(2)
    ans = driver.find_elements_by_css_selector('div.s-result-item')
    
    for option in ans:
        if option.get_attribute("data-asin") != '' :
            option.click()
            break

    time.sleep(2)
    
    try:
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "add-to-cart-button"))).click()
        return '"{}" has been added to cart!'.format(item_q.capitalize())
    except:
        return 'Oops, product not in stock'
    finally:
        driver.close()


if __name__ == '__main__':
    app.run_server(debug=True)