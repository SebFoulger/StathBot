a = ["asf,1\n","bsdf,5\n","sdf,2\n","zfgthjg,34\n"]

b = input("Input name: ")
c = int(input("Input number: "))

n = len(a)

p = 0
q = n

while p<q:
    m=(p+q)//2
    if a[m]<b:
        p=m+1
    else:
        q=m

if p!=n:
    if a[p].split(",")[0]==b:
        temp = a[p].strip("\n").split(",")
        a[p]=temp[0]+","+str(int(temp[1])+1)+"\n"
    else:
        a.insert(p,b+"1"+"\n")
else:
    a.append(b+"1"+"\n")

print(a)


