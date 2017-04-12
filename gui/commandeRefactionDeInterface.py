__author__ = 'Xavier'
__date__ = '2015-04-30'
__description__ = "Permet de lancer l'invite de commance afin de regenerer le code de  l'interface graphique en python"
__version__ = '1.0'

import os


def translate_ui(path, uiName, python_ui_name=None,is_om = False):
    """

    :param uiName:
    :type uiName: str
    :param python_ui_name:
    :type python_ui_name: str
    :return:
    """
    assert 'ui' in uiName, 'invalid name'

    if python_ui_name == None:
        python_ui_name = 'ui_' + uiName.replace('ui', 'py')
    else:
        assert '.py' in python_ui_name
    if is_om == False:
        os.system('pyuic4 -o'
                  ' {path}\\gui\\python_ui\\old_widget'
                  '\\{python_ui_name} -x'
                  ' {path}\\gui\\yqt_ui\\old_widget'
                  '\\{uiName}'
                  .format(path=path, uiName=uiName, python_ui_name=python_ui_name))
    else:
        os.system('pyuic4 -o'
                  ' {path}\\gui\\python_ui\\om'
                  '\\{python_ui_name} -x'
                  ' {path}\\gui\\pyqt_ui\\om'
                  '\\{uiName}'
                  .format(path=path, uiName=uiName, python_ui_name=python_ui_name))
    
    print('{} refait'.format(python_ui_name.replace('.py', '')))

def get_list_of_element():
    return os.listdir(os.path.join(path,'gui','pyqt_ui','old_widget'))


def refaire(path,is_om=False):
    print("_" * 30)
    print("En cours")
    try:
        if is_om ==False:
            list_of_window = get_list_of_element()
        else:
            list_of_window = get_list_of_om_window(path)
            
        for window in list_of_window:
            translate_ui(path=path, uiName=window, is_om=is_om)

        print("_" * 30)
        print('fini')
    except Exception as e:
        print(e)
        
def get_list_of_om_window(path):
    return os.listdir(os.path.join(path,'gui','pyqt_ui','om'))


if __name__ == '__main__':
    os.chdir(os.path.split(os.getcwd())[0])
    path = os.getcwd()
    print(path)
    # refaire(path, get_list_of_element())
    print(get_list_of_om_window(path))
    refaire(path,True)
