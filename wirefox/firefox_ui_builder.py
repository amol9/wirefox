import json

from .firefox_ui import *


class FirefoxUIBuilder:

    def  __init__(self, json_str):
        self.json_obj = self.make_json_obj(json_str)
        self.firefox_ui = FirefoxUI()

    def make_json_obj(self, json_str):
        return json.loads(json_str)        

    def build(self):
        j = self.json_obj
        #import pdb; pdb.set_trace()

        if len(j['windows']) == 0:
            self.no_windows = True
            return

        w_index = 0
        swin = j['selectedWindow'] - 1
        for w in j['windows']:
            nw = self.add_window(w_index, selected=(w_index==swin))
            tabs = w['tabs']
            if len(tabs) == 0:
                nw.no_tabs = True
                break

            stab = w['selected'] - 1

            t_index = 0
            for i, t in enumerate(tabs):
                e = t['entries'][-1]
                nw.add_tab(Tab(t_index, e['title'], e['url'], selected=(i==stab)))

                t_index += 1

            w_index += 1

        return self.firefox_ui

    
    def add_window(self, index, selected=False):
        w = Window(index, selected=selected)
        self.firefox_ui.add_window(w)

        #self.firefox_ui.selected_window = len(self.firefox_ui.windows) - 1

        return w
        