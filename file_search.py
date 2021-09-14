import os
import pickle
import PySimpleGUI as sg

sg.ChangeLookAndFeel("Dark")
class GUI:

    def __init__(self):
        self.layout = [[sg.Text("Search Term:",size=(10,1)),
                        sg.Input(size=(45,1),focus=True,key="TERM"),
                        sg.Radio("Contains",group_id='choice',key="CONTAINS",default=True),
                        sg.Radio("StartsWith",group_id='choice',key="START"),
                        sg.Radio("EndsWith",group_id='choice',key="END")],
                       [sg.Text("Root Path:",size=(10,1)),
                       sg.Input('C:\\Users\\Nguyen\\Downloads\\',size=(45,1),key="PATH"),
                       sg.FolderBrowse("Browse",size=(10,1)),
                       sg.Button("Re-Index",size=(10,1),key="INDEX"),
                       sg.Button("Search",size=(10,1),key="SEARCH")],
                       [sg.Output(size=(100,30))]]
        self.window = sg.Window("simple search engine").Layout(self.layout)

class file_search:

    def __init__(self):
        self.files = []
        self.result = []
        self.matches = 0
        self.records = 0

    def create_new_index(self,values):

        root_path = values["PATH"]

        self.files = [(root,files) for root,dirs,files in os.walk(root_path) if files]

        with open("save_index.pkl",'wb') as file_out:
            pickle.dump(self.files,file_out)

    def load_index(self):

        try:

            with open("save_index.pkl",'rb') as file_in:
                self.files = pickle.load(file_in)

        except:

            self.files = []


    def search(self,values):
        
        #reset search result
        self.result.clear()
        self.matches=0
        self.records=0

        term = values["TERM"]

        #perform search
        for path,files in self.files:
            for file in files:
                self.records+=1
                if( values["CONTAINS"] and term.lower() in file.lower() or 
                    values["START"] and file.lower().startswith(term.lower()) or 
                    values["END"] and file.lower().endswith(term.lower())):

                    self.matches+=1
                    result =  path.replace('\\','/') + '/' + file
                    self.result.append(result)
                else:
                    continue


        #save result
        with open("search_results.txt",'w',encoding="utf-8") as f:
            for result in self.result:
                f.write(result+'\n')

def testcase1():
    fs = file_search()
    #fs.create_new_index("C:\\Users\\Nguyen\\Downloads\\")
    fs.load_index()

    fs.search("mp4")

    print(f"there are {fs.matches} matches in {fs.records} records")
    print()
    print("these are the matches: ")
    for match in fs.result:

        print(match)
#testcase1()
def testGUI():
    g = GUI()
    while True:

        event,values = g.window.Read()
        if event == sg.WIN_CLOSED or event == "Cancel":
            break

        if event == "SEARCH":
            print("results goes here")


    g.window.close()


def main():
    s= file_search()
    g=GUI()
    s.load_index()

    while True:

        event,values = g.window.Read()

        if event == sg.WIN_CLOSED:
            break

        if event == "INDEX":
            print("index")
            s.create_new_index(values)

            print()
            print("New Index Created")
            print()

        if event == "SEARCH":

            s.search(values)
            print(f"there are {s.matches} matches in {s.records} records")
            print()
            print("these are the matches: ")
            for match in s.result:

                print(match)

main()