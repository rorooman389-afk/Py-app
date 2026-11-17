with open ('R.txt','a+')as outputfile:
    done = input("y/Y")


    while (done != "y") and (done != "Y"):
         id =(input("id"))
         date = input("date:")
         clas = input ("class:")
         outputfile.write(str(id)+date+clas+'/n')
         done = input("y/Y")
