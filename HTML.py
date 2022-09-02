


class Parser:
    def __init__(self,filename):
        self.parsed = []
        self.results = ''
        with open(filename,'r') as f:
            self.data = f.read().split('<!---->')
        for i in self.data:
            self.parsed.append('')

    def Add(self,section,variables=None):
        html = self.data[section]
        if(variables == None):
            self.parsed[section] += html
        else:
            for i in variables:
                html = html.replace(i,str(variables[i]))
            self.parsed[section] += html
        return html

    def Remove(self,section):
        self.data[section] = ''
        return True

    def Generate(self):
        n = 0
        for i in self.parsed:
            #if(i == ''):
            #    self.results += self.data[n]
            #else:
            self.results += i
            #n += 1
        return self.results
