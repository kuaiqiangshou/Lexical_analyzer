'''
Created on 2017年3月18日

@author: liuyifeng

    '''
import re
import itertools


# list--"key" store some keywords of the EBNF grammar. there is no blacks in the "end if" and "end while".
key = [';','=','+','-','*','/','%','(',')','read','print','int','float','boolean','if','{','}',
           ':','else','endif','end','while','do','endwhile','and','or','>','<','>=','==']


# count the number of lines in input.
def number_lines ():
    number_of_lines = 0
    file_object = open('input_program.txt') 
    lines = file_object.readlines()
    for line in lines:
        number_of_lines = number_of_lines +1    
    
    file_object.close() 
    
    return number_of_lines


# Using input function to input a expression(string)    
def expression(line_number):

    file_object = open('input_program.txt')  
    lines = file_object.readlines()    
    str_input = lines[line_number]   
    file_object.close()  
    
    return str_input
    
# convert the input string to a list    
def con_list(str_input):
    con_input = list(str_input)

    chunks = [] #store the transfered list
    chunk = []
  
    for le in range(len(con_input)):
        if con_input[le] != ' ' and con_input[le] not in key :
            chunk.append(con_input[le])
        elif le == len(con_input)-1 or con_input[le] == " " or (con_input[le] in key) :
            if chunk != []:
                chunks.append(chunk)
            chunks.append([con_input[le]])
            chunk = []   
    return chunks
    
# transfer the list into a type which can be used by function tokenType
def con_token(chunks):  
    
    out_token = []

    for le in range(len(chunks)):
        var = "".join(itertools.chain(*chunks[le]))
        out_token.append(var)

    return out_token

#generate the token_type of the code.
def tokenType(out_token,line_number):
#    print(out_token)
#     print("The out_token of line_",line_number,"is:")
    ad = ' '
    out_token.extend(10*ad)
    token_type = []
    count = 0
    for le in range(0,len(out_token)):

        if out_token[le] not in key:
            if re.match('^[A-z]+$',out_token[le]):
                token_type = token_type + ['VAR_CODE']
            
            elif out_token[le].isdigit():
                token_type = token_type + ['DIGIT_CODE']
            
            elif "." in out_token[le]:
                for a in out_token[le]:
                    if a == '.':
                        count = count +1
                if count >= 2 :
                    print("float number type wrong.")
                
                elif out_token[le][0] == "." or out_token[le][len(out_token[le])-1] == '.':
                    print("float number type wrong.")
                                   
                else:
                    token_type = token_type + ['FLOAT_num']
            
            elif out_token[le]== " " or "" :
                pass
            
            else:
                print("error happen in VAR, the characters of variable must in alphabet.")
        
        elif out_token[le] in key:
            if out_token[le] == '=':
                token_type = token_type + ['ASSIGN_OP']
            
            elif out_token[le] == '+' or out_token[le] =='-':
                token_type = token_type + ['ADD_OP']
            
            elif out_token[le] == '*' or out_token[le] =='/' or out_token[le] == '%':
                token_type = token_type + ['MULTIPLY_OP']
            
            elif out_token[le] == ";":
                token_type = token_type + ['SEMICOLON']
            
            elif out_token[le] == "int" or out_token[le] =="float" or out_token[le] =="boolean":
                token_type = token_type +['TYPE']
            
            elif out_token[le] == "read":
                token_type = token_type +['READ_OP']
            
            elif out_token[le] == "print":
                token_type = token_type +['PRINT_OP']
            
            elif out_token[le] == "and" or out_token[le] == "or":
                token_type = token_type +['LOGICAL_OP']
            
            elif out_token[le] == ">" or out_token[le] =="<" or out_token[le] == ">=" or out_token[le] =="<=" :
                token_type = token_type +['VALUE_OP']
            
            elif out_token[le] == "(":
                token_type = token_type +["left_pa"]
            
            elif out_token[le] == ")":
                token_type = token_type +["right_pa"]

#if and while token types:            
            elif out_token[le] == "if":
                token_type = token_type +['IF_OP']    
            
            elif out_token[le] == "else":
                token_type = token_type +['ELSE_OP']                           
           
            elif out_token[le] == ":":
                token_type = token_type +['COLON']                                           
           
            elif out_token[le] == "endif":
                token_type = token_type +['ENDIF_OP']
            
            elif (out_token[le] == "end" and out_token[le+2] == "if"):
                token_type = token_type +['ENDIF_OP']
                out_token[le+2] = ' '
                                         
            elif out_token[le] == "while":
                token_type = token_type +['WHILE_OP']              
           
            elif out_token[le] == "do":
                token_type = token_type +['DO_OP']               
           
            elif out_token[le] == "endwhile":
                token_type = token_type +['ENDWHILE_OP']
            
            elif (out_token[le] == "end" and out_token[le+2] == "while"):
                token_type = token_type +['ENDWHILE_OP']
                out_token[le+2] = ' '
                          
            
    return token_type


        
# Using token_type to check if the grammar of the code is right or not.     
def check(token_type,line_number):
    sample_of_token_type = ['VAR_CODE','DIGIT_CODE','ASSIGN_OP','ADD_OP','MULTIPLY_OP','SEMICOLON','TYPE','READ_OP','PRINT_OP','LOGICAL_OP','VALUE_OP',
              "left_pa","right_pa",'IF_OP','ELSE_OP','COLON','ENDIF_OP','WHILE_OP','DO_OP','ENDWHILE_OP']
  
    index_left_pa = 0 # count the number of left_pa in an expression
    index_right_pa = 0 #count the number of right_pa in an expression

    chunks = [] # the output of token_type by dividing of "semicolon"
    chunk = [] # median variable for storing list
# divide the statement according to "semicolon and colon".   
    for le in range(len(token_type)):
        chunk.append(token_type[le])
        if le == len(token_type)-1 or token_type[le] == "SEMICOLON" or token_type[le] == "COLON" or token_type[le] == "DO_OP":
            chunks.append(chunk)
            chunk = []   
     
#    print(chunks)

# analysis the expressions. 
    for i in range(len(chunks)):      
#judge if the statement is var_dec or not.
        if chunks[i][0] == "TYPE" :            
            if len(chunks[i])>=3 and chunks[i][len(chunks[i])-1] == "SEMICOLON":
                if chunks[i][1] != "VAR_CODE":
                    print ("ERROR!!!","line_",line_number+1," The expression of var_dec IS WRONG. Lack VAR_CODE.")
                    return False
            
                elif chunks[i][1] == "VAR_CODE":
                    if chunks[i][2] != "SEMICOLON":
                        print ("ERROR!!!","line_",line_number+1," There is no semicolon in the final of the statement.")
                        return False
                    else:
                        pass
#                        print ("Correct grammar in line_",line_number+1)
                        return True 
                else: 
                    print("ERROR!!!","line_",line_number+1," Wrong var_dec statement.")
                    return False
            
            else: 
                    print("ERROR!!!","line_",line_number+1," Wrong var_dec statement.Lack element of var_dec statement.")
                    return False

#judge if the statement is assign or not.     
        elif chunks[i][0] == "VAR_CODE":
            if len(chunks[i]) >= 4 and chunks[i][len(chunks[i])-1] == "SEMICOLON":
                if chunks[i][1] == "ASSIGN_OP":
                    if "left_pa" not in chunks[i]:
                        if "right_pa" not in chunks[i]: 
     
#using check_expr function to check if the grammar of expression is right or not. if it's right return value 1 and wrong return value 0.
                            chunks[i] = chunks[i][2:len(chunks[i])-1]

                            if check_expr(chunks[i]) == 1:
                                pass
                                return True
#                                 print("Correct grammar with assign statement in line_", line_number+1)
                            elif check_expr(chunks[i]) == 0:
                                print("ERROR!!!","line_",line_number+1," Error! the grammar of assign statement is wrong.")
                                return False
                        else:
                            print("ERROR!!!","line_",line_number+1," Error! the grammar of assign statement is wrong.")
                            return False
                        
#check if there are parentheses in this statement:
                    elif "left_pa" in chunks[i]:
                        for pa in range(len(chunks[i])):
                            if chunks[i][pa] == "left_pa":
                                index_left_pa = index_left_pa+1;
                            elif chunks[i][pa] == "right_pa":
                                index_right_pa = index_right_pa +1;
                        
                        if index_left_pa != index_right_pa:
                            print("ERROR!!!","line_",line_number+1," Error! Wrong assign statement. the numbers of left and right Parentheses are not equal.")
                            return False
                        
                        elif index_left_pa == index_right_pa:
                            chunks[i] = chunks[i][2:len(chunks[i])-1]
   
                            while "left_pa" in chunks[i]:
                                chunks[i].remove("left_pa")
                            while "right_pa" in chunks[i]:
                                chunks[i].remove("right_pa")

                            if check_expr(chunks[i]) == 1:
                                pass
                                return True
#                                print("Correct grammar with assign statement in line_", line_number+1)
                            elif check_expr(chunks[i]) == 0:
                                print("ERROR!!!","line_",line_number+1," Error! the grammar of assign statement is wrong.") 
                                return False 
                        
                        index_left_pa = 0
                        index_right_pa = 0             
                else:
                    print("ERROR!!!","line_",line_number+1," Error! wrong assign statement.")
                    return False
            else:
                print("ERROR!!!","line_",line_number+1," Error!.Lack element of assign statement.")
                return False

#judge if the statement is read_stat or not.
        elif chunks[i][0] == "READ_OP":
            if len(chunks[i]) >= 5 and chunks[i][len(chunks[i])-1] == "SEMICOLON":
                if chunks[i][1] == "left_pa" and chunks[i][len(chunks[i])-2] == "right_pa":

                    chunks[i] = chunks[i][2:len(chunks[i])-2] 

                    if "left_pa" not in chunks[i]:
                        if "right_pa" not in chunks[i]:
                            if check_expr(chunks[i]) == 1:
                                pass
                                return True
#                                print("Correct grammar with read statement in line_", line_number+1)
                            elif check_expr(chunks[i]) == 0:
                                print("ERROR!!!","line_",line_number+1," Error! the grammar of read statement is wrong.")
                                return False
                        else:
                            print("ERROR!!!","line_",line_number+1," Error! the grammar of read statement is wrong.")
                            return False
                        
                    elif "left_pa" in chunks[i]:
                        for pa in range(len(chunks[i])):
                            if chunks[i][pa] == "left_pa":
                                index_left_pa = index_left_pa+1;
                            elif chunks[i][pa] == "right_pa":
                                index_right_pa = index_right_pa +1;
                        
                        if index_left_pa != index_right_pa:
                            print("ERROR!!!","line_",line_number+1," Error! Wrong read statement. the numbers of left and right Parentheses are not equal.")
                            return False
                        
                        elif index_left_pa == index_right_pa:
                            chunks[i] = chunks[i][2:len(chunks[i])-2]
                            while "left_pa" in chunks[i]:
                                chunks[i].remove("left_pa")
                            while "right_pa" in chunks[i]:
                                chunks[i].remove("right_pa")

                            if check_expr(chunks[i]) == 1:
                                pass
                                return True
#                                 print("Correct grammar with read statement in line_", line_number+1)
                            elif check_expr(chunks[i]) == 0:
                                print("ERROR!!!","line_",line_number+1," Error! the grammar of read statement is wrong.")
                                return False  
                        
                        index_left_pa = 0
                        index_right_pa = 0                                                      
                else:
                    print("ERROR!!!","line_",line_number+1," Error! wrong read statement.")
                    return False
            else:
                print("ERROR!!!","line_",line_number+1," Error!.Lack element of read statement.")
                return False

#judge if the statement is print_stat or not.
        elif chunks[i][0] == "PRINT_OP":
            if len(chunks[i]) >= 5 and chunks[i][len(chunks[i])-1] == "SEMICOLON":
                if chunks[i][1] == "left_pa" and chunks[i][len(chunks[i])-2] == "right_pa":
                    chunks[i] = chunks[i][2:len(chunks[i])-2] 

                    if "left_pa" not in chunks[i]:
                        if "right_pa" not in chunks[i]:
                            if check_expr(chunks[i]) == 1:
                                pass
                                return True
#                                 print("Correct grammar with print statement in line_", line_number+1)
                            elif check_expr(chunks[i]) == 0:
                                print("ERROR!!!","line_",line_number+1," Error! the grammar of print statement is wrong.")
                                return False
                        else:
                            print("ERROR!!!","line_",line_number+1," Error! the grammar of print statement is wrong.")
                            return False
                        
                    elif "left_pa" in chunks[i]:
                        for pa in range(len(chunks[i])):
                            if chunks[i][pa] == "left_pa":
                                index_left_pa = index_left_pa+1;
                            elif chunks[i][pa] == "right_pa":
                                index_right_pa = index_right_pa +1;
                        
                        if index_left_pa != index_right_pa:
                            print("ERROR!!!","line_",line_number+1," Error! Wrong print statement. the numbers of left and right Parentheses are not equal.")
                            return False
                        
                        elif index_left_pa == index_right_pa:
                            chunks[i] = chunks[i][2:len(chunks[i])-2]
                            while "left_pa" in chunks[i]:
                                chunks[i].remove("left_pa")
                            while "right_pa" in chunks[i]:
                                chunks[i].remove("right_pa")

                            if check_expr(chunks[i]) == 1:
                                pass
                                return True
#                                 print("Correct grammar with print statement in line_", line_number+1)
                            elif check_expr(chunks[i]) == 0:
                                print("ERROR!!!","line_",line_number+1," Error! the grammar of print statement is wrong.")
                                return False  
                        
                        index_left_pa = 0
                        index_right_pa = 0  
                        
                else:
                    print("ERROR!!!","line_",line_number+1," Error! wrong print statement.")
                    return False
            else:
                print("ERROR!!!","line_",line_number+1," Error!.Lack element of print statement.")
                return False
         
# judge the the statement is "if statement" or not.
        elif chunks[i][0] == "IF_OP":
            if len(chunks[i]) >= 3 and chunks[i][len(chunks[i])-1] == "COLON":
                if chunks[i][1] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")        
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=7 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
               
                elif len(chunks[i]) >=7 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "VAR_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "VAR_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"if" +"statement correct at first part.")
                
                else: 
                    print("ERROR!!!","line_",line_number+1," Error! the "+"if" +" statement is wrong at first part.")
                    return False
            else:
                print("ERROR!!!","line_",line_number+1,"Error! the "+"if" +"statement is wrong at first part.")
                return False
        
        elif chunks[i][0] == "ELSE_OP":
            if len(chunks[i]) >3 :
                print("ERROR!!!","line_",line_number+1," Error! the else statement is wrong as second part of if statement.")
                return False
            if len(chunks[i]) ==2 and chunks[i][1]== "COLON":
                pass
                return True
#                print("the else statement is correct as second part of if statement.")
            else:
                print("ERROR!!!","line_",line_number+1," Error! the else statement is wrong as second part of if statement.")
                return False
        
        elif chunks[i][0] == "ENDIF_OP":
            if len(chunks[i]) >3 :
                print("ERROR!!!","line_",line_number+1," Error! the endif statement is wrong as third part of if statement.")
                return False
            if len(chunks[i]) ==2 and chunks[i][1]== "SEMICOLON":
                pass
                return True
#                print("the endif statement is correct as third part of if statement.")
            else:
                print("ERROR!!!","line_",line_number+1," Error! the endif statement is wrong as third part of if statement.")
                return False

# judge the the statement is "while statement" or not.        
        elif chunks[i][0] == "WHILE_OP":
            if len(chunks[i]) >= 3 and chunks[i][len(chunks[i])-1] == "DO_OP":
                if chunks[i][1] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")        
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=5 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=7 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
               
                elif len(chunks[i]) >=7 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "VAR_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "VAR_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "VAR_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "DIGIT_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "DIGIT_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                elif len(chunks[i]) >=9 and chunks[i][1] == "DIGIT_CODE" and chunks[i][2] == "VALUE_OP" and chunks[i][3] == "DIGIT_CODE" and chunks[i][4] == "LOGICAL_OP" and chunks[i][5] == "VAR_CODE" and chunks[i][6] == "VALUE_OP" and chunks[i][7] == "VAR_CODE":
                    pass
                    return True
#                    print("the "+"while" +"statement correct at first part.")
                
                else: 
                    print("ERROR!!!","line_",line_number+1," Error! the "+"while" +" statement is wrong at first part.")
                    return False
            else:
                print("ERROR!!!","line_",line_number+1," Error! the "+"while" +" statement is wrong at first part.")
                return False
        
        elif chunks[i][0] == "ENDWHILE_OP":
            if len(chunks[i]) >3 :
                print("ERROR!!!","line_",line_number+1," Error! the endwhile statement is wrong as third part of while statement.")
                return False
            if len(chunks[i]) ==2 and chunks[i][1]== "SEMICOLON":
                pass
                return True
#                print("the endwhile statement is correct as third part of while statement.")
            else:
                print("ERROR!!!","line_",line_number+1," Error! the endwhile statement is wrong as third part of while statement.")
                return False
        
        else:
            print("ERROR!!!","line_",line_number+1," Error! wrong type of the beginning of the expression.")
            return False

    
# this function is used to check if the "expression" is true or false.
def check_expr(listin):
    index_var = 0 #count the number of variable
    index_add_op = 0 #count the number of addition or multiply operation
   
    for va in range(len(listin)):
        if listin[va] == "VAR_CODE" or listin[va] == "DIGIT_CODE" or listin[va] == "FLOAT_num":
            index_var = index_var +1;
        elif listin[va] == "ADD_OP" or listin[va] == "MULTIPLY_OP":
            index_add_op = index_add_op +1
    
    temple = index_var -1
    check = 0
    if index_add_op == temple:            
        check = 1
    elif index_add_op != temple:
        check = 0
    
    return check
        

# Function of running the lexical analyzer   
def run ():    
# Variable "whole_if" is used to store the if statement.    
    whole_if = []
# Variable "whole_while" is used to store the while statement.  
    whole_while = []

    flag_if = 0
    flag_while = 0

    check_error_number =0
# Variable "number" is the number of lines in the file.      
    number = number_lines();     
    for n in range(0,number):
        z = expression(n)
        y = con_list(z)
        o = con_token(y) 
        k = tokenType(o,n+1)
#        print(k)
        if (("IF_OP") in k or ("ENDIF_OP" in k)):
            flag_if = n+1;
        
        if (("WHILE_OP") in k or ("ENDWHILE_OP" in k)):
            flag_while = n+1;
        
        if (("IF_OP" in k) or ("ELSE_OP" in k) or ("ENDIF_OP" in k)):
            whole_if.extend(k)      
       
        if (("WHILE_OP" in k) or ("ENDWHILE_OP")in k):
            whole_while.extend(k)
     
        b = check(k,n)
        if (b == True):
            check_error_number = check_error_number + 0
        elif (b == False):
            check_error_number = check_error_number + 1
    
    if (check_error_number == 0 ):
        print ("The program is type error free.")
    else:
        print("ERROR!!! Happens")
   
    number_if = whole_if.count("IF_OP")
    number_endif = whole_if.count("ENDIF_OP")    
    number_while = whole_while.count("WHILE_OP")
    number_endwhile = whole_while.count("ENDWHILE_OP")    
     
    if (number_if != number_endif):
        print("ERROR!!! line_",flag_if," ERROR!.IF_Statement lack element.")
    if (number_while != number_endwhile):
        print("ERROR!!! line_",flag_while," ERROR!.While_Statement lack element.")
       
    return ''


r = run()



