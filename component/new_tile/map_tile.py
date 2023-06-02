from sepal_ui import mapping as sm
from sepal_ui import sepalwidgets as sw
from sepal_ui import aoi

from component import new_model as cmod
from component import new_widget as cw
from component import new_scripts as cs
from component import parameter as cp
from component.message import cm

from .export_control import ExportControl
from .about_control import AboutControl
from .aoi_control import AoiControl
from .priority_control import PriorityControl
from .cost_control import CostControl
from .constraint_control import ConstraintControl
from .dashboard_control import DashBoardControl


class MapTile(sw.Tile):
    def __init__(self):

        # set the map in the center
        self.map = sm.SepalMap()
        self.map.add_basemap("SATELLITE")

        # replace the basemapcontrol
        self.map.remove_control(
            next(c for c in self.map.controls if isinstance(c, sm.LayersControl))
        )
        self.map.add_control(cw.LayersControl(self.map))

        # add a layerstate (there are too many of them)
        layer_state_control = sm.LayerStateControl(self.map, position="bottomleft")

        # create the models
        self.aoi_model = aoi.AoiModel()
        priority_model = cmod.PriorityModel()
        cost_model = cmod.CostModel()
        constraint_model = cmod.ConstraintModel()

        # link them in a seplan_buider
        self.seplan_builder = cs.Seplan(
            self.aoi_model, priority_model, cost_model, constraint_model
        )

        # create the parameters controls
        full_control = sm.FullScreenControl(self.map, True, True, position="topright")
        val_control = sm.InspectorControl(self.map, False, position="bottomleft")
        export_control = ExportControl(position="bottomleft")
        about_control = AboutControl(position="bottomleft")
        aoi_control = AoiControl(self.map, self.aoi_model, position="bottomright")
        priority_control = PriorityControl(
            self.map, priority_model, position="bottomright"
        )
        cost_control = CostControl(self.map, cost_model, position="bottomright")
        constraint_control = ConstraintControl(
            self.map, constraint_model, self.aoi_model, position="bottomright"
        )
        dashboard_control = DashBoardControl()

        # create the viz controls
        priority_layer_control = cw.PriorityLayersControl(
            self.map, self.aoi_model, priority_model, position="topleft"
        )
        cost_layer_control = cw.CostLayersControl(
            self.map, self.aoi_model, cost_model, position="topleft"
        )
        constraint_layer_control = cw.ConstraintLayersControl(
            self.map, self.aoi_model, constraint_model, position="topleft"
        )
        self.index_layer_control = cw.IndexLayersControl(self.map, position="topleft")

        # add them on the map
        self.map.add_control(layer_state_control)
        self.map.add(val_control)
        self.map.add(export_control)
        self.map.add(about_control)

        self.map.add(dashboard_control)
        self.map.add(constraint_control)
        self.map.add(cost_control)
        self.map.add(priority_control)
        self.map.add(aoi_control)

        self.map.add(self.index_layer_control)
        self.map.add(constraint_layer_control)
        self.map.add(cost_layer_control)
        self.map.add(priority_layer_control)

        super().__init__(id_="map_tile", title="", inputs=[self.map])

        # add few js behavior
        self.aoi_model.observe(self.compute_index, "name")
        cost_model.observe(self.compute_index, "validated")
        priority_model.observe(self.compute_index, "validated")
        constraint_model.observe(self.compute_index, "validated")

    def compute_index(self, *args):

        if self.aoi_model.feature_collection is None:
            return

        # ste the prefix
        _prefix = "[index]"

        # priority only indicatior
        index = self.seplan_builder.get_priority_index(clip=True).multiply(4).add(1)
        layer = cs.get_layer(
            index, cp.final_viz, _prefix + cm.index.layers.priorities, False
        )
        self.map.add_layer(layer)

        # priority/cost ratio
        index = (
            self.seplan_builder.get_priority_cost_index(clip=True).multiply(4).add(1)
        )
        layer = cs.get_layer(
            index, cp.final_viz, _prefix + cm.index.layers.ratio, False
        )
        self.map.add_layer(layer)

        # filtered by constraints
        index = self.seplan_builder.get_constraint_index(clip=True).multiply(4).add(1)
        layer = cs.get_layer(index, cp.final_viz, _prefix + cm.index.layers.final, True)
        self.map.add_layer(layer)

        # update the layer control
        self.index_layer_control.update_index()
