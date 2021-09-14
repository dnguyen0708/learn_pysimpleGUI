import PySimpleGUI as sg

#CONSTANT and GLOBAL
sg.theme('Dark Green 5')
queue = {'back':[],'front':[],'result':0,'dot':False,'op_type':"",'xval':0.0,'yval':0.0}

class calculator:

    def calculate(self,op,n1,n2):
        if op == '+':
            return n1+n2
        elif op == '-':
            return n1-n2
        elif op == '*':
            return n1*n2
        elif op == '/':
            try:
                return n1/n2
            except ZeroDivisionError:
                return "Error"
        elif op == '%':
            return n1 % n2

class GUI:

    def __init__(self,title):

        self.title = title
        self.layout = [[sg.Text('0',size=(16,1),font=('Digital-7',47),justification='right',background_color="black",key="SCREEN",text_color='white')],
                        [sg.Button("C",font=('Helvetica', 25),size=(7,2),key="C",button_color="#FCD299"),
                        sg.Button("CE",font=('Helvetica', 25),size=(7,2),key="CE",button_color="#FCD299"),
                        sg.Button("%",font=('Helvetica', 25),size=(7,2),key="%",button_color="#FCD299"),
                        sg.Button("/",font=('Helvetica', 25),size=(7,2),key="/",button_color="#FCD299")],
                        [sg.Button("7",font=('Helvetica', 25),size=(7,2),key=7),
                        sg.Button("8",font=('Helvetica', 25),size=(7,2),key=8),
                        sg.Button("9",font=('Helvetica', 25),size=(7,2),key=9),
                        sg.Button("*",font=('Helvetica', 25),size=(7,2),key='*',button_color="#FCD299")],
                        [sg.Button("4",font=('Helvetica', 25),size=(7,2),key=4),
                        sg.Button("5",font=('Helvetica', 25),size=(7,2),key=5),
                        sg.Button("6",font=('Helvetica', 25),size=(7,2),key=6),
                        sg.Button("-",font=('Helvetica', 25),size=(7,2),key="-",button_color="#FCD299")],
                        [sg.Button("1",font=('Helvetica', 25),size=(7,2),key=1),
                        sg.Button("2",font=('Helvetica', 25),size=(7,2),key=2),
                        sg.Button("3",font=('Helvetica', 25),size=(7,2),key=3),
                        sg.Button("+",font=('Helvetica', 25),size=(7,2),key="+",button_color="#FCD299")],
                        [sg.Button("0",font=('Helvetica', 25),size=(7,2),key=0),
                        sg.Button(".",font=('Helvetica', 25),size=(7,2),key="."),
                        sg.Button("=",font=('Helvetica', 25),size=(15,2),key="=",button_color="orange")]]


        self.window = sg.Window(self.title).Layout(self.layout)
        self.cal = calculator()

    def number_click(self,event):

        if queue['dot']:
            queue['back'].append(str(event))
        else:
            queue['front'].append(str(event))


    def format(self):
        return float(''.join(queue['front'])+'.'+''.join(queue['back']))

    def clear_click(self):
        queue['front'] = []
        queue['back'] = []
        queue['dot'] = False
        queue['result'] = 0
        queue['op_type'] = ""
        self.window["SCREEN"].update(value=0)

    def update_screen(self):

        self.window["SCREEN"].update(value=f"{self.format()}")

    def operator_click(self,event):
        #self.window[event].update(disabled=True)
        if queue['xval'] != 0 or queue['front'] != []:
            if queue['result'] != 0:
                queue['xval'] = queue['result']
            else:
                queue['xval'] = self.format()
            queue['op_type'] = event
            queue['front'] = []
            queue['back'] = []
            queue['dot'] = False
            self.window[event].update(disabled=True)

    def reset(self):
        queue['front'] = []
        queue['back'] = []
        queue['op_type'] = ""



    def get_result(self):

        queue['yval'] = self.format()

        queue['result'] = self.cal.calculate(queue['op_type'],queue['xval'],queue['yval'])

        if queue['result'] == "Error":
            self.window["SCREEN"].update(value="zero division error")
        else:
            self.window["SCREEN"].update(value=f"{queue['result']}")
            self.window[queue['op_type']].update(disabled=False)

            self.reset()



def main():
    g = GUI("SIMPLE calculator")
    c = calculator()

    while True:

        event,values = g.window.Read()

        if event == sg.WIN_CLOSED:
            break

        elif event in ['C','CE']:
            g.clear_click()

        elif event == '.':
            queue['dot'] = True

        elif event in [1,2,3,4,5,6,7,8,9,0]:
            #print(event)
            g.number_click(event)
            g.update_screen()

        elif event in ['+','-','*','/','%']:
            g.operator_click(event)



        elif event == "=":
            g.get_result()

    g.window.close()

if __name__ == "__main__":
    main()