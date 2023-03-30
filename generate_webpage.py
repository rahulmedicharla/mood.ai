import webbrowser

class WebBrowser:
    def __init__(self, ai_generation):
        self.image_results = ai_generation.image_results
        self.html_starting = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>mood.ai art gallery</title>
            <style>
                body {
                    background-color: #F2E8E8;
                    font-family: Arial, sans-serif;
                    color: #333;
                    margin: 0;
                    padding: 0;
                }
                h1 {
                    text-align: center;
                    margin-top: 50px;
                    font-size: 40px;
                    color: #333;
                }
                .gallery {
                    align-items: center;
                    justify-content: center;
                    margin-top: 30px;
                }
                .item {
                    margin: 20px;
                    box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.3);
                    transition: box-shadow 0.3s ease-in-out;
                    cursor: pointer;
                    display: flex
                }
                .item:hover {
                    box-shadow: 0px 0px 20px rgba(0, 0, 0, 0.5);
                }
                .item img {
                    width: 500px;
                    height: 500px;
                }
                .item h2 {
                    text-align: center;
                    font-size: 24px;
                    margin-top: 10px;
                    color: #333;
                }
            </style>
        </head>
        <body>
            <h1>Art Gallery</h1>
            <div class="gallery">
        """
        self.html_ending = """
            </div>
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
        for image in self.image_results:
            f.write("<div class = 'item'><img src=" + image['link'] + "></img><h2>" + image['title'] + "</h2></div>")

        f.write(self.html_ending)
        f.close()

        webbrowser.open_new('output.html')
