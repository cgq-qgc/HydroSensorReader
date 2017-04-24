#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'xmalet'
__date__ = '2017-04-11'
__description__ = " "
__version__ = '1.0'

from database.db_acces_layer.main_access import MainControllerSingleton
from database.db_acces_layer.process_access import ProcessSingleton
from database.db_acces_layer.sampling_feature_access import SamplingFeaturesSingleton as SF_db_access
from domain_element.sampling_feature import *


class Sampling_features_controller_Singleton(object):
    _instances = None

    def __new__(cls, *args, **kwargs):
        if (cls._instances == None):
            cls._instances = _Sampling_features_controller()
        return cls._instances


class _Sampling_features_controller(object):
    def __init__(self):
        self._sampling_feature_dict = {}

    def get_references_for_user(self) -> list:
        return MainControllerSingleton().get_references_for_user().fetchall()

    def get_sampling_context_relation_type_for_specimen(self):
        return SF_db_access().get_sampling_context_relation_type_for_specimen()

    def create_spatial_sampling_feature(self) -> int:
        new_spatial_samp_feat = SpatialSamplingFeature()
        new_spatial_samp_feat.update_unique_id(SF_db_access())
        self._sampling_feature_dict[new_spatial_samp_feat.foi_id] = new_spatial_samp_feat
        return new_spatial_samp_feat.foi_id

    def create_specimen(self):
        new_specimen = Specimen()
        new_specimen.update_unique_id(SF_db_access())
        self._sampling_feature_dict[new_specimen.foi_id] = new_specimen
        return new_specimen.foi_id

    def get_sampling_feature_by_foi_id(self, foi_id) -> SamplingFeature:
        if foi_id in self._sampling_feature_dict.keys():
            return self._sampling_feature_dict[foi_id]
        else:
            raise Exception("aucun sampling feature avec ce foi_id")

    def get_specimen_by_foi_id(self, foi_id) -> Specimen:
        try:
            if isinstance(self.get_sampling_feature_by_foi_id(foi_id), Specimen):
                return self._sampling_feature_dict[foi_id]
            else:
                raise Exception("Ce n'est pas un specimen")
        except Exception as e:
            raise e

    def get_spatial_sampling_feature_by_foi_id(self, foi_id) -> SpatialSamplingFeature:
        try:
            if isinstance(self.get_sampling_feature_by_foi_id(foi_id), SpatialSamplingFeature):
                return self._sampling_feature_dict[foi_id]
            else:
                raise Exception("Ce n'est pas un spatial_sampling_feature")
        except Exception as e:
            raise e

    def set_sampling_feature_by_foi_id(self, sampling_feature):
        """
        
        :param sampling_feature: 
        :type sampling_feature: SamplingFeature
        :return: 
        """
        self._sampling_feature_dict[sampling_feature.foi_id] = sampling_feature

    def get_foi_id_list_of_controller(self) -> list:
        return list(self._sampling_feature_dict.keys())

    def clear_sampling_feature_list(self):
        self._sampling_feature_dict.clear()

    def insert_all_sampling_feature(self):
        for foi_id in list(self._sampling_feature_dict.keys()):
            self.insert_specific_sampling_feature(foi_id)
        for child_foi_id in list(self._sampling_feature_dict.keys()):
            self.insert_specific_sampling_context(child_foi_id)

    def insert_specific_sampling_feature(self, p_foi_id):
        sampling_feature = self.get_sampling_feature_by_foi_id(p_foi_id)
        sampling_feature.insert_in_database(SF_db_access())

    def insert_specific_sampling_context(self, p_foi_id):
        sampling_feature = self.get_sampling_feature_by_foi_id(p_foi_id)
        sampling_feature.sampling_context.insert_in_database(SF_db_access())

    def get_sample_interet(self):
        return SF_db_access().get_sample_interet()

    def get_process_type(self):
        return ProcessSingleton().get_process_for_display()

    def get_process_by_categorie(self, categorie):
        return ProcessSingleton().get_process_description(categorie)

    def get_process_description_by_process_id_and_category(self, categorie, process_id):
        return ProcessSingleton().get_process_description_by_process_id_and_category(categorie, process_id)

    def update_sampling_feature(self, foi_id: int,
                                process: int = None,
                                name: str = None,
                                date: str = None,
                                note: str = None,
                                ref_id: int = None,
                                id_bd_extern: str = None,
                                interet: int = None,
                                metadata: int = None) -> None:
        """
        permet d'updater un sampling feature à partir de données
        :param foi_id: identifiant du sampling feature
        :param process: process_id correspondant à la methode
        :param name: nom du sampling feature
        :param date: date associée au sampling feature
        :param note: notes du sampling feature (max 1000 caractères)
        :param ref_id: reference (provenance) du sampling feature
        :param id_bd_extern: id de BD externe du sampling feature
        :param interet: type de sampling feature
        :param metadata: s'il y a d'autres métadonnées associées au sampling feature
        :return: 
        """
        sampling_feature = self.get_sampling_feature_by_foi_id(foi_id)
        sampling_feature.process_id = process
        sampling_feature.sampling_name = name
        sampling_feature.sampling_date = date
        sampling_feature.sampling_note = note
        sampling_feature.ref_id = ref_id
        sampling_feature.id_bd_extern = id_bd_extern
        sampling_feature.interet = interet
        sampling_feature.metadata = metadata


if __name__ == '__main__':
    control = Sampling_features_controller_Singleton()
