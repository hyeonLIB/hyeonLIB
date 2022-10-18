from requests_html import HTML
# html = HTML(html="<a href='./PivotTable.html'>")
html = HTML(html = './PivotTable.html')
# scrpt = """
# function getURL(){
# return window.location.href;
# }
# """
scrpt = './scripts/app.js'
# return window.location.href;
output = html.render(script=scrpt, reload=False)
print(output)