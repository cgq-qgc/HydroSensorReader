import unittest
from  controller.sampling_feature_controller import Sampling_features_controller_Singleton
from database.database_tester.database_content_tester import DataBaseTesterSingleton

DataBaseTesterSingleton()
from domain_element.sampling_feature import *
from interface.sampling_features_interfaces import *


class SamplingFeature_controllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = Sampling_features_controller_Singleton()
        self.controller.clear_sampling_feature_list()

    def test_create_sampling_feature(self):
        self.controller.create_specimen()
        self.assertNotEqual(len(self.controller.get_foi_id_list_of_controller()), 0,
                            "Le dictionnaire ne devrait pas être vide")
        self.assertEqual(len(self.controller.get_foi_id_list_of_controller()), 1)
        foi_id = list(self.controller.get_foi_id_list_of_controller())[0]
        self.assertNotEqual(foi_id, 0)

    def test_sampling_feature_creation(self):
        self.controller.create_specimen()
        foi_id = list(self.controller.get_foi_id_list_of_controller())[0]
        self.assertNotEqual(foi_id, 0)
        sampling_interface = self.controller.get_sampling_feature_by_foi_id(foi_id)
        self.assertNotEqual(sampling_interface.sampling_feature.sampling_context.child_foi_id, 0)
        self.assertEqual(sampling_interface.sampling_feature.foi_id,
                         sampling_interface.sampling_feature.sampling_context.child_foi_id)

    def test_create_specimen(self):
        foi_id = self.controller.create_specimen()
        self.assertIsInstance(self.controller.get_sampling_feature_by_foi_id(foi_id), OM_SamplingFeatureInterface)
        self.assertIsInstance(self.controller.get_sampling_feature_by_foi_id(foi_id), OM_SpecimenInterface)

        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sampling_feature.sampling_name is None,
                        "Le sampling feature ne devrait pas avoir de nom")
        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sampling_feature.ref_id is None)

    def test_update_specimen(self):
        foi_id = self.controller.create_specimen()

        interface = self.controller.get_sampling_feature_by_foi_id(foi_id)
        self.controller.update_sampling_feature(foi_id, name='teste')
        self.assertTrue(interface.sampling_feature.sampling_name == 'teste')

        interface.specimen.sample_type = 5
        self.assertTrue(interface.specimen.sample_type == 5)


suite = unittest.TestLoader().loadTestsFromTestCase(SamplingFeature_controllerTest)
unittest.TextTestRunner(verbosity=2).run(suite)
