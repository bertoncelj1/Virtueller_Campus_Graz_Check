import requests
from pyquery import PyQuery
from getpass import getpass

# you can set your username and password into these two variables so that you don't have to type it all the time
username = ""
password = ""

debug = False

def write_file(file_name, content):
    file = open(file_name,"w")
    file.write(content)
    file.close()


def get_first_page(session):
    url = "https://vcadmin.vc-graz.ac.at/vcg/mod-todolist/todoOverview.xhtml"

    webpage = session.post(url).text
    if debug:
        write_file("first.html", webpage)
        
    pq = PyQuery(webpage.encode())
    tag = pq('[name="javax.faces.ViewState"]')
    view_state = (tag.attr("value"))
    return view_state
    
    
def get_info_page(session, view_state):
    url = "https://vcadmin.vc-graz.ac.at/vcg/mod-todolist/todoOverview.xhtml"
    data = {
    'javax.faces.partial.ajax': 'true',
    'artus_form:menuId': 'artus_form:menuId',
    'artus_form:menuId_menuid': '2_0',
    'artus_form': 'artus_form',
    'javax.faces.ViewState': view_state
    }

    webpage = session.post(url, data=data).text
    if debug:
        write_file("info.html", webpage)
        
    pq = PyQuery(webpage.encode())
    accountid = pq('#artus_form\:j_idt109\:accountid').attr("value")
    transferlimit = pq('#artus_form\:j_idt117\:transferlimit').attr("value")
    current_transfer = pq('#artus_form\:j_idt125\:currenttransfer').attr("value")
    current_transfer_up = pq('#artus_form\:j_idt141\:currenttransfer_up').attr("value")
    current_transfer_down = pq('#artus_form\:j_idt149\:currenttransfer_down').attr("value")
    current_transfer_percent = pq("#artus_form\:j_idt133\:currenttransferpercent").attr("value")
    print("")
    print("")
    print("Account Id: " + str(accountid))
    print("Limit: " + transferlimit + " GB")
    print("Used: " + current_transfer_percent)
    print("Transfer: %s (d:%s u:%s)" % (current_transfer, current_transfer_down, current_transfer_up))


def login(session, username, password):
    url = "https://vcadmin.vc-graz.ac.at/vcg/j_security_check"
    data = {
    'j_password': password,
    'j_username': username,
    }

    webpage = session.post(url, data=data)
    if debug:
        write_file("login.html", webpage)
    
    return len(webpage.text) == 0
    


session = requests.Session()

print("Logging in")
login_succesful = False
while not login_succesful:
    if len(username) == 0:
        print("You can set your username and password inside the code so that you don't have to write them all the time")
        username_tmp = input("Username: ") # temporary username typed by user 
    else:
        username_tmp = username
        print("Username: " + username)
        
    if len(password) == 0:
        password_tmp = getpass("Password: ")
    else:
        password_tmp = password
        
    login_succesful = login(session, username_tmp, password_tmp)
    
    if not login_succesful:
        print()
        print("Wrong username or password")
        print()
        username_tmp = ""
    


print("Getting first page")
view_state = get_first_page(session)
print("Getting user info")
get_info_page(session, view_state)

