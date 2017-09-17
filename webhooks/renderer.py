import yattag



class HtmlDoc(yattag.SimpleDoc):
    def render(self):
        return '<!DOCTYPE html>' + self.getvalue()
