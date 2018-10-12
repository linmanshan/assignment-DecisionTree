from node import Node
import math

def GetRoot(examples, cla):
  '''
  Takes in an array of examples, and returns a tree (an instance of Node) 
  trained on the examples.  Each example is a dictionary of attribute:value pairs,
  and the target class variable is a special attribute with the name "Class".
  Any missing attributes are denoted with a value of "?"
  '''
#cla代表学习目标
  labeldict=GetLabelDict(examples,cla)
  root=Node('',{},examples,[])
  if len(labeldict)==1:
    return root
  else:
    root=build(root,'Class')
    return root



def ID3(examples,default):
  examples=missingSolution1(examples,default)
  examples=missingSolution2(examples,default)
  return GetRoot(examples,'Class')


def build(root,default):
    maxfeature=''
    if root.label=='Class':
      return root
    CurrentInfoGain=0
    for k in root.records[0].keys():
    #每条记录中的每个属性
      if k!='Class' and k not in root.UsedFeatures:
        temp=calGain(root.records,k,'Class')
        if temp>CurrentInfoGain:
          maxfeature=k
          CurrentInfoGain=temp
            #print(CurrentInfoGain)

    if maxfeature=='':
      root.label='Class'
      root.children={}
      d=GetLabelDict(root.records,'Class')
      v=0
      v2=''
      for x in d:
        if d[x]>v:
          v=d[x]
          v2=x
      for record in root.records:
        record['Class']=x

      return root
    root.UsedFeatures.append(maxfeature)
    #print(maxfeature)
    root.label=maxfeature
    #print(root.label)
    #print(maxfeature)
    Attrdict=GetLabelDict(root.records,maxfeature)

    #哪个属性
    for i in Attrdict:
      #属性的值
      
      examples=splitData(root.records,maxfeature,i)
      #print(examples)


      #print(examples)
      root.children[i]=Node('',{},examples,root.UsedFeatures)
    for x in root.children:
      if judgeIfEnd(root.children[x].records,'Class')==True:
        build(root.children[x],'Class')
        return root
      else:
        root.children[x].label='Class'
        #print(root.children.records)
      #return root
    return root

def prune(node, examples):
  '''
  Takes in a trained tree and a validation set of examples.  Prunes nodes in order
  to improve accuracy on the validation data; the precise pruning strategy is up to you.
  '''
  if node.label=='':
    node.children={}
    return node
  #print(node.label)
  infoGain=calGain(node.records,node.label,'Class')
  #print(infoGain)
  if infoGain<1:
    result=GetLabelDict(node.records,'Class')
    max=0
    FrequentPro=''
    for x in result:
        if result[x]>max:
          max=result[x]
          FrequentPro=x
    for record in node.records:
      record['Class']=FrequentPro
    node.children={}
    node.label='Class'

  for x in node.children:
      if judgeIfEnd(node.children[x].records,'Class'):
        prune(node.children[x],node.children[x].records)
        return node

  return node








  #剪枝

def test(node, examples):
  '''
  Takes in a trained tree and a test set of examples.  Returns the accuracy (fraction
  of examples the tree classifies correctly).
  '''
#计算分类的精确比例
  examples=missingSolution1(examples,'democrat')
  examples=missingSolution2(examples,'')
  right=0
  sum=len(examples)
  print(sum)
  for item in examples:
    if item['Class']==evaluate(node,item):
      right+=1
  print(right)
  return right/sum



def evaluate(node, example):

  '''
  Takes in a tree and one example.  Returns the Class value that the tree
  assigns to the example.
  '''
  while(node.children!={}):
    if node.label in example:
      if example[node.label] not in node.children.keys():
        return None
      else:
        node=node.children[example[node.label]]
    else:
      break

  for x in node.records:
    return x['Class']



#给属性 返回预测值


def calEntropy(examples,label):
  '''examples is the dataset which is a list of example
  while label is the attribute that we aim to classify'''
  dic=GetLabelDict(examples,label)

  probability=[]
  for x in dic:
    probability.append(dic[x]/len(examples))
  sum=0
  for i in probability:
    sum+=i*math.log(i,2)
  sum*=-1
  return sum


def GetLabelDict(examples,label):
  dic={}
  for item in examples:
    '''if item[label]=='?':
      continue'''
    if item[label] not in dic:
      dic[item[label]]=1
    else:
      dic[item[label]]+=1
  return dic

def calGain(examples,attr,label):
  #求信息增益
  #S代表原来的信息熵 label是学习目标 attr是属性
  S=calEntropy(examples,label)
  labeldict=GetLabelDict(examples,label)

  attrdict=GetLabelDict(examples,attr)
  EachCount={}
  Tlist=[]
  for i in labeldict:
    for j in attrdict:
      Tlist.append((j,i))
  #(sunny,good)

  for item in examples:
    for (i,j) in Tlist:
      if j==item[attr] and i==item[label]:
        if (j,i)not in EachCount:
          EachCount[(j,i)]=1
        else:
          EachCount[(j,i)]+=1
#(sunny,good)出现的次数


#suuny的熵（类比）
  dicOfEntropy={}
  for (x,y) in EachCount:
    dicOfEntropy[x]=0
    temp=EachCount[(x,y)]/attrdict[x]
    dicOfEntropy[x]-=temp*math.log(temp,2)

#条件熵ST
  ST=0
  for item in dicOfEntropy:
    ST+=attrdict[item]/len(examples)*dicOfEntropy[item]

#返回信息增益
  return S-ST
def splitData(examples,attr,value):
  result=[]
  for i in range(0,len(examples)):
    if examples[i][attr]==value:
      result.append(examples[i])

  return result



def judgeIfEnd(examples,label):
  #判断是否停止分裂
  dic=GetLabelDict(examples,label)
  if len(dic)==1:
    return False
  return True

def missingSolution1(examples,default):
  for example in examples:
      if example['Class']=='?':
        example[item]=default
  return examples
def missingSolution2(examples,default):
  #取众数
  for example in examples:
    for item in example:
      Currendic=GetLabelDict(examples,item)
      max=0
      maxProperty=''
      for k in Currendic:
        if Currendic[k]>max and k!='?':
          max=Currendic[k]
          maxProperty=k
      if example[item]=='?':
        example[item]=maxProperty
  return examples






    












