import pandas as pd

'''This dataset has various features that decide whether a person will play golf or not'''
data = pd.read_csv('golf2.csv')
print(data.shape)
data.head()

#Encoding the labels to 0(No) and 1(Yes)
for i in range(14):
    if data['label'][i] == 'No':
        data['label'][i] = 0
    elif data['label'][i] == 'Yes':
        data['label'][i] = 1
        
data.head()


#Total number of yes and no
num_yes, num_no = 0, 0
for i in range(14):
    if data['label'][i] == 1:
        num_yes += 1
    else:
        num_no += 1
print("Total number of 'Yes':",num_yes, "\nTotal number of 'No'",num_no)


#Finding the conditional probabilities 
#tdict is a ditionary with keys as the distinct values in a column, the corresponding value is a list which stores the 
#following info:
#[num(yes), num(no), P(data|yes), P(data|no)]
def prob_y_n(colName):
    tdict = dict()
    k = list(set(list(data[colName])))
    #print(k)
    for keys in k:
        tdict[keys] = [0, 0, 0, 0]
    
    c = 0
    for keys in data[colName]:
        #l = data['label'][c]
        #print(type(l))
        if data['label'][c] == 1:
            tdict[keys][0] += 1
        else:
            tdict[keys][1] += 1
        c+=1
    
    for k in data[colName]:
        tdict[k][2] = tdict[k][0] / num_yes
        tdict[k][3] = tdict[k][1] / num_no
    return tdict



#list_of_data is a list that stores all the dictionaries returned by prob_y_n()
list_of_data = list()
for c in data.columns:
    list_of_data.append(prob_y_n(c))



for x in list_of_data:
    print(x)
    print('\n\n')



'''This function does the final calculation

    P(Class|outlook, temp, humidity, wind) = P(outlook|Class)*P(temp|Class)*P(humidity|Class)*P(wind|Class)*P(class)

'''

def calc_probability(outlook = None, temp = None, humidity = None, wind = None):
    #prob stores the probability of all the classes
    prob = list()
    for cl in [1, 0]:
        #p_cl = class prior probability
        p_cl = (list_of_data[4][cl][0] + list_of_data[4][cl][1])/list(data.shape)[0]
        #print(p_cl)
        ind = 0
        if cl == 1:
            ind = 0
        else:
            ind = 1
        _ = list_of_data[0][outlook][ind+2] * list_of_data[1][temp][ind+2] * list_of_data[2][humidity][ind+2] * list_of_data[3][wind][ind+2] * p_cl
        prob.append(_)
    
    return prob





ot = input('Enter the outlook, (Sunny, Overcast or Rain): ')
t = input('Enter the temperature, (Hot, Cool or Mild): ')
h = input('Enter the humidity level, (Normal or High): ')
w = input('Enter the wind intensity(Strong or Weak): ')

#prob = calc_probability(outlook = 'Sunny', temp = 'Hot', humidity = 'Normal', wind = 'Weak')
prob = calc_probability(outlook = ot, temp = t, humidity = h, wind = w)


if prob.index(max(prob)) == 0:
    pred = 'YES'
else:
    pred = 'NO'



print(pred)
