##################################################################
#----- BankManagementSystem.py                                   #
#----- Written by - Anirudha Basu Thakur                         #
#----- Class - XII                                               #
#----- Roll No - 1771199                                         #
#----- Registration ID # B/2/22/15674/0188                       #
##################################################################
import signal
import sys
import os
import os.path
import random
import datetime
import time
import csv
import MySQLdb

#KeyBoard Interrupt Error trap for especilly CTRL-C pressed
def sigint_handler(signal, frame):
    while(True): pass

#Clears Screen
def cls():
    os.system('cls')

#Replacing Single quote to double quote -'-> " & \
def FormatString(sVal):
    return sVal.replace("'", "''").replace("\\", "\\\\")

#Replacing double quote to single quote -"->' & \
def ReverseString(sVal):
    return sVal.replace("''", "'").replace("\\\\", "\\")

#Padding with number of spaces
def Pad(fLength, vLength):
    sSpace = " "*(fLength - vLength)
    return sSpace

#Printing messages with a format
def Message(sMsg):
    sMsg = "#" + (chr(ord("—"))*3) + " " + sMsg + " " + (chr(ord("—"))*3) + "#\n"
    print("\n"+ sMsg.center(len(sMsg) + (160 - len(sMsg)), " "))

#Validating correct Date
def isDate(sDate):
    odate = None
    isValidDate = 0
    dateformat = '%d/%m/%Y'
    try:
        curdate = datetime.date.today()
        odate = datetime.datetime.strptime(sDate, dateformat)
        if(odate.year <= 1900): isValidDate = -1 # Year cannot be less than 1900
        elif(odate.date() > curdate): isValidDate = -2 # Date cannot be greater than current Date
        elif(odate.date() == curdate): isValidDate = -3 # Date cannot be same as current Date
        else: isValidDate = 1 # valid date
    except ValueError:
        isValidDate = -4
    except Exception:
        isValidDate = -5
    finally:
        odate = None
    return isValidDate

#Reading MySQL DB Connection String CSV datafile
def getConnectionStringCSV():
    rowlist = None
    csv_file = None
    csv_reader = None
    try:
        if(os.path.isfile('BMS_MySQL_ConnectionString.csv') == True):
            with open(r'BMS_MySQL_ConnectionString.csv') as csv_file:
                csv_reader = csv.reader(csv_file, delimiter = ',')
                for row in csv_reader:
                    rowlist = row
            
            csv_file.close()
    except FileNotFoundError:
        Message("Error :: BMS_MySQL_ConnectionString.csv file not found......Cannot proceed")
    except Exception as e:
        Message(str(e))
    finally:
        if(csv_reader is not None): csv_reader = None
        if(csv_file is not None): csv_file = None
    return rowlist

#Creating MySQL DB Connection object
def getConnection():
    sLocalHost = ""
    sDatabase = ""
    sUser = ""
    sPWD = ""
    row_list = None
    connection = None
    try:
        row_list = getConnectionStringCSV()
        if(row_list is not None):
            sLocalHost = str(row_list[0])
            sDatabase = str(row_list[1])
            sUser = str(row_list[2])
            sPWD = str(row_list[3])
            connection = MySQLdb.connect(host = sLocalHost, database = sDatabase, user = sUser, password = sPWD)
            #connection = mysql.connector.connect(host = 'localhost', database = 'narDB', user = 'root', password = 'sasa')
    except Exception as e:
        Message(str(e))
    finally:
        row_list = None
    return connection

#Get data from MySQL Database tables
def getData(sSQL):
    connection = None
    cursor = None
    records = None
    try:
        connection = getConnection()
        if(connection is not None):
            if(connection.open ==  1):
                cursor = connection.cursor()
                cursor.execute(sSQL)
                records = cursor.fetchall()
    except Exception as e:
        Message(str(e))
    finally:
        if(connection is not None):
            if(connection.open ==  1):
                if(cursor is not None):
                    cursor.close()
                    cursor = None
                    
                connection.close()
                connection = None
    return records

#Insert, Update data in MySQL Database tables
def getInsertUpdateSQL(sSQL, oData = None):
    connection = None
    cursor = None
    iRowsAffected = 0
    try:
        connection = getConnection()
        if(connection is not None):
            if(connection.open ==  1):
                cursor = connection.cursor()
                
                if(oData is None):
                    cursor.execute(sSQL)
                else:
                    cursor.execute(sSQL, oData)
                
                connection.commit()
                cursor.fetchall()
                iRowsAffected = cursor.rowcount
    except Exception as e:
        connection.rollback()
        Message(str(e))
    finally:
        if(connection is not None):
            if(connection.open ==  1):
                if(cursor is not None):
                    cursor.close()
                    cursor = None

                connection.close()
                connection = None
    return iRowsAffected

#Randon Number generetion for Bank Account No.
#Generating randon number consisting of 12 digits
def getAccountNo():
    return random.SystemRandom().randint(100000000000, 999999999999)

#validate Name entered by user
def validateName(sName):
    try:
        if((len(sName) == 0) or (len(sName) > 30)):
            Message("Error :: Please Enter Account Holder Name[Max Length 30]")
            sName = validateName(FormatString(str(input("\t"*1 + "Enter Account Holder Name[Max Length 30]: ")).strip()))
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sName

#validate DOB entered by user
def validateDOB(sDOB):
    iDate = 0
    try:
        iDate = isDate(sDOB)
        if(iDate == -1):        
            Message("Error :: Account Holder DOB cannot be Less or Equal than 1900 year")
            sDOB = validateDOB(FormatString(str(input("\t"*1 + "Enter Account Holder DOB [DD/MM/YYYY]: ")).strip()))
        elif(iDate == -2):
            Message("Error :: Account Holder DOB cannot be greater than Current Date")
            sDOB = validateDOB(FormatString(str(input("\t"*1 + "Enter Account Holder DOB [DD/MM/YYYY]: ")).strip()))
        elif(iDate == -3):
            Message("Error :: Account Holder DOB cannot be same as Current Date")
            sDOB = validateDOB(FormatString(str(input("\t"*1 + "Enter Account Holder DOB [DD/MM/YYYY]: ")).strip()))
        elif(iDate == -4 or iDate == -5 or iDate == 0):
            Message("Error :: Please Enter Account Holder DOB in [DD/MM/YYYY] Format")
            sDOB = validateDOB(FormatString(str(input("\t"*1 + "Enter Account Holder DOB [DD/MM/YYYY]: ")).strip()))
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sDOB

#validate Address City State Country entered by user
def validate_ADDR_CITY_STATE_COUNTRY(sVal, sKey):
    try:
        if(sKey == "ADDR"):
            if((len(sVal) == 0) or (len(sVal) > 50)):
                Message("Error :: Please Enter Account Holder Address[Max Length 50]")
                sVal = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder Address[Max Length 50]: ")).strip()), "ADDR")
        elif(sKey == "CITY"):
            if((len(sVal) == 0) or (len(sVal) > 20)):
                Message("Error :: Please Enter Account Holder City[Max Length 20]")
                sVal = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder City[Max Length 20]: ")).strip()), "CITY")
        elif(sKey == "STATE"):
            if((len(sVal) == 0) or (len(sVal) > 20)):
                Message("Error :: Please Enter Account Holder State[Max Length 20]")
                sVal = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder State[Max Length 20]: ")).strip()), "STATE")
        elif(sKey == "COUNTRY"):
            if((len(sVal) == 0) or (len(sVal) > 20)):
                Message("Error :: Please Enter Account Holder Country[Max Length 20]")
                sVal = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder Country[Max Length 20]: ")).strip()), "COUNTRY")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sVal

#validate Phone entered by user
def validatePH(sPH):
    try:
        if(sPH.isnumeric() == False):
            Message("Error :: Account Holder Phone Number cannot be Alphabetic/AlphaNumeric or consists Wild Card Characters")
            sPH = validatePH(FormatString(str(input("\t"*1 + "Enter Account Holder Phone Number[10 Digit]: ")).strip()))
        elif((len(sPH) == 0) or (len(sPH) < 10) or (len(sPH) > 10)):
            Message("Error :: Please Enter Account Holder Phone Number[10 Digit]")
            sPH = validatePH(FormatString(str(input("\t"*1 + "Enter Account Holder Phone Number[10 Digit]: ")).strip()))
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sPH

#check Amount entered by user
def getCheckAmount(sAmount: str, iMode):
    try:
        if(sAmount.isnumeric() == False):
            Message("Error : Amount cannot be Alphabetic/AlphaNumeric or consists Wild Card Characters")
            Message("Please Enter Amount [with in 10 Digits and Decimals not allowed]")
            if(iMode == 1): sAmount = getCheckAmount(FormatString(str(input("\t"*8 + "Enter Deposit Amount : ")).strip()), 1)
            elif(iMode == 2): sAmount = getCheckAmount(FormatString(str(input("\t"*8 + "Enter Withdrawal Amount : ")).strip()), 2)
        elif(len(sAmount) > 10):
            Message("Error : Please Enter Amount [with in 10 Digits and Decimals not allowed]")
            if(iMode == 1): sAmount = getCheckAmount(FormatString(str(input("\t"*8 + "Enter Deposit Amount : ")).strip()), 1)
            elif(iMode == 2): sAmount = getCheckAmount(FormatString(str(input("\t"*8 + "Enter Withdrawal Amount : ")).strip()), 2)
        elif(int(sAmount) == 0):
            Message("Error : Amount Cannot be 0")
            if(iMode == 1): sAmount = getCheckAmount(FormatString(str(input("\t"*8 + "Enter Deposit Amount : ")).strip()), 1)
            elif(iMode == 2): sAmount = getCheckAmount(FormatString(str(input("\t"*8 + "Enter Withdrawal Amount : ")).strip()), 2)
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sAmount

#Check Duplicate Account No.
def getCheckDuplicateAccount(sENQID):
    sSQL = ""
    iDupID = 0
    records = None
    try:
        sSQL = "SELECT ACCOUNT_ID FROM narDB.BMS_MASTER WHERE ACCOUNT_ID = '" + sENQID + "';"
        records = getData(sSQL)
        if(len(records) > 0): iDupID = len(records)
    except Exception as e:
        Message(str(e))
    finally:
        if(records is not None): records = None
    return iDupID

#Validate Active Account
def getActiveAccount(sENQID):
    sSQL = ""
    iActive = 0
    records = None
    try:
        sSQL = "SELECT ACCOUNT_ACTIVE FROM narDB.BMS_MASTER WHERE ACCOUNT_ID = '" + sENQID + "';"
        records = getData(sSQL)
        if(len(records) == 0): iActive = -1
        else:
            for row in records:
                iActive = int(row[0])
    except Exception as e:
        Message(str(e))
    finally:
        if(records is not None): records = None
    return iActive

#Check Account Balance
def getCheckBalance(sENQID):
    iCr = 0
    iDr = 0
    iBalance = 0
    records = None
    sSQL = ""
    try:
        if(sENQID != ""):
            sSQL = "SELECT B.ACCOUNT_ID, B.AMOUNT_CR, B.AMOUNT_DR "
            sSQL += "FROM narDB.BMS_ACCOUNTS B "
            sSQL += "LEFT OUTER JOIN narDB.BMS_MASTER A "
            sSQL += "ON B.ACCOUNT_ID = A.ACCOUNT_ID "
            sSQL += "WHERE A.ACCOUNT_ID = '" + sENQID + "'; "
            records = getData(sSQL)
            if(len(records) > 0):
                for row in records:
                    iCr += row[1] #AMOUNT_CR
                    iDr += row[2] #AMOUNT_DR
                    
                if(iCr == 0): iBalance = -1
                elif(iDr > iCr): iBalance = -1
                else: iBalance = (iCr - iDr)
            else: iBalance = 0
    except Exception as e:
        Message(str(e))
    finally:
        if(records is not None): records = None
    return iBalance

# Modify Account Details - Caller function - getColumn(sCol)
def getUpateColumn(sCol):
    sACCN_HLD_NAME = ""
    sACCN_HLD_DOB = ""
    sACCN_HLD_ADDR = ""
    sACCN_HLD_CITY = ""
    sACCN_HLD_STATE = ""
    sACCN_HLD_COUNTRY = ""
    sACCN_HLD_PH = ""
    sSQL = ""
    try:
        if(sCol == "NAME"):
            sACCN_HLD_NAME = validateName(FormatString(str(input("\t"*1 + "Enter Account Holder Name[Max Length 30]: ")).strip()))
            if(sACCN_HLD_NAME != ""):
                sSQL = "ACCOUNT_HOLDER_NAME = TRIM('" + sACCN_HLD_NAME + "')"
        elif(sCol == "DOB"):
            sACCN_HLD_DOB = validateDOB(FormatString(str(input("\t"*1 + "Enter Account Holder DOB [DD/MM/YYYY]: ")).strip()))
            if(sACCN_HLD_DOB != ""):
                sSQL = "ACCOUNT_HOLDER_DOB = STR_TO_DATE(TRIM('" + sACCN_HLD_DOB + "'),'%d/%m/%Y')"
        elif(sCol == "ADDR"):
            sACCN_HLD_ADDR = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder Address[Max Length 50]: ")).strip()), "ADDR")
            if(sACCN_HLD_ADDR != ""):
                sSQL = "ACCOUNT_HOLDER_ADDR = TRIM('" + sACCN_HLD_ADDR + "')"
        elif(sCol == "CITY"):
            sACCN_HLD_CITY = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder City[Max Length 20]: ")).strip()), "CITY")
            if(sACCN_HLD_CITY != ""):
                sSQL = "ACCOUNT_HOLDER_CITY = TRIM('" + sACCN_HLD_CITY + "')"
        elif(sCol == "STATE"):
            sACCN_HLD_STATE = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder State[Max Length 20]: ")).strip()), "STATE")
            if(sACCN_HLD_STATE != ""):
                sSQL = "ACCOUNT_HOLDER_STATE = TRIM('" + sACCN_HLD_STATE + "')"
        elif(sCol == "COUNTRY"):
            sACCN_HLD_COUNTRY = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder Country[Max Length 20]: ")).strip()), "COUNTRY")
            if(sACCN_HLD_COUNTRY != ""):
                sSQL = "ACCOUNT_HOLDER_COUNTRY = TRIM('" + sACCN_HLD_COUNTRY + "')"
        elif(sCol == "PH"):
            sACCN_HLD_PH = validatePH(FormatString(str(input("\t"*1 + "Enter Account Holder Phone Number[10 Digit]: ")).strip()))
            if(sACCN_HLD_PH != ""):
                sSQL = "ACCOUNT_HOLDER_PH = TRIM('" + sACCN_HLD_PH + "')"
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sSQL

# Modify Account Details - Caller function - getModifyAccount()
def getColumn(sCol):
    sCmd = ""
    sSQL = ""
    try:
        if(sCol == "NAME"):
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder Name [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("NAME")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("NAME")
        elif(sCol == "DOB"):
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder DOB [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("DOB")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("DOB")
        elif(sCol == "ADDR"): 
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder Address [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("ADDR")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("ADDR")
        elif(sCol == "CITY"): 
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder City [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("CITY")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("CITY")
        elif(sCol == "STATE"): 
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder State [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("STATE")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("STATE")
        elif(sCol == "COUNTRY"): 
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder Country [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("COUNTRY")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("COUNTRY")
        elif(sCol == "PH"):
            sCmd = str(input("\t"*1 + "Do you want to modify Account Holder Phone Number [Y/N] : ")).upper().strip()
            if(sCmd == "Y"): sSQL += getUpateColumn("PH")
            elif(sCmd == "N"): pass
            else:
                Message("Error :: Invalid Input"),
                sSQL += getColumn("PH")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    return sSQL

#Menu Functions
#Menu option 1 - Open New Account
def getOpenAccount():
    iRowsAffected = 0
    sACCN_HLD_NAME = ""
    sACCN_HLD_DOB = ""
    sACCN_HLD_ADDR = ""
    sACCN_HLD_CITY = ""
    sACCN_HLD_STATE = ""
    sACCN_HLD_COUNTRY = ""
    sACCN_HLD_PH = ""
    sAccountNo = ""
    sCmd = ""
    sSQL = ""
    try:
        print("\t"*1 + chr(ord("—"))*139)
        print("\t"*1 + "Open New Account #")
        print("\t"*1 + chr(ord("—"))*139)
        
        sACCN_HLD_NAME = validateName(FormatString(str(input("\t"*1 + "Enter Account Holder Name[Max Length 30]: ")).strip()))
        sACCN_HLD_DOB = validateDOB(FormatString(str(input("\t"*1 + "Enter Account Holder DOB [DD/MM/YYYY]: ")).strip()))
        sACCN_HLD_ADDR = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder Address[Max Length 50]: ")).strip()), "ADDR")
        sACCN_HLD_CITY = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder City[Max Length 20]: ")).strip()), "CITY")
        sACCN_HLD_STATE = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder State[Max Length 20]: ")).strip()), "STATE")
        sACCN_HLD_COUNTRY = validate_ADDR_CITY_STATE_COUNTRY(FormatString(str(input("\t"*1 + "Enter Account Holder Country[Max Length 20]: ")).strip()), "COUNTRY")
        sACCN_HLD_PH = validatePH(FormatString(str(input("\t"*1 + "Enter Account Holder Phone Number[10 Digit]: ")).strip()))
        
        #if(sACCN_HLD_NAME != "" and sACCN_HLD_DOB != "" and sACCN_HLD_ADDR != "" and sACCN_HLD_CITY != ""
        #                           and sACCN_HLD_STATE != "" and sACCN_HLD_COUNTRY != "" and sACCN_HLD_PH != ""):
        sSQL = "INSERT INTO narDB.BMS_MASTER(ACCOUNT_ID, ACCOUNT_HOLDER_NAME, ACCOUNT_HOLDER_DOB, "
        sSQL += "ACCOUNT_HOLDER_ADDR, ACCOUNT_HOLDER_CITY, ACCOUNT_HOLDER_STATE, ACCOUNT_HOLDER_COUNTRY, "
        sSQL += "ACCOUNT_HOLDER_PH) VALUES (%s, %s, %s, %s, %s, %s, %s, %s); "
            
        sAccountNo = str(getAccountNo())
        if(getCheckDuplicateAccount(sAccountNo) != 0) : sAccountNo = str(getAccountNo())
        
        date,month,year = sACCN_HLD_DOB.split("/")
        DOB = datetime.datetime(int(year), int(month), int(date))
                    
        data = (sAccountNo, sACCN_HLD_NAME, DOB, sACCN_HLD_ADDR,sACCN_HLD_CITY, sACCN_HLD_STATE, sACCN_HLD_COUNTRY, sACCN_HLD_PH)
        iRowsAffected = getInsertUpdateSQL(sSQL, data)
        if(iRowsAffected > 0):
            Message("New Account Created Successfully")
            getAccountsList(sAccountNo)
            sCmd = FormatString(str(input("\t"*7 + "Do You Want To Open More Account? [Y/N] : "))).upper().strip()
            if(sCmd == "Y"): getOpenAccount()
            elif(sCmd == "N"): cls(), main()
            else: Message("Error :: Invalid Input"), cls(), main()
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
        
#Menu option 2 - Modify Account
def getModifyAccount():
    iActive = 0
    iRowsAffected = 0
    sENQID = ""
    sCmd = ""
    mSQL_NAME = ""
    mSQL_DOB = ""
    mSQL_ADDR = ""
    mSQL_CITY = ""
    mSQL_STATE = ""
    mSQL_COUNTRY = ""
    mSQL_PH = ""
    bUpdate = False
    try:
        print("\t"*5 + chr(ord("—"))*79)
        print("\t"*5 + "Modify Account #")
        print("\t"*5 + chr(ord("—"))*79)
        
        sENQID = FormatString(str(input("\t"*8 + "Enter Account No. : ")).strip())
        if(sENQID != ""):
            iActive = getActiveAccount(sENQID)
            if(iActive == -1) : Message("No Records found")
            elif(iActive == 0): Message("This " + sENQID + " Account is already Closed")
            else:
                getAccountsList(sENQID)
                sCmd = str(input("\t"*7 + "Do you want to modify this Account[Y/N] : ")).upper().strip()
                if(sCmd == "Y"):
                    sSQL = "UPDATE narDB.BMS_MASTER SET "
                    mSQL_NAME = getColumn("NAME")
                    if(mSQL_NAME != ""):
                        sSQL += mSQL_NAME
                        bUpdate = True
                    
                    mSQL_DOB = getColumn("DOB")
                    if(mSQL_DOB != ""):
                        if(mSQL_NAME != ""): sSQL += ", "
                        sSQL += mSQL_DOB
                        bUpdate = True
                    
                    mSQL_ADDR = getColumn("ADDR")
                    if(mSQL_ADDR != ""):
                        if((mSQL_NAME != "") or (mSQL_DOB != "")): sSQL += ", "
                        sSQL += mSQL_ADDR
                        bUpdate = True
                    
                    mSQL_CITY = getColumn("CITY")
                    if(mSQL_CITY != ""):
                        if((mSQL_NAME != "") or (mSQL_DOB != "") or (mSQL_ADDR != "")): sSQL += ", "
                        sSQL += mSQL_CITY
                        bUpdate = True
                    
                    mSQL_STATE = getColumn("STATE")
                    if(mSQL_STATE != ""):
                        if((mSQL_NAME != "") or (mSQL_DOB != "") or (mSQL_ADDR != "") or (mSQL_CITY != "")): sSQL += ", "
                        sSQL += mSQL_STATE
                        bUpdate = True
                    
                    mSQL_COUNTRY = getColumn("COUNTRY")
                    if(mSQL_COUNTRY != ""):
                        if((mSQL_NAME != "") or (mSQL_DOB != "") or (mSQL_ADDR != "") or (mSQL_CITY != "") or (mSQL_STATE != "")): sSQL += ", "
                        sSQL += mSQL_COUNTRY
                        bUpdate = True
                    
                    mSQL_PH = getColumn("PH")
                    if(mSQL_PH != ""):
                        if((mSQL_NAME != "") or (mSQL_DOB != "") or (mSQL_ADDR != "") or (mSQL_CITY != "") or (mSQL_STATE != "") or (mSQL_COUNTRY != "")): sSQL += ", "
                        sSQL += mSQL_PH
                        bUpdate = True
                    
                    sSQL += " WHERE ACCOUNT_ID = '" + sENQID + "'; "
                    if(bUpdate == True):
                        iRowsAffected = getInsertUpdateSQL(sSQL)
                        if(iRowsAffected > 0): Message("Account Modified Successfully"), getAccountsList(sENQID)
                    else:
                        Message("Nothing Entered to Update the Same")
                elif(sCmd == "N"): cls(), main()
                else: Message("Error :: Invalid Input"), cls(), main()
        else:
            Message("Account No. not entered")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
        
#Menu option 3 - Deposit Amount
def getDepositAmt():
    iActive = 0
    iRowsAffected = 0
    iDepositAmt = 0
    sSQL = ""
    sENQID = ""
    try:
        print("\t"*5 + chr(ord("—"))*79)
        print("\t"*5 + "Deposit Amount #")
        print("\t"*5 + chr(ord("—"))*79)
        
        sENQID = FormatString(str(input("\t"*8 + "Enter Account No. : ")).strip())
        if(sENQID != ""):
            iActive = getActiveAccount(sENQID)
            if(iActive == -1) : Message("No Records found")
            elif(iActive == 0): Message("This " + sENQID + " Account is already Closed")
            else:
                iDepositAmt = int(getCheckAmount(FormatString(str(input("\t"*8 + "Enter Deposit Amount : ")).strip()), 1))
                sSQL = "INSERT INTO narDB.BMS_ACCOUNTS(ACCOUNT_ID, TRAN_DT, AMOUNT_CR) VALUES (%s,%s,%s); "
                tranDt = datetime.datetime.now()
                data = (sENQID, tranDt,iDepositAmt)
                iRowsAffected = getInsertUpdateSQL(sSQL, data)
                if(iRowsAffected > 0): Message("Amount Deposited Successfully")
        else:
            Message("Account No. not entered")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
        
#Menu option 4 - Withdraw Amount
def getWithdrawAmt():
    iActive = 0
    iBalance = 0
    iWithdrawalAmt = 0
    iRowsAffected = 0
    sSQL = ""
    sENQID = ""
    try:
        print("\t"*5 + chr(ord("—"))*79)
        print("\t"*5 + "Withdraw Amount #")
        print("\t"*5 + chr(ord("—"))*79)
        sENQID = FormatString(str(input("\t"*8 + "Enter Account No. : ")).strip())
        if(sENQID != ""):
            iActive = getActiveAccount(sENQID)
            if(iActive == -1) : Message("No Records found")
            elif(iActive == 0): Message("This " + sENQID + " Account is already Closed")
            else:
                iWithdrawalAmt = int(getCheckAmount(FormatString(str(input("\t"*8 + "Enter Withdrawal Amount : ")).strip()), 2))
                iBalance = getCheckBalance(sENQID)
                if(iBalance != -1 and (iBalance >= iWithdrawalAmt)):
                    sSQL = "INSERT INTO narDB.BMS_ACCOUNTS(ACCOUNT_ID, TRAN_DT, AMOUNT_DR) VALUES (%s, %s, %s); "
                    tranDt = datetime.datetime.now()
                    data = (sENQID, tranDt, iWithdrawalAmt)
                    iRowsAffected = getInsertUpdateSQL(sSQL, data)
                    if(iRowsAffected > 0): Message("Amount Withdrawn Successfully")
                elif(iWithdrawalAmt > iBalance): Message("This " + sENQID + " Account does not have enough balance")
        else:
            Message("Account No. not entered")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
        
#Menu option 5 - Account Balance Enquiry
def getAccBalance():
    iCr = 0
    iDr = 0
    iBalance = 0
    sSQL = ""
    sENQID = ""
    sHeader = ""
    subHeader = ""
    records = None
    try:
        sENQID = FormatString(str(input("\t"*8 + "Enter Account No. : ")).strip())
        if(sENQID != ""):
            sSQL =  "SELECT A.ACCOUNT_ID, A.ACCOUNT_HOLDER_NAME, "
            sSQL += "DATE_FORMAT(B.TRAN_DT, '%d/%c/%Y %h:%i:%s %p') AS TRAN_DT, "
            sSQL += "B.AMOUNT_CR, B.AMOUNT_DR, A.ACCOUNT_ACTIVE "
            sSQL += "FROM narDB.BMS_MASTER A "
            sSQL += "LEFT OUTER JOIN narDB.BMS_ACCOUNTS B "
            sSQL += "ON A.ACCOUNT_ID = B.ACCOUNT_ID "
            sSQL += "WHERE B.ACCOUNT_ID = '" + sENQID + "'; "
            records = getData(sSQL)
            if(len(records) == 0) : Message("No Records Found")
            else:
                subHeader = "Transacton Date" + Pad(25, 0) + "Deposit(Cr.)" + Pad(12, 0) + "Withdrawal(Dr.)"
                print("\t"*5 + chr(ord("—"))*len(subHeader))
                print("\t"*5 + "Balance Enquiry #")
                for row in records:
                    sHeader = "Name : " + ReverseString(str(row[1])) + "\n"
                    sHeader += "\t"*5 + "Account No. : " + str(row[0])
                    sHeader += Pad(50, len(str(row[0]))) + "Status : "
                    if(int(row[5]) == 1): sHeader += "Active"
                    elif(int(row[5]) == 0): sHeader += "Closed"
                
                print("\t"*5 + chr(ord("—"))*len(subHeader))
                print("\t"*5 + sHeader)
                
                print("\t"*5 + chr(ord("—"))*len(subHeader))
                print("\t"*5 + subHeader)
                print("\t"*5 + chr(ord("—"))*len(subHeader))
                
                for row in records:
                    sLine = str(row[2]) + Pad(30, len(str(row[3]))) + str(row[3]) + Pad(27, len(str(row[4]))) + str(row[4])
                    iCr += row[3]
                    iDr += row[4]
                    iBalance = (iCr - iDr)
                    print("\t"*5 + sLine)
                
                print("\t"*5 + chr(ord("—"))*len(subHeader))
                print("\t"*5 + Pad(61, len(str(iBalance))) + "Account Balance : " + str(iBalance))
                print("\t"*5 + chr(ord("—"))*len(subHeader))
        else:
            Message("Account No. not entered")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    finally:
        if(records is not None): records = None

#Menu Option 6 - Customer Details
def getAccountDetails():
    sENQID = ""
    sSQL = ""
    sLine = ""
    sNAME = ""
    sDOB = ""
    sADDR = ""
    sCITY = ""
    sSTATE = ""
    sCOUNTRY = ""
    sPH = ""
    iCr = 0
    iDr = 0
    iBalance = 0
    ACrecs = None
    AmtRecs = None
    try:
        sENQID = FormatString(str(input("\t"*8 + "Enter Account No. : ")).strip())
        if(sENQID != ""):
            sSQL = "SELECT ACCOUNT_ID, ACCOUNT_HOLDER_NAME, ACCOUNT_HOLDER_DOB, ACCOUNT_HOLDER_ADDR,"
            sSQL += "ACCOUNT_HOLDER_CITY, ACCOUNT_HOLDER_STATE, ACCOUNT_HOLDER_COUNTRY, ACCOUNT_HOLDER_PH, ACCOUNT_ACTIVE "
            sSQL += "FROM narDB.BMS_MASTER "
            sSQL += "WHERE ACCOUNT_ID = '" + sENQID + "'; "
            ACrecs = getData(sSQL)
            if(len(ACrecs) == 0) : Message("No Records found")
            else:
                sSQL = "SELECT ACCOUNT_ID, AMOUNT_CR, AMOUNT_DR FROM narDB.BMS_ACCOUNTS WHERE ACCOUNT_ID = '" + sENQID + "'; "
                AmtRecs = getData(sSQL)
                for Arows in AmtRecs:
                    iCr += Arows[1]
                    iDr += Arows[2]
                iBalance = (iCr - iDr)
                
                print("\t"*5 + chr(ord("—"))*79)
                print("\t"*5 + "Customer Details #")
                print("\t"*5 + chr(ord("—"))*79)
                
                for row in ACrecs:
                    sNAME = ReverseString(str(row[1])) #Name
                    sDOB = row[2].strftime("%d/%m/%Y")#DOB
                    sADDR = ReverseString(str(row[3]))#Address
                    sCITY = ReverseString(str(row[4]))#City
                    sSTATE = ReverseString(str(row[5]))#State
                    sCOUNTRY = ReverseString(str(row[6]))#Country
                    sPH = str(row[7])#Phone
                    
                    sLine = "\t"*5 + "Account No." + Pad(5, 0) + ": " + str(row[0])#Account No.

                    if(int(row[8]) == 1): sLine += "\t"*5 + "Status : Active" + "\n"
                    else: sLine += "\t"*5 + "Status : Closed" + "\n"
                    
                    sLine += "\t"*5 + "Name" + Pad(12, 0) + ": " + sNAME + "\n"
                    sLine += "\t"*5 + "DOB" + Pad(13, 0) + ": " + sDOB + "\n"
                    sLine += "\t"*5 + "Address" + Pad(9, 0) + ": " + sADDR + "\n"
                    sLine += "\t"*5 + "City" + Pad(12, 0) + ": " + sCITY + "\n"
                    sLine += "\t"*5 + "State" + Pad(11, 0) + ": " + sSTATE + "\n"
                    sLine += "\t"*5 + "Country" + Pad(9, 0) + ": " + sCOUNTRY + "\n"
                    sLine += "\t"*5 + "Phone" + Pad(11, 0) + ": " + sPH + "\n"
                    sLine += "\t"*5 + "Account Balance : " + str(iBalance) + "\n"
                    print(sLine)
                print("\t"*5 + chr(ord("—"))*79)
        else:
            Message("Account No. not entered")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
    finally:
        if(ACrecs is not None): ACrecs = None
        if(AmtRecs is not None): AmtRecs = None

#Menu option 7 - Account Holder List
def getAccountsList(sENQID, sCond = ""):
    sSQL = ""
    sHeader = ""
    sLine = ""
    sNAME = ""
    sDOB = ""
    sADDR = ""
    sCITY = ""
    sSTATE = ""
    sCOUNTRY = ""
    sPH = ""
    records = None
    try:
        sSQL = "SELECT ACCOUNT_ID, ACCOUNT_HOLDER_NAME, ACCOUNT_HOLDER_DOB, ACCOUNT_HOLDER_ADDR,"
        sSQL += "ACCOUNT_HOLDER_CITY, ACCOUNT_HOLDER_STATE, ACCOUNT_HOLDER_COUNTRY, ACCOUNT_HOLDER_PH, ACCOUNT_ACTIVE "
        sSQL += "FROM narDB.BMS_MASTER "
        if(sENQID != ""):
            sSQL += "WHERE ACCOUNT_ID = '" + sENQID + "'"
        sSQL += "ORDER BY ACCOUNT_HOLDER_NAME; "
        
        records = getData(sSQL)
        if(len(records) == 0): Message("No Records found")
        else:
            sHeader = "Account No." + Pad(3, 0) + "Name"
            sHeader += Pad(25, 0) + "DOB" + Pad(9, 0) + "Address" + Pad(23, 0) + "City"
            sHeader += Pad(8, 0) + "State" + Pad(12, 0) + "Country" + Pad(10, 0) + "Phone" + Pad(8, 0) + "Status"
            
            print("\t"*1 + chr(ord("—"))*len(sHeader))
            if(sCond == ""):
                print("\t"*1 + "Account Holder List #")
            else:
                print("\t"*1 + "Account Holder List #" + Pad(129, 26) + " Total No. of Records : " + str(len(records)))
            
            print("\t"*1 + chr(ord("—"))*len(sHeader))
            print("\t"*1 + sHeader)
            print("\t"*1 + chr(ord("—"))*len(sHeader))
                
            for row in records:
                sLine = str(row[0]) #Account No.
                sNAME = ReverseString(str(row[1])) #Name
                sLine += Pad(14, len(row[0])) + sNAME
                
                sDOB = row[2].strftime("%d/%m/%Y")#DOB
                sADDR = ReverseString(str(row[3]))#Address
                sCITY = ReverseString(str(row[4]))#City
                sSTATE = ReverseString(str(row[5]))#State
                sCOUNTRY = ReverseString(str(row[6]))#Country
                sPH = str(row[7])#Phone
                    
                sLine += Pad(29, len(sNAME)) + sDOB
                sLine += Pad(12, len(sDOB)) + sADDR
                sLine += Pad(30, len(sADDR)) + sCITY
                sLine += Pad(12, len(sCITY)) + sSTATE
                sLine += Pad(17, len(sSTATE)) + sCOUNTRY
                sLine += Pad(17, len(sCOUNTRY)) + sPH
                sLine += Pad(12, len(sPH))
                
                if(int(row[8]) == 1): sLine += " Active" #Status
                else: sLine += " Closed"
                print("\t"*1 + sLine)
                
        print("\t"*1 + chr(ord("—"))*len(sHeader))
    except Exception as e:
        Message(str(e))
    finally:
        if(records is not None): records = None

#Menu option 8 - Close Account
def getCloseAccount():
    iActive = 0
    iRowsAffected = 0
    sSQL = ""
    sCmd = ""
    sENQID = ""
    try:
        print("\t"*5 + chr(ord("—"))*79)
        print("\t"*5 + "Close An Account #")
        print("\t"*5 + chr(ord("—"))*79)
        sENQID = FormatString(str(input("\t"*8 + "Enter Account No. : ")).strip())
        if(sENQID != ""):
            iActive = getActiveAccount(sENQID)
            if(iActive == -1) : Message("No Records found")
            elif(iActive == 0): Message("This " + sENQID + " Account is already Closed")
            else:
                getAccountsList(sENQID)
                sCmd = str(input("\t"*7 + "Do you want to close this Account[Y/N] : ")).upper().strip()
                if(sCmd == "Y"):
                    sSQL = "UPDATE narDB.BMS_MASTER SET ACCOUNT_ACTIVE = 0 WHERE ACCOUNT_ID = '" + sENQID + "'; "
                    iRowsAffected = getInsertUpdateSQL(sSQL)
                    if(iRowsAffected > 0): Message("Account Closeure Done"), getAccountsList(sENQID)
                elif(sCmd == "N"): cls(), main()
                else: Message("Error :: Invalid Input"), cls(), main()
        else:
            Message("Account No. not entered")
    except Exception as e:
        if(str(e) != ""): Message(str(e))
        else: Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
        
#Return to Menu Function
def getReturnToMainMenu():
    ch = input("\t"*7 + "   Press 0 To Go Back To Main Menu: ").strip()
    if(ch.isnumeric() == True):
        ch = int(ch)
        if(ch == 0): cls(), main()
        else: getReturnToMainMenu()
    else: getReturnToMainMenu()
    
#Menu Function
def main():
    ch = None
    try:
        print("\t"*5 + chr(ord("—"))*79)
        print("\t"*8 + " BANK MANAGEMENT SYSTEM")
        print("\t"*8 + " "*6 + "Written By ")
        print("\t"*6 + " Anirudha Basu Thakur - Class XII - Roll No.- 1771199 ")
        print("\t"*6 + " Anamitra Mondal      - Class XII - Roll No.- 1765581 ")
        print("\t"*6 + " Aaditya Verma        - Class XII - Roll No.- 1787072 ")
        print("\t"*5 + chr(ord("—"))*79)
        print("\t"*5 + " "*6 + "Developed using Python 3.10.0/MySQL 8.0/MySQLClient 2.1.0 ")
        print("\t"*5 + chr(ord("—"))*79)
        
        if(os.path.isfile('BMS_MySQL_ConnectionString.csv') == True):
            print("\t"*8 + "1. OPEN NEW ACCOUNT: ")
            print("\t"*8 + "2. MODIFY AN ACCOUNT: ")
            print("\t"*8 + "3. DEPOSIT AMOUNT: ")
            print("\t"*8 + "4. WITHDRAW AMOUNT: ")
            print("\t"*8 + "5. BALANCE ENQUIRY: ")
            print("\t"*8 + "6. DISPLAY CUSTOMER DETAILS: ")
            print("\t"*8 + "7. DISPLAY ACCOUNT HOLDER LIST: ")
            print("\t"*8 + "8. CLOSE AN ACCOUNT: ")
            print("\t"*8 + "9. EXIT: ")
                
            print("\t"*5 + chr(ord("—"))*79)
            ch = input("\t"*8 + "Enter your choice [1-9] : ").strip()
            if(ch.isnumeric() == True):
                ch = int(ch)
                if ch == 1: getOpenAccount()
                elif ch == 2: getModifyAccount()
                elif ch == 3: getDepositAmt()
                elif ch == 4: getWithdrawAmt()
                elif ch == 5: getAccBalance()
                elif ch == 6 : getAccountDetails()
                elif ch == 7 : getAccountsList("", "LIST")
                elif ch == 8: getCloseAccount()
                elif ch == 9:
                    sys.exit(0)
                    
                getReturnToMainMenu()
            else: cls(), main()
        else:
            Message("Error :: BMS_MySQL_ConnectionString.csv file not found......Cannot proceed")
            input("\t"*8 + "Press any key to continue......")
    except FileNotFoundError:
        Message("Error :: BMS_MySQL_ConnectionString.csv file not found......Cannot proceed")
        input("\t"*8 + "Press any key to continue......")
    except TypeError:
        #Message(str(e))
        input("\t"*8 + "Press any key to continue......")
    except KeyboardInterrupt:
        Message("KeyBoard Interruption Error Occured")
        signal.signal(signal.SIGINT, sigint_handler) #CTRL+Z=SIGTSTOP CTRL+D+CTRL/ = SIGQUIT
    except EOFError:
        input("\t"*8 + "Press any key to continue......")
    except Exception as e:
        if(str(e) != ""):
            Message(str(e))
        else:
            Message("KeyBoard Interruption Error Occured") #Assumping user pressed CTRL+Z//CTRL+D//CTRL+/
        input("\t"*8 + "Press any key to continue......")
    finally:
        ch = None
main()
