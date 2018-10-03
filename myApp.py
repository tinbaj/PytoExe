 # myApp.py
"""
This is the file which contains the main function
"""
import sys
import ReadFile as ReadFile
import Packages


class myApp:
    def __init__(self):
        pass
    def __call__(self, *args, **kwargs):
        pass
    def main(self,**kwargs):
        """
        This is the main function of the App
        :param self:
        :param kwargs:
        :return:
        """

        Logger = Packages.LoggerDetails()
        log = Logger.setLogger()
        returnVal = {}

        print(kwargs)
        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug("-----------------Starting new Parsing-------------")
            log.debug('Entering function main(self,**kwargs) of Module: ' + __name__)

        try:
            funcName = Packages.Utilities.getValuefromDict(kwargs, 'funcName', 'Y')
            fileName = Packages.Utilities.getValuefromDict(kwargs, 'fileName', 'Y')
            funcInput = Packages.Utilities.getValuefromDict(kwargs, 'funcInput', 'Y')

            print('funcName : ', funcName)
        except ValueError as error:
            log.error(repr(error))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function main(self,**kwargs) of Module: ' + __name__)
            returnVal["retval"] = Packages.sv.XL_FAILURE
            returnVal["recordCount"] = 0
            return returnVal
        try:
            if str(funcName).upper() == "CSV":
                retval = ReadFile.ReadFile.file_tokenizer_csv(fileName, funcInput)
                if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                    recordCount = list(retval)[1]
                    log.debug('Value returned from function:file_tokenizer_txt is:  {0}  of Module: '.format(retval) + __name__)
            elif str(funcName).upper() == "TXT":
                retval = ReadFile.ReadFile.file_tokenizer_txt(fileName, funcInput)
                if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                    recordCount = list(retval)[1]
                    log.debug('Value returned from function:file_tokenizer_txt is:  {0}  of Module: '.format(retval) + __name__)

            elif str(funcName).upper() == "XML":
                retval = ReadFile.ReadFile.file_tokenizer_xml(fileName, funcInput)

                if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                    recordCount = list(retval)[1]
                    print("Number of records processed = {0}".format(recordCount))
                    log.debug('Value returned from function:file_tokenizer_txt is:  {0}  of Module: '.format(retval) + __name__)
            else:
                log.error("Invalid value: {0} passed for parameter: funcName.".format(funcName))
                raise ValueError('Invalid value: {0} passed for parameter: funcName.'.format(funcName))

        except ValueError as error:
            log.error(repr(error))
            if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
                log.debug('Exiting function main(self,**kwargs) of Module: ' + __name__)
            returnVal["retval"] = Packages.sv.XL_FAILURE
            returnVal["recordCount"] = 0
            return returnVal


        if log.getEffectiveLevel() == Packages.sv.XL_DEBUG:
            log.debug('Exiting function main(self,**kwargs) of Module: ' + __name__)
            log.debug("-----------------End ofParsing-------------")
        returnVal["retval"] = Packages.sv.XL_SUCCESS
        returnVal["recordCount"] = recordCount
        return returnVal
