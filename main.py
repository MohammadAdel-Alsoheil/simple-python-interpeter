#from shell2 import Map
LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
regs = {"x0":"","x1":"","x2":"","x3":"","x4":"","x5":"","x6":"","x7":"","x8":"","x9":""}
definedVars = []
barmajehFlag = False
tejhizFlag = False
Flag = False

lst = []
Lcounter = 0
Tempcounter = 0

def main():
    global Flag
    global Lcounter
    global Tempcounter
  
    filename = "yayy.bbl"
    
    
    file = open(filename,"r")
    
    if checkIndentation(filename):
        for line in file:
        
            
            exp = ""


            check = line.split()
            
            if line.strip():
                #print(check)
                if check[0] == "tejhez#" and len(check) == 1:
                    tejhizFlag = True
                    barmajehFlag = False

                elif check[0] == "barmajeh#" and len(check) == 1:
                    barmajehFlag = True
                    tejhizFlag = False

                if tejhizFlag == True and  check[0]=="ra2m":
                        if AssigIntchecker(check):
                            exp+="mov "+setValue(check[1])+" ,#"+check[3]
                            definedVars.append(check[1])
                        if exp != "" :
                            lst.append(exp)
                        
                if tejhizFlag == True and check[0] in LETTERS:
                        if AssignVarChecker(check):
                            exp+="addi "+setValue(check[0])+" ,"+setValue(check[2])+" ,#0"
                        if exp != "" :
                            lst.append(exp)
                        
                if barmajehFlag == True and check[0] in LETTERS :
                        if checkAnd(check) and Flag == False:
                            exp+="AND "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                        elif checkOrr(check)  and Flag == False:
                            exp+="ORR "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                        elif checkAnd(check) and Flag == True:
                            exp+="L"+str(Lcounter)+": "
                            exp+="AND "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                            Lcounter+=1
                        elif checkOrr(check)  and Flag == True:
                            exp+="L"+str(Lcounter)+": "
                            exp+="ORR "+setValue(check[0])+" ,"+setValue(check[2])+" ,"+setValue(check[4])
                            Lcounter+=1
                        
                        if exp != "" :
                            lst.append(exp)
                if barmajehFlag == True and check[0] == "iza" and check[-1] == ":":
                        #print(check)
                        #print(checkIf(check))
                        if checkIf(check):
                        
                            if check[1] in definedVars and check[-2] in definedVars:
                                exp+="SUB "+setValue("temp"+str(Tempcounter))+" ,"+setValue(check[1])+" ,"+setValue(check[-2])
                                definedVars.append("temp"+str(Tempcounter))
                                lst.append(exp)
                                exp=""
                                exp+="CBZ "+get_keys_by_value(regs,"temp"+str(Tempcounter))[0]+", L"+str(Lcounter)   
                                lst.append(exp)                 
                                Flag=True
                                Tempcounter+=1
        return lst
    else:
        raise ValueError("there is an error in your program")

def get_keys_by_value(dct, value):
    return [k for k, v in dct.items() if v == value]
      
                                
def setValue(value):
   
    for key in regs:
        if regs[key] == value:
            return key
    for key in regs:
        if regs[key] == "":
            regs[key] = value
            return str(key)
    raise ValueError("All registers are full")



def checkIf(arr):
    if len(arr) != 5:
        return False
    if arr[1] not in definedVars :
        return False
    if arr[2] != "=":
        return False
    if arr[3] not in definedVars:
        return False
    return True
    
def checkOrr(arr):
     if(len(arr)!= 5):
        return False
     if arr[0] not in LETTERS:
        return False
     if arr[2] not in definedVars  :
        return False
     if arr[1] != "=":
        return False
     if arr[3] != "|":
         return False
     if arr[4] not in definedVars:
         return False
        
     return True
        
def checkAnd(arr):
     if(len(arr)!= 5):
        return False
     if arr[0] not in LETTERS:
        return False
     if arr[2] not in definedVars  :
        return False
     if arr[1] != "=":
        return False
     if arr[3] != "&":
         return False
     if arr[4] not in definedVars:
         return False
        
     return True

def AssignVarChecker(arr):
    if(len(arr)!= 3):
        return False
    if arr[0] not in LETTERS:
        return False
    if arr[2] not in definedVars:
        return False
    if arr[1] != "=":
        return False
    return True

     
def AssigIntchecker(arr):
    if(len(arr)!= 4):
        return False
    if arr[0] != "ra2m":
        return False
    if arr[1] not in LETTERS:
        return False
    if arr[2] != "=":
        return False
    if not arr[3].isnumeric():
        return False
    return True

def countTabs(filename):
    file = open(filename,"r")
    TabList = [] 
    for line in file:
        counter = 0
        if line.strip():
            for i in line :
                if i != "\t":
                        TabList.append(counter)
                        break
                counter+=1
    return TabList

def checkIndentation(filename):
   
    lst = ["barmajeh#","tejhez#","iza"]
    indentation_lst = countTabs(filename)
    first_word_lst = getFirstWord(filename)
    stack = []
    for i in range(len(indentation_lst)-1):
        if first_word_lst[i] in lst and len(stack) == 0 :
                stack.append(first_word_lst[i])
        if first_word_lst[i] in lst and len(stack) != 0:
                return True


def getFirstWord(filename):
    file = open(filename,"r")
    lst = []
    for line in file:
        if line.strip():
            lst.append(line.split()[0])
    return lst



 
if __name__ == "__main__":
    Main = main()
    print(Main)
    print(regs)
    newFile = open("RunMe.s","w")
    for i in Main:
        newFile.write("\n")
        newFile.write(i)
    


    """flaws of the program indentation must be coded correctly we had no time to fix it 
       The program wouldve been better if it were coded in OOP """


