#Seth Turnage
#ASU Student
#Python program to help with getting info from access to sql for homework
#Reads a comma delimited csv and writes to sql query file
import csv
import os
import sys
#put the local urls of the files you want to convert here
COMMENTS = True
FILEINDEX = 0
DELIMITERINDEX = 1
CSV_Files_To_Be_Converted = [["CSV/application.csv","\t"],["CSV/applicationAssignedToReviewer.csv",","],["CSV/applicationPhoneNumber.csv",","],["CSV/job.csv",","],["CSV/jobHasRequirement.csv",","],["CSV/jobRequirement.csv",","],["CSV/recruiter.csv",","],["CSV/reference.csv",","],["CSV/referenceRatesApplicant.csv",","],["CSV/reviewer.csv",","],["CSV/reviewerRatesApplication.csv",","]]

Create_SQL_URL = "create.sql"
Insert_SQL_URL = "insert.sql"

try:
    os.remove(Create_SQL_URL)
except OSError:
    pass

try:
    os.remove(Insert_SQL_URL)
except OSError:
    pass

user_comment_choice_input = input("Would you like comments in your output files?(Y/n) [Some systems don't support them.]\n")
if (str(user_comment_choice_input) in ["Y","y","Yes","yes"]):
    COMMENTS = True
elif (str(user_comment_choice_input) in ["N","n","No","no"]):
    COMMENTS = False
else:
    print("Not a valid input. Setting comments to false, just in case.\n")
    COMMENTS = False

for CURRENT_FILE in range(0,CSV_Files_To_Be_Converted.__len__()):
    with open(CSV_Files_To_Be_Converted[CURRENT_FILE][FILEINDEX],'r') as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter=CSV_Files_To_Be_Converted[CURRENT_FILE][DELIMITERINDEX])
        TableName = "TableNameHere"
        DictionaryKeys = []
        ColumnType = []
        ByteLength = []
        with open(Insert_SQL_URL, 'a') as insert_file:
            TableName = os.path.splitext(os.path.basename(csv_file.name))[0]
            if(COMMENTS):
                insert_file.write("---------"+TableName+" ----------------------------------------------------------------------------------------\n")
                insert_file.write("---------------------------------------------------------------------------------------------------------------\n")
            for row in csv_reader:
                DictionaryKeys = csv_reader.fieldnames.copy()
                currentRow = []
                for index in range (0, len(DictionaryKeys)):
                    ColumnType.append("integer")
                    ByteLength.append(0)
                

                for index in range (0, len(DictionaryKeys)):
                    valueToBeAppended = row[DictionaryKeys.pop()]

                    if ColumnType[index] != "varchar":
                        if valueToBeAppended.isnumeric() and ColumnType[index] != "date":
                            ColumnType[index] = "integer"
                        else:
                            mightBeDate = valueToBeAppended.split("/")
                            print(valueToBeAppended+"We will split this value with / to see if it is a date")
                            print(mightBeDate)
                            Date = True
                            for substringIndex in (0,len(mightBeDate)-1):
                                if (Date != False):
                                    print("checking substring"+mightBeDate[substringIndex])
                                    Date = mightBeDate[substringIndex].isnumeric()
                            if (Date == True):
                                ColumnType[index] = "date"
                            else:
                                ColumnType[index] = "varchar"
                            
                        
                    if sys.getsizeof(valueToBeAppended) > ByteLength[index]:
                        ByteLength[index] = sys.getsizeof(valueToBeAppended)
                    currentRow.append(valueToBeAppended)

                DictionaryKeys = csv_reader.fieldnames.copy()
                #The following line gets rid of the UTF-8 encoding at the start of each file if you are exporting from microsoft excel 2016 or a similar program
                DictionaryKeys[0] = DictionaryKeys[0].replace("ï»¿","")
                
                Columns = (", ".join( repr(fieldname) for fieldname in DictionaryKeys)).replace("\'","")
                
                Tuple = (", ".join( repr(value) for value in currentRow)).replace("\'","")

                insert_file.write( "INSERT INTO " + TableName + " (" + Columns + ")" + " VALUES " + "(" + Tuple + ");\n" )
            if(COMMENTS):
                insert_file.write("---------------------------------------------------------------------------------------------------------------\n")
 
        with open(Create_SQL_URL, 'a') as create_file:
            TableName = os.path.splitext(os.path.basename(csv_file.name))[0]
            if(COMMENTS):
                create_file.write("---------"+TableName+" ----------------------------------------------------------------------------------------\n")
                create_file.write("---------------------------------------------------------------------------------------------------------------\n")
            create_file.write("CREATE TABLE "+ TableName +" (\n")
            Columns = DictionaryKeys.copy()
            for row in range(0,len(Columns)):
                if (ColumnType[row] == "varchar"):
                    Columns[row]+=(" varchar("+str(ByteLength[row])+"),")
                elif (ColumnType[row] == "integer"):
                    Columns[row]+=(" integer,")
                elif (ColumnType[row] == "date"):
                    Columns[row]+=(" date,")
                print(str(row) +"|"+ Columns[row])
            #is_primary_key_input = input("")
            #primary_key_indexes = input("")
            #is_foreign_key_input = input("")
            #foreign_key_indexes = input("")
            #add_not_null_input = input("")
            #not_null_indexes = input("")
            for row in range(0,len(Columns)):
                create_file.write("\t"+Columns[row]+"\n")

            create_file.write(");\n")
            if(COMMENTS):
                create_file.write("---------------------------------------------------------------------------------------------------------------\n")
           
            


            
            

