class FirefoxUI:

    def __init__(self):
        self.windows = []
        self.selected_window = None

    def get_selected_window(self):
        return self.selected_window


    def __str__(self):
        s = ''
        s += 'Windows: %02d, Selected Window: %02d'%(len(self.windows), self.selected_window)
        for w in self.windows:
            s += '\n' + str(w)

        return s

    def add_window(self, window):
        self.windows.append(window)
        if window.selected:
            self.selected_window = window.index

class Window:

    def __init__(self, index, selected=False):
        self.tabs = []
        self.index = index
        self.selected = selected
        self.selected_tab = None


    def add_tab(self, tab):
        self.tabs.append(tab)
        if tab.selected:
            self.selected_tab = tab.index


    def get_selected_tab(self):
        return None


    def __str__(self):
        s = 'Window [index: %02d, tabs: %02d, selected tab: %02d]'%(self.index, len(self.tabs), self.selected_tab or -1)

        for t in self.tabs:
            s += '\n ' + str(t)

        return s

class Tab:

    def __init__(self, index, title, url, selected=False):
        self.index = index
        self.title = title
        self.url = url
        self.selected = selected


    def __str__(self):
        return 'Tab [index: %02d, title: %-30s, url: %-30s, selected: %d]'%(self.index, asc(self.title[0:30]), self.url[0:30], self.selected)


asc = lambda s : ''.join([c if ord(c) <= 128 else '?' for c in s])


