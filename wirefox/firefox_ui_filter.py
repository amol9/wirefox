import re

from .firefox_ui import *
from .firefox_ui_builder import *
from .firefox_paths import *

asc = lambda s : ''.join([c if ord(c) <= 128 else '?' for c in s])


class FirefoxUIFilter:

    class Result:

        def __init__(self, title, url, window, tab):
            self.title  = title
            self.url    = url
            self.window = window
            self.tab    = tab


        def __str__(self):
            return 'title: %s\nurl: %s\nwindow: %02d, tab: %02d'%(asc(self.title), self.url, self.window, self.tab)


    def __init__(self, url='.*', title='.*', window=None, tab=None):
        self.url = re.compile(url)
        self.title = re.compile(title)
        self.firefox_ui = None

        self.build_firefox_ui()

        self.windows = self.enum(window, len(self.firefox_ui.windows), self.firefox_ui.selected_window)
        #print(self.windows)

        max_tabs = max([len(w.tabs) for w in self.firefox_ui.windows])
        self.tabs_sel = False
        self.tabs = self.enum(tab, max_tabs, -1)
        #print(self.tabs)


    def build_firefox_ui(self):
        fpaths = FirefoxPaths()
        recovery_js = None

        with open(fpaths.get_recovery_js_path(), 'rb') as f:
            recovery_js = f.read().decode()

        fub = FirefoxUIBuilder(recovery_js)
        self.firefox_ui = fub.build()

        
    def enum(self, filter, count, sel):
        result = None
        if filter is not None:
            result = []
            parts = filter.split(',')
            for p in parts:
                if p == 'sel':
                    if sel != -1:
                        result.append(sel)
                    else:
                        self.tabs_sel = True
                elif p.find('..') > -1:
                    s, e = map(int, p.split('..')[0: 2])
                    for i in range(s, e + 1):
                        if i < count:
                            result.append(i)
                else:
                    i = int(p)
                    if i < count:
                        result.append(i)
        else:
            result = range(0, count)

        result = list(set(result))
        return result

    def result(self):
        results = []
        for w in self.firefox_ui.windows:
            if w.index in self.windows:
                for t in w.tabs:
                    if (t.index in self.tabs) or (self.tabs_sel and t.selected):
                        #print(asc(t.url))
                        if self.title.search(t.title) and self.url.search(t.url):
                            results.append(FirefoxUIFilter.Result(t.title, t.url, w.index, t.index))

        return results        
    