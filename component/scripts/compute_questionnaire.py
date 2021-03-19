import json
import random

import pandas as pd

from component import parameter as cp

def compute_questionnaire(questionnaire_io):
    """use the questionnaire answers to produce a layer list of weight"""
    
    # description of the questionnaire_io inputs 
    
    # questionnaire_io.goals = name of the restoration goal
    # questionnaire_io.priorities = { priorityName: value from 0 to 4 } for each priority as json dict
    # questionnaire_io.potential = [ [names of land use that allow restration], treecover] as json list
    # questionnaire_io.constraints = { name of the criteria : [ bool activated, bool gt or lt, value] } for each criteria as json dict
    
    # at the moment we just load random weight values

    priorities = json.loads(questionnaire_io.priorities)

    def assign_weights(index, row):
        layer_dict ={
                'name'   : row.layer_name,
                'theme' : row.theme,
                'subtheme' : row.subtheme,
                'layer': row.gee_asset.strip(),
        }
        if row.theme == "benefits" :
            layer_dict['weight'] = priorities[layer_dict['subtheme']]
        else:
            layer_dict['weight'] = 0

        return layer_dict
    
    layers_values= [ assign_weights(i, row) for i, row in pd.read_csv(cp.layer_list).fillna('').iterrows() ]

    
    
    return layers_values