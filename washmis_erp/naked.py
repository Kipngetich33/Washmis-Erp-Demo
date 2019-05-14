from Naked.toolshed.shell import execute_js, muterun_js

class Sending_Signals:
    def __init__(self,message,dev_address,edit_file,file_path):
        self.message = message
        self.dev_address = dev_address
        self.edit_file = edit_file
        self.file_path = file_path

    def edit_js(self):
        lines_n_messages = self.line_n_message()
        
        # read the line to replace
        file_read = open(self.edit_file)
        lines = file_read.readlines()
        message_to_replace = lines[3]
        address_to_replace = lines[10]
        file_read.close()
    
        # replace with new line
        s = open(self.edit_file).read()
        s = s.replace(message_to_replace,lines_n_messages[3])
        s = s.replace(address_to_replace,lines_n_messages[10])
        f = open(self.edit_file, 'w')
        f.write(s)
        f.close()
        

    def line_n_message(self):
        # replace the message part
        replacement_message = "my_message ='{}' \n".format(self.message)
        
        # replace the device address part
        replacement_address = "wsHost = 'ws://94.237.44.24:8080/ws/uplink/{}' \n".format(self.dev_address)
        return {3:replacement_message,10:replacement_address}

    def run_js(self):
        try:
            js_command = self.file_path
            return execute_js(js_command)
        except Exception as e:
            print e


    def main(self):
        '''
        Function that runs the other functions
        '''
        self.edit_js()
        self.run_js()
