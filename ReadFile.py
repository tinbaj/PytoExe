# ReadFile.py

"""
This file contains class ReadFile which has functions to parse xml, csv and text files

"""
import operator
import os
import re
from xmltodict import parse
import Packages

Logger = Packages.LoggerDetails()
log = Logger.setLogger()

class ReadFile:
    def __init__(self):
        pass
    def file_tokenizer_csv(fileName: str,funcInputs: dict):
        """
        This is a function to tokenize a csv file and create an output file which contains column indexes provided in the input
        The Output File will be names: <Input File Name>_output.csv in the same directory as the source file
        :param
        fileName: Name of the source file. The File name should have the absolute path to the file
        funcInputs: Dictionary containing a list with the indexes of all the columns that need to be extracted.
        :return: True = Success/ False = Failure
        """

        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug("Entering function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: "+__name__)
        try:
            file_obj_read = open(fileName,mode='r')
        except IOError:
            log.error("Cannot open file {0} in read mode".format(fileName))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug("Exiting function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: "+__name__)
            return Packages.sv.XL_FAILURE, 0

        try:
            file, extension = os.path.splitext(fileName)
            outputFile = file+'_output.csv'
            recCounter = 0
            outputStringBuffer = ""

            writeFile = open(outputFile,mode='w')
            file_content = file_obj_read.readlines()
            attr_list = dict(funcInputs).get('attr_list')
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug("attr_list is : {0}".format(attr_list))


            header,header1,header2,header3,*file_details = file_content
            listHeader = operator.itemgetter(*attr_list)(str(header).split(sep=';'))
            strHeader = ",".join(tknHeader for tknHeader in listHeader)
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strHeader + '\n')
            listHeader1 = operator.itemgetter(*attr_list)(str(header1).split(sep=';'))
            strHeader1 = ",".join(tknHeader1 for tknHeader1 in listHeader1)
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strHeader1 + '\n')
            listHeader2 = operator.itemgetter(*attr_list)(str(header2).split(sep=';'))
            strHeader2 = ",".join(tknHeader2 for tknHeader2 in listHeader2)
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strHeader2 + '\n')
            listHeader3 = operator.itemgetter(*attr_list)(str(header3).split(sep=';'))
            strHeader3 = ",".join(tknHeader3 for tknHeader3 in listHeader3)
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strHeader3 + '\n')

            for lst in file_details:
                recCounter += 1
                listAttributes = operator.itemgetter(*attr_list)(str(lst).split(sep=';'))
                strAttributes = ",".join(tknAttributes for tknAttributes in listAttributes)
                outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strAttributes + '\n')

            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Total Number of Records parsed in XML : {0} '.format(recCounter))
            writeFile.write(outputStringBuffer)
        except:
            log.error("Exeption Encountered")
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug("Exiting function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: " + __name__)
            return Packages.sv.XL_FAILURE, 0
        finally:
            writeFile.close()
            file_obj_read.close()
        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug("Exiting function file_tokenizer_csv(fileName: str,funcInputs: dict) of Module: " + __name__)
        return Packages.sv.XL_SUCCESS, recCounter

    def file_tokenizer_txt(fileName: str,funcInputs: dict):
        """
        This is a function to tokenize a txt file and create an output csv file which contains column provided in the input
        The Output File will be names: <Input File Name>_output.csv in the same directory as the source file
        :param
        fileName: Name of the source file. The File name should have the absolute path to the file
        funcInputs: Dictionary containing a list with the indexes of all the columns that need to be extracted.
            recordMarkerStartText (Mandatory): Text indicating the start of one record
            recordMarkerEndText (Mandatory): Text indicating the end of one record
            tableMarkerStartText (Mandatory): Text indicating the start of table withing a record
            tabledMarkerEndText (Mandatory): Text indicating the end of table withing a record
            headerMarkerStartText (Mandatory): Text indicating the start of header withing a record
            headerMarkerEndText (Mandatory): Text indicating the end of header withing a record
            headerFieldsSelection (Optional): List containing all the fields required from header
            tableFieldsSelection (Mandatory): List containing all the fields required from Table
            delimiter (Mandatory): delimiter for the values

        :return: True = Success/ False = Failure
        """
        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Entering function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)

        #Extract input Variables from the dictionary: funcInputs
        try:
            recordMarkerStartText = Packages.Utilities.getValuefromDict(funcInputs, 'recordMarkerStartText', 'Y')
            recordMarkerEndText = Packages.Utilities.getValuefromDict(funcInputs, 'recordMarkerEndText', 'Y')
            tableMarkerStartText = Packages.Utilities.getValuefromDict(funcInputs, 'tableMarkerStartText', 'Y')
            tableMarkerEndText = Packages.Utilities.getValuefromDict(funcInputs, 'tableMarkerEndText', 'Y')
            headerMarkerStartText = Packages.Utilities.getValuefromDict(funcInputs, 'headerMarkerStartText', 'N')
            headerMarkerEndText = Packages.Utilities.getValuefromDict(funcInputs, 'headerMarkerEndText', 'N')
            headerFieldsSelection = Packages.Utilities.getValuefromDict(funcInputs, 'headerFieldsSelection', 'Y')
            tableFieldsSelection = Packages.Utilities.getValuefromDict(funcInputs, 'tableFieldsSelection', 'Y')
            delimiter = Packages.Utilities.getValuefromDict(funcInputs, 'delimiter', 'Y')

        except ValueError as error:
            log.error(repr(error))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return  Packages.sv.XL_FAILURE

        tableHeaderHasUnits = True
        tableSeperator = 1

        headerMarkerStart = True
        tableMarkerStart = True
        recordMarkerStart = True
        tableIndexSelected = False
        headerPrinted = False

        headerMarkers = ()
        recordMarkers = ()
        tableMarkers = ()

        listHeaderMarkers = []
        listTableMarkers = []
        listRecordMarkers = []
        tableFieldIndex = []

        headerStart = 0
        headerEnd = 0
        tableStart = 0
        tableEnd = 0
        recordStart = 0
        recordEnd = 0
        outputStringBuffer = ""
        recCounter = 0
        file, extension = os.path.splitext(fileName)
        outputFileName = file + "_output.csv"

        try:
            writeFile = open(outputFileName, mode='w')
            try:
                with open(fileName,mode='r') as openFile:
                    for lineno,fileDetails in enumerate(openFile):
                        # Get start and end markets for record
                        if recordMarkerStartText in fileDetails and recordMarkerStart:
                            recordStart = lineno
                            recordMarkerStart = False
                        if recordMarkerEndText in fileDetails:
                            recordEnd = lineno
                            recordMarkers = recordStart, recordEnd
                            listRecordMarkers.append(recordMarkers)
                            recordMarkerStart = True
                        # Get start and end markets for Table
                        if tableMarkerStartText in fileDetails and tableMarkerStart:
                            tableStart = lineno
                            tableMarkerStart = False
                        if tableMarkerEndText in fileDetails:
                            tableEnd = lineno
                            tableMarkers = tableStart, tableEnd
                            listTableMarkers.append(tableMarkers)
                            tableMarkerStart = True

                        # Get start and end markets for Header
                        if headerMarkerStartText in fileDetails and headerMarkerStart:
                            headerStart = lineno
                            headerMarkerStart = False
                        if headerMarkerEndText in fileDetails:
                            headerEnd = lineno
                            headerMarkers = headerStart, headerEnd
                            listHeaderMarkers.append(headerMarkers)
                            headerMarkerStart = True
            except Exception as Ex:
                log.debug('Error in Getting Markers for Header,Record and Table')
                log.debug((repr(Ex)))
                if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                    log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                return Packages.sv.XL_FAILURE, 0

            # Creating header text for output File
            log.debug('Creating header text for output File')
            fileHeader = ','.join(fldList for fldList in (headerFieldsSelection+tableFieldsSelection))
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, fileHeader + '\n')

            index = 0
            recCounter = 0
            tablerecCounter = 0
            record = []
            recordTable = []
            print('len(listRecordMarkers) :',len(listRecordMarkers))
            with open(fileName, mode='r') as openFile:
                while index < len(listRecordMarkers):
                    recCounter += 1
                    try:
                        recordStartMarker, recordEndMarker = listRecordMarkers[index]
                        record = []
                        currentLine = ""
                        try:
                            while True:
                                currentLine = next(openFile)
                                if recordMarkerStartText in currentLine:
                                    record.append(currentLine)
                                    break
                        except StopIteration:
                            continue
                        #check logic to append to record
                        for _ in range(recordStartMarker,recordEndMarker):
                            record.append(next(openFile))

                        headerStartMarker = headerEndMarker = 0
                        headerStartMarker, headerEndMarker = listHeaderMarkers[index]
                        tableStartMarker = tableEndMarker = newTableMarker = 0
                        tableStartMarker, tableEndMarker = listTableMarkers[index]
                        index += 1

                        recordHeader = record[(headerStartMarker - recordStartMarker): (headerEndMarker - recordStartMarker)]
                        recordTable = record[(tableStartMarker - recordStartMarker): (tableEndMarker - recordStartMarker)]

                    except Exception as Ex:
                        log.debug('Error in Details of Header,Record and Table')
                        log.debug((repr(Ex)))
                        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                            log.debug(
                                'Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                        return Packages.sv.XL_FAILURE, 0

                    headerText = ""
                    fileHeader = ""
                    try:
                        for headText in recordHeader:
                            for headField in headerFieldsSelection:
                                if headField in headText:
                                    # Count number of delimiters in the line. if count = 1, then get the till the end of line and then tokenize based on delimiter
                                    if headText.count(delimiter) == 1:
                                        fieldDetails = re.findall('"' + headField + '.*?\n', headText, flags=re.DOTALL)
                                    elif headText.count(delimiter) == 0:
                                        #log.debug('No Delimiter found in the line for header filed: {0}'.format(headField))
                                        continue
                                    else:
                                        # Split the text based on delimiter and get the second item of the text after the text is split based on tokens
                                        fieldDetails = re.findall('"' + headField + '.*' + delimiter + '*?' + delimiter,
                                                                  headText, flags=re.DOTALL)
                                    if fieldDetails:
                                        if delimiter in fieldDetails[0]:
                                            if headerText:
                                                headerText += "," + \
                                                              str(fieldDetails[0]).replace('"', '').replace('\n', '').split(
                                                                  ',')[1]
                                            else:
                                                headerText = \
                                                str(fieldDetails[0]).replace('"', '').replace('\n', '').split(',')[1]
                                        else:
                                            log.debug('Delimiter not found in the field Details: {0}'.format(fieldDetails))
                                    else:
                                        log.debug('Details not found in the Header: {0}'.format(headText))
                                        headerText += ','

                    except Exception as Ex:
                        log.debug('Error in Getting Markers for Header')
                        log.debug("Record index : {0}".format(index))
                        log.debug((repr(Ex)))
                        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                            log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                        return Packages.sv.XL_FAILURE, 0
                     # Calculate number of lines to table start from the start table token
                    counter = 0
                    for tableData in recordTable:
                        if tableFieldsSelection[0] in tableData:
                            break
                        else:
                            counter += 1

                    tableHeaderList = []

                    if tableHeaderHasUnits:
                        newTableMarker = counter + tableSeperator + 1
                    else:
                        newTableMarker = counter + tableSeperator

                    try:
                        # Create a list of header items for the table
                        for tableHeader in recordTable[counter:newTableMarker]:
                            tableHeaderList.append((tableHeader).replace('"', '').split(','))


                        # Get Table Header
                        if not tableIndexSelected:
                            for tableFields in tableFieldsSelection:
                                fieldIndex = tableHeaderList[0].index(tableFields)
                                tableFieldIndex.append(fieldIndex)
                                tableIndexSelected = True

                        # if table has header Units then get the units
                        if tableHeaderHasUnits and not headerPrinted:
                            headerPrinted = True
                            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer,
                                                                        ',' * len(headerFieldsSelection)
                                                                     + ','.join(string for string in
                                                                                   operator.itemgetter(
                                                                                       *tableFieldIndex)
                                                                                   (str(','.join(
                                                                                       lstItem for lstItem
                                                                                       in tableHeaderList[
                                                                                           1])).replace('"',
                                                                                                        '').split(
                                                                                       delimiter))) + '\n')


                         # get table data
                        for tableData in recordTable[newTableMarker:len(recordTable)]:
                            if delimiter in tableData:
                                tablerecCounter += 1
                                outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer,
                                                                         headerText + ','.join(
                                                                                string for string in
                                                                                operator.itemgetter(
                                                                                    *tableFieldIndex)(
                                                                                    str(tableData).replace(
                                                                                        '"', '').split(
                                                                                        delimiter))) + '\n')



                    except Exception as Ex:
                        log.debug('Error in Getting Parsing for Table')
                        log.debug("Record index : : {0}".format(index))
                        log.debug((repr(Ex)))
                        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                            log.debug(
                                'Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
                        return Packages.sv.XL_FAILURE, 0

            writeFile.write(outputStringBuffer)
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Total Number of Records parsed in TXT : {0} '.format(recCounter))
                log.debug('Total Number of Table Records in TXT : {0} '.format(tablerecCounter))
        except IOError:
            log.error('Cannot open file: {0} in read mode'.format(fileName))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return  Packages.sv.XL_FAILURE,0

        except Exception as error:
            print(repr(error))
            log.error('Exception Encountered in function: file_tokenizer_txt')
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.sv.XL_FAILURE,0
        finally:
            writeFile.close()

        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
        return Packages.sv.XL_SUCCESS,recCounter

    def file_tokenizer_xml(fileName: str, funcInputs: dict):
        """
        This is a function to tokenize a xml file and create an output csv file which contains details for tags provided in the input
        The Output File will be names: <Input File Name>_output.csv in the same directory as the source file
        :param
        fileName: Name of the source file. The File name should have the absolute path to the file
        funcInputs: Dictionary containing a list with the indexes of all the columns that need to be extracted.
            parentTag (Mandatory): Tag which breaks two records
            headerFields (Mandatory): A List containing all the attributes which will be marked as header records, format: parentTag:tag
            tableFields (Mandatory): A List containing all the attributes which will be marked as table records tags, format: parentTag:tag
            tabledMarkerEndText (Mandatory): Text indicating the end of table withing a record

        :return: True = Success/ False = Failure
        """

        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Entering function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)

        try:
            if dict(funcInputs).get("tableHeader"):
                tableHeader = dict(funcInputs).get("tableHeader")
            else:
                tableHeader = []

            if dict(funcInputs).get("header"):
                header = dict(funcInputs).get("header")
            else:
                header = []

            if dict(funcInputs).get("fields"):
                fields = dict(funcInputs).get("fields")
            else:
                fields = []

            parentTag = Packages.Utilities.getValuefromDict(funcInputs, 'parentTag')
            headerFields = Packages.Utilities.getValuefromDict(funcInputs, 'headerFields')
            tableFields = Packages.Utilities.getValuefromDict(funcInputs, 'tableFields')
            listRecordMarkers = []
            recCounter = 0
            recordMarkerStart = True

        except ValueError as error:
            log.error(repr(error))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.sv.XL_FAILURE

        try:
            OpenFile = open(fileName, mode='r').read()
        except IOError:
            log.error('Cannot open filename: {0} in read mode'.format(fileName))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.sv.XL_FAILURE
        try:
            fileName, extension = os.path.splitext(fileName)
            writeFile = open(fileName + 'output.csv', mode='w')
            patternMarker = '<' + parentTag + '[>| ].*?</' + parentTag + '>'
            tokenMatches = re.finditer(patternMarker, OpenFile, flags=re.MULTILINE | re.DOTALL)
            currentHeaderRecord = ''
            outputStringBuffer = ''
            recCounter = 0

            for tm in tokenMatches:
                tableHeader = []
                funcInputs['tableHeader'] = tableHeader
                start, end = tm.span()
                parsedRecord = parse(OpenFile[start:end])

                for k, v in parsedRecord.items():
                    if type(v) is str:
                        Packages.Utilities.getHeader(k, k, funcInputs)
                    else:
                        Packages.Utilities.parseHeader(k, v, funcInputs)

                tableHeader = dict(funcInputs).get('tableHeader')
                headerRecord = ','.join(strHeader for strHeader in tableHeader)

                if len(currentHeaderRecord) < len(headerRecord):
                    currentHeaderRecord = headerRecord
            outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, headerRecord + '\n')

            tokenMatches = re.finditer(patternMarker, OpenFile, flags=re.MULTILINE | re.DOTALL)

            # Get data for the parsed file
            for tm in tokenMatches:
                recCounter += 1
                tableHeader = []
                header = []
                fields = []

                funcInputs['tableHeader'] = tableHeader
                funcInputs['header'] = header
                funcInputs['fields'] = fields

                start, end = tm.span()
                parsedRecord = parse(OpenFile[start:end])

                for k, v in parsedRecord.items():
                    if type(v) is str:
                        Packages.Utilities.getValue(k, k, v, funcInputs)
                    else:
                        Packages.Utilities.parseList(k, v, funcInputs)

                tableHeader = funcInputs.get('tableHeader')
                header = funcInputs.get('header')
                fields = funcInputs.get('fields')

                fullRecord = header + fields

                recordHeader = ','.join(strHeader for strHeader in tableHeader)

                indexHeader = 0
                indexRecord = 0
                strRecord = 0

                if len(headerRecord) == len(recordHeader):
                    strRecord = ','.join(strData for strData in fullRecord)
                else:
                    while (indexHeader < len(headerRecord.split(','))):
                        if tableHeader[indexRecord] == headerRecord.split(',')[indexHeader]:
                            if strRecord:
                                strRecord += ',' + str(fullRecord[indexRecord])
                                indexHeader += 1
                                indexRecord += 1
                            else:
                                strRecord = str(fullRecord[indexRecord])
                                indexHeader += 1
                                indexRecord += 1
                        else:
                            strRecord += ','
                            indexHeader += 1
                outputStringBuffer = Packages.Utilities.writeFile(writeFile, outputStringBuffer, strRecord + '\n')

            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Total Number of Records parsed in XML : {0} '.format(recCounter))

            writeFile.write(outputStringBuffer)
            writeFile.close()

        except Exception as Ex:
            log.debug('Error in Getting Markers for Header,Record and Table')
            log.debug((repr(Ex)))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function file_tokenizer_txt(fileName: str,funcInputs: dict) of Module: ' + __name__)
            return Packages.sv.XL_FAILURE, 0


        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Exiting function file_tokenizer_xml(fileName: str,funcInputs: dict) of Module: ' + __name__)
        return Packages.sv.XL_SUCCESS, recCounter
