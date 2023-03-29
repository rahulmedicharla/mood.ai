import webbrowser

class WebBrowser:
    def __init__(self, ai_generation):
        self.image_links = ai_generation.image_links
        self.html_starting = """
        <html>
            <head>
                <title>AI Gallery</title>
            </head>
            <body>
        """
        self.html_ending = """
            </body>
        </html>
        """
    
    def create_webpage(self):
        #add header, replace old images
        f = open('output.html', 'w')
        f.write(self.html_starting)
        f.close()

        #add content:
        f = open('output.html', 'a')
        for link in self.image_links:
            f.write("<img src=" + link + "width = '500px' height = '500px'></img>")
            f.write('<br><br>')

        f.write(self.html_ending)
        f.close()

        webbrowser.open_new('output.html')
