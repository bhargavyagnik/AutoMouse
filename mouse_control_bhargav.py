import pyautogui

#old=[50,50] # where the hand was detected
#new=[120,100] # where the hand is detected now

rect=[400,400]      #Rectangle where the hand is observed
dim=pyautogui.size()  # Dimension of Screen

sensitivity= 3 #Scale like 1,2,3,4,5 where 1 is lowest sensitiviy and 5 max

ani=1/sensitivity

def move_mouse(old,new,rect=[400,400]):    
    X=(new[0]-old[0])*dim[0]/(rect[0]*ani)
    Y=(new[1]-old[1])*dim[1]/(rect[1]*ani)
    x,y=pyautogui.position()
    if x-abs(X) in range(dim[0]+1) and y-abs(Y)>0 in range(dim[1]+1):
        print(X,Y)
        pyautogui.move(X,Y,ani,pyautogui.easeInOutQuad)
    elif x-abs(X) in range(dim[0]+1):
        print(X,y)
        pyautogui.move(X,y,ani,pyautogui.easeInOutQuad)
    elif  y-abs(Y) in range(dim[1]+1):
        print(x,Y)
        pyautogui.move(x,Y,ani,pyautogui.easeInOutQuad)


def drag_mouse(old,new,rect=[400,400]):    
    X=(new[0]-old[0])*dim[0]/rect[0]
    Y=(new[1]-old[1])*dim[1]/rect[1]
    #print(X,Y)
    pyautogui.drag(X,Y,ani,button='left')



def click_mouse(cliks,buttn):
    pyautogui.click(clicks=cliks,button=buttn)

def scroll_mouse(level=5):
    pyautogui.scroll(level)


move_mouse([100,100],[100,150])
scroll_mouse()


