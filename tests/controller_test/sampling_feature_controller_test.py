import unittest
from database.database_tester.database_content_tester import DataBaseTesterSingleton
DataBaseTesterSingleton()

from controller.sampling_feature_controller import Sampling_features_controller_Singleton as SF_control

from domain_element.sampling_feature import *
class SamplingFeatureControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = SF_control()
        self.controller.clear_sampling_feature_list()

    def test_create_specimen(self):
        foi_id = self.controller.create_specimen()
        self.assertIsInstance(self.controller.get_sampling_feature_by_foi_id(foi_id),SamplingFeature)
        self.assertIsInstance(self.controller.get_sampling_feature_by_foi_id(foi_id), Specimen)

        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sampling_name is None,
                        "Le sampling feature ne devrait pas avoir de nom")
        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).ref_id is None)

    def test_update_specimen(self):
        foi_id = self.controller.create_specimen()

        self.controller.update_sampling_feature(foi_id,name='teste')
        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sampling_name == 'teste')

        self.controller.get_specimen_by_foi_id(foi_id).sample_type = 5
        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sample_type == 5)



suite = unittest.TestLoader().loadTestsFromTestCase(SamplingFeatureControllerTest)
unittest.TextTestRunner(verbosity=2).run(suite)
