import torch
gnome="ATATGA"
dic={"A":0.,"T":1.,"C":2.,"G":3.}
g1_tensor=torch.tensor([dic[gnome[0]],dic[gnome[1]],dic[gnome[2]]])
a=3
while a!=len(gnome):
    g2_tensor=torch.tensor([dic[gnome[a]],dic[gnome[a+1]],dic[gnome[a+2]]])
    g1_tensor=torch.cat((g1_tensor,g2_tensor))
    a+=3
print(g1_tensor)
