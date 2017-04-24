import sys
import unittest

from PyQt4 import QtGui

from database.database_tester.database_content_tester import DataBaseTesterSingleton
from gui_controller.om_sampling_feature_gui_controller import Om_sampling_feature_gui_controller
import datetime
app = QtGui.QApplication(sys.argv)
DataBaseTesterSingleton()


class Gui_SF_Controller_Test(unittest.TestCase):
    def setUp(self):
        self.view = Om_sampling_feature_gui_controller()

    def setup_gb_id_bd_extern(self):
        self.view.gb_id_bd_extern.setChecked(True)

    def setup_combo(self):
        self.view.fill_sample_feature_type()
        self.view.fill_reference()

    def test_validate_id_bd_extern(self):
        self.setup_gb_id_bd_extern()

        self.view.LE_id_bd_extern.setText('teste')
        self.assertEqual(self.view.validate_id_bd_extern(), True, 'Est valide')

        self.view.LE_id_bd_extern.setText('')
        self.assertEqual(self.view.validate_id_bd_extern(), False, 'Est invalide')

        self.view.LE_id_bd_extern.setText(' ')
        self.assertEqual(self.view.validate_id_bd_extern(), False, 'Est invalide')

        self.view.LE_id_bd_extern.setText('')
        self.assertEqual(self.view.validate_id_bd_extern(), False, 'Est invalide')

        self.view.gb_id_bd_extern.setChecked(False)
        self.view.LE_id_bd_extern.setText('teste')
        self.assertEqual(self.view.validate_id_bd_extern(), False, 'Est invalide')

    def test_validate_sampling_name(self):
        self.view.LE_sampling_name.setText('teste')
        self.assertEqual(self.view.validate_sampling_name(), True, 'est valide')

        self.view.LE_sampling_name.setText('')
        self.assertEqual(self.view.validate_sampling_name(), False, 'est invalide')

        self.view.LE_sampling_name.setText('teste et teste')
        self.assertEqual(self.view.validate_sampling_name(), True, 'est valide')

        self.view.LE_sampling_name.setText('teste12544%?&*(_')
        self.assertEqual(self.view.validate_sampling_name(), True, 'est valide')

        self.view.LE_sampling_name.setText('       ')
        self.assertEqual(self.view.validate_sampling_name(), False, 'est valide')

    def test_validate_sampling_name_getter(self):
        for texte in [
            'teste', '', 'teste et teste', '1235496!"/$%?&*()_', "^¨:L`.:`^:ÉéÉàèÈ- "]:
            self.view.LE_sampling_name.setText(texte)
            self.assertEqual(self.view.get_sampling_name(), texte, 'est valide')

    def test_validate_combo_box(self):
        self.setup_combo()
        self.assertEqual(self.view.validate_combo_box(),False,'est invalide')


        self.view.CB_interet.setCurrentIndex(2)
        self.view.CB_ref.setCurrentIndex(2)
        self.assertEqual(self.view.validate_combo_box(),True,'est valide')

    def test_validate_date(self):
        self.view.set_date()

        self.assertTrue(self.view.validate_date())

        self.view.DTE_sampling_date.setDateTime(datetime.datetime(2500,12,1))
        self.assertFalse(self.view.validate_date())




suite = unittest.TestLoader().loadTestsFromTestCase(Gui_SF_Controller_Test)
unittest.TextTestRunner(verbosity=2).run(suite)
