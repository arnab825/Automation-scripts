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
    
#Create CSV data file for MySQL DB Connection String
def CreateConnectionStringCSV(sLocalHost, sDatabase, sUser, sPWD):
    rowlist = None
    csv_file = None
    try:
        rowlist = [[sLocalHost, sDatabase, sUser, sPWD]]
        if(os.path.isfile('BMS_MySQL_ConnectionString.csv') == True):
            os.remove('BMS_MySQL_ConnectionString.csv')
        
        with open('BMS_MySQL_ConnectionString.csv', 'w', newline = '') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerows(rowlist)

        csv_file.close()
    except Exception as e:
        print(str(e))
    finally:
        rowlist = None
        if(csv_file is not None): csv_file = None

#Read CSV data file for MySQL DB Connection String
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
        print("Error :: BMS_MySQL_ConnectionString.csv file not found......Cannot proceed !")
    except Exception as e:
        print(str(e))
    finally:
        if(csv_reader is not None): csv_reader = None
        if(csv_file is not None): csv_file = None
    return rowlist

#Creating MySQl Connection object
def getConnection(bCon):
    sLocalHost = ""
    sDatabase = ""
    sUser = ""
    sPWD = ""
    row_list = None
    connection = None
    try:
        if(bCon == 0):
            sLocalHost = str(input("Enter Local Server Name[i.e. localhost] : ")).replace("'", "").replace("\\", "")
            sDatabase = str(input("Enter Database Name[i.e. - sys] : ")).replace("'", "").replace("\\", "")
            sUser = str(input("Enter UserName[i.e. root] : ")).replace("'", "").replace("\\", "")
            sPWD = str(input("Enter Password : ")).replace("'", "").replace("\\", "")
            #connection = mysql.connector.connect(host = 'localhost', database = 'sys', user = 'root', password = 'sasa')
            connection = MySQLdb.connect(host = sLocalHost, database = sDatabase, user = sUser, password = sPWD)
            if(connection.open == 1):
                CreateConnectionStringCSV(sLocalHost, "narDB", sUser, sPWD)
        else:
            row_list = getConnectionStringCSV()
            sLocalHost = str(row_list[0])
            sDatabase = str(row_list[1])
            sUser = str(row_list[2])
            sPWD = str(row_list[3])
            #connection = mysql.connector.connect(host = 'localhost', database = 'narDB', user = 'root', password = 'sasa')
            connection = MySQLdb.connect(host = sLocalHost, database = sDatabase, user = sUser, password = sPWD)
    except Exception as e:
        print(str(e))
    finally:
        row_list = None
    return connection

#Create Application Database - narDB
def CreateDB():
    sSQL = ""
    connection = None
    cursor = None
    try:
        print("\n")
        print("Preparing to create Database......\n")
        connection = getConnection(0)
        if(connection is not None):
            if(connection.open == 1):
                cursor = connection.cursor()
                sSQL = "DROP DATABASE IF EXISTS `NARDB`;"
                cursor.execute(sSQL)
               
                sSQL = ""
                sSQL = "CREATE DATABASE `NARDB`;"
                cursor.execute(sSQL)
                print("\n")
                print("Application Database Created -- narDB\n")
    except Exception as e:
        print(str(e))
    finally:
        if(connection is not None):
            if(connection.open == 1):
                if(cursor is not None):
                    cursor.close()
                    cursor = None

                connection.close()
                connection = None

#Create Application Database Tables - Accounts & Amount
def CreateTable():
    sSQL = ""
    connection = None
    cursor = None
    try:
        print("Preparing to create Database Tables......\n")
        connection = getConnection(1)
        if(connection is not None):
            if(connection.open == 1):
                cursor = connection.cursor()
                
                sSQL = "DROP TABLE IF EXISTS narDB.BMS_MASTER;"
                cursor.execute(sSQL)
                
                sSQL = ""
                sSQL += "CREATE TABLE narDB.`BMS_MASTER` ( "
                sSQL += "`ACCOUNT_ID` varchar(15) NOT NULL, "
                sSQL += "`ACCOUNT_HOLDER_NAME` varchar(30) DEFAULT NULL, "
                sSQL += "`ACCOUNT_HOLDER_DOB` datetime DEFAULT NULL, "
                sSQL += "`ACCOUNT_HOLDER_ADDR` varchar(50) DEFAULT NULL, "
                sSQL += "`ACCOUNT_HOLDER_CITY` varchar(20) DEFAULT NULL, "
                sSQL += "`ACCOUNT_HOLDER_STATE` varchar(20) DEFAULT NULL, "
                sSQL += "`ACCOUNT_HOLDER_COUNTRY` varchar(20) DEFAULT NULL, "
                sSQL += "`ACCOUNT_HOLDER_PH` varchar(10) DEFAULT NULL, "
                sSQL += "`ACCOUNT_ACTIVE` int(11) DEFAULT '1', "
                sSQL += "PRIMARY KEY (`ACCOUNT_ID`) "
                sSQL += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; "
                
                cursor.execute(sSQL)
                print("Master Table Created......\n")
                
                sSQL = ""
                sSQL = "DROP TABLE IF EXISTS narDB.BMS_ACCOUNTS;"
                cursor.execute(sSQL)
               
                sSQL = ""
                sSQL += "CREATE TABLE narDB.`BMS_ACCOUNTS` ( "
                sSQL += "`ACCOUNT_ID` varchar(15) DEFAULT NULL, "
                sSQL += "`TRAN_DT` datetime DEFAULT NULL, "
                sSQL += "`AMOUNT_CR` bigint DEFAULT '0', "
                sSQL += "`AMOUNT_DR` bigint DEFAULT '0', "
                sSQL += "KEY `FK_BMS_MASTER` (`ACCOUNT_ID`), "
                sSQL += "CONSTRAINT `FK_BMS_MASTER` FOREIGN KEY (`ACCOUNT_ID`) REFERENCES `BMS_MASTER` (`ACCOUNT_ID`) ON DELETE RESTRICT "
                sSQL += ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci; "
                
                cursor.execute(sSQL)
                print("Accounts Table Created......\n")
                print("Database for BMS Application is ready......\n")
                print("BMS Application is ready to run......\n")
    except Exception as e:
        print(str(e))
    finally:
        if(connection is not None):
            if(connection.open == 1):
                if(cursor is not None):
                    cursor.close()
                    cursor = None
                    
                connection.close()
                connection = None
#Main function
def main():
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
        
        CreateDB()
        CreateTable()
        
        input("Press any key to continue......")
        sys.exit(0)
    except FileNotFoundError:
        print(str(e))
        input("Press any key to continue......")
    except TypeError:
        print(str(e))
        input("Press any key to continue......")
    except KeyboardInterrupt:
        print("KeyBoard Interruption Error Occured !")
        signal.signal(signal.SIGINT, sigint_handler)
    except Exception as e:
        print(str(e))
        input("Press any key to continue......")
        
main()
