class Node:
  def __init__(self,label,children,records,UsedFeatures):
    self.label = label#标签（用哪个属性划分） ex:weather
    self.children = children #sunny:node1,rainy:node2   字典
    self.records=records # 字典列表
    self.UsedFeatures=UsedFeatures


	