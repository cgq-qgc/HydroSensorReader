import unittest
from database.database_tester.database_content_tester import DataBaseTesterSingleton
DataBaseTesterSingleton()

from controller.sampling_feature_controller import Sampling_features_controller_Singleton as SF_control

from interface.sampling_features_interfaces import *

class SamplingFeatureControllerTest(unittest.TestCase):
    def setUp(self):
        self.controller = SF_control()
        self.controller.clear_sampling_feature_list()

    def test_create_specimen(self):
        foi_id = self.controller.create_specimen()
        self.assertIsInstance(self.controller.get_sampling_feature_by_foi_id(foi_id),OM_SamplingFeatureInterface)
        self.assertIsInstance(self.controller.get_sampling_feature_by_foi_id(foi_id), OM_SpecimenInterface)

        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sampling_feature.sampling_name is None,
                        "Le sampling feature ne devrait pas avoir de nom")
        self.assertTrue(self.controller.get_sampling_feature_by_foi_id(foi_id).sampling_feature.ref_id is None)

    def test_update_specimen(self):
        foi_id = self.controller.create_specimen()

        interface = self.controller.get_sampling_feature_by_foi_id(foi_id)
        self.controller.update_sampling_feature(foi_id,name='teste')
        self.assertTrue(interface.sampling_feature.sampling_name == 'teste')

        interface.specimen.sample_type = 5
        self.assertTrue(interface.specimen.sample_type == 5)



suite = unittest.TestLoader().loadTestsFromTestCase(SamplingFeatureControllerTest)
unittest.TextTestRunner(verbosity=2).run(suite)
